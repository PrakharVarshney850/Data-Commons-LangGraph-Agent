"""
LangGraph Agent with Data Commons MCP Server Integration

This agent can answer questions about statistical data using the Data Commons MCP server.
"""

import os
import sys
import json
import httpx
from typing import TypedDict, Annotated, Sequence

from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Configure stdout for UTF-8 encoding (Windows compatibility)
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Load environment variables
load_dotenv()

# MCP Server Configuration
MCP_SERVER_URL = "http://localhost:8889/mcp"


class AgentState(TypedDict):
    """State of the agent"""
    messages: Annotated[Sequence[BaseMessage], "The messages in the conversation"]
    next_action: str


class MCPClient:
    """Client for communicating with the MCP server"""

    def __init__(self, server_url: str):
        self.server_url = server_url
        self.session_id = None

    async def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """Call an MCP tool"""

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.server_url,
                json=payload,
                headers=headers
            )

            if response.status_code == 200:
                # Parse SSE response
                lines = response.text.strip().split('\n')
                for line in lines:
                    if line.startswith('data: '):
                        data = json.loads(line[6:])
                        if 'result' in data:
                            return data['result']
                        elif 'error' in data:
                            raise Exception(f"MCP Error: {data['error']}")

            raise Exception(f"Unexpected response: {response.status_code} - {response.text}")


# Initialize MCP client
mcp_client = MCPClient(MCP_SERVER_URL)


async def search_indicators(query: str, places: list[str] = None, include_topics: bool = True):
    """
    Search for statistical indicators in Data Commons.

    Args:
        query: Search query (e.g., "GDP", "population", "health data")
        places: List of place names to filter by (e.g., ["United States", "China"])
        include_topics: Whether to include topic categories
    """
    arguments = {
        "query": query,
        "include_topics": include_topics
    }

    if places:
        arguments["places"] = places

    result = await mcp_client.call_tool("search_indicators", arguments)
    return result


async def get_observations(
    variable_dcid: str,
    place_dcid: str,
    date: str = "latest",
    child_place_type: str = None
):
    """
    Fetch observations for a statistical variable.

    Args:
        variable_dcid: The variable identifier (from search_indicators)
        place_dcid: The place identifier
        date: 'latest', 'all', 'range', or specific date (YYYY, YYYY-MM, YYYY-MM-DD)
        child_place_type: Optional - get data for all child places of this type
    """
    arguments = {
        "variable_dcid": variable_dcid,
        "place_dcid": place_dcid,
        "date": date
    }

    if child_place_type:
        arguments["child_place_type"] = child_place_type

    result = await mcp_client.call_tool("get_observations", arguments)
    return result


async def fetch_statistical_data(
    query: str,
    places: list[str] = None,
    date: str = "latest"
):
    """
    Combined helper: Search and fetch data in one step.

    This function automatically:
    1. Searches for indicators matching the query
    2. Extracts the first matching variable and place DCIDs
    3. Fetches the actual observations

    Args:
        query: What to search for (e.g., "population", "GDP", "unemployment rate")
        places: List of place names (e.g., ["India", "United States"])
        date: Date filter for observations (default: "latest")
    """
    try:
        # Step 1: Search for indicators
        search_result = await search_indicators(query, places, include_topics=False)

        # Parse the search result to extract DCIDs
        if isinstance(search_result, dict):
            # Look for variables in the result
            variables = search_result.get("content", [{}])[0].get("text", "")

            # Try to extract variable_dcid and place_dcid from the result
            # This is a simplified extraction - in production, use proper JSON parsing
            import re

            # Extract variable DCID (pattern: dcid like "Count_Person", "Amount_EconomicActivity_...")
            var_match = re.search(r'"dcid":\s*"([^"]+)"', str(variables))
            variable_dcid = var_match.group(1) if var_match else None

            # Extract place DCID (pattern: country/XXX or geoId/XXX)
            place_match = re.search(r'"placeDcid":\s*"([^"]+)"', str(variables))
            place_dcid = place_match.group(1) if place_match else None

            # If we found both DCIDs, fetch the observations
            if variable_dcid and place_dcid:
                observations = await get_observations(
                    variable_dcid=variable_dcid,
                    place_dcid=place_dcid,
                    date=date
                )
                return {
                    "search_result": search_result,
                    "observations": observations,
                    "variable_dcid": variable_dcid,
                    "place_dcid": place_dcid
                }
            else:
                return {
                    "error": "Could not extract DCIDs from search results",
                    "search_result": search_result,
                    "suggestion": "Try using search_indicators and get_observations separately"
                }

        return {
            "error": "Unexpected search result format",
            "search_result": search_result
        }

    except Exception as e:
        return {
            "error": f"Failed to fetch data: {str(e)}",
            "suggestion": "Try using search_indicators and get_observations separately for more control"
        }


# Define available tools for the LLM
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "fetch_statistical_data",
            "description": "EASIEST OPTION: One-step tool to search and fetch actual statistical data. Automatically searches for indicators and retrieves actual values. Use this for simple queries. If this fails, fall back to the two-step approach (search_indicators + get_observations).",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "What to search for (e.g., 'population', 'GDP', 'unemployment rate')"
                    },
                    "places": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of place names (e.g., ['India', 'United States'])"
                    },
                    "date": {
                        "type": "string",
                        "description": "Date filter: 'latest', 'all', or specific date (default: 'latest')"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_indicators",
            "description": "STEP 1: Search for statistical indicators (variables) and topics in Data Commons. Returns variable DCIDs and place DCIDs. YOU MUST call get_observations next with the DCIDs from this result to get actual data values. This tool alone does NOT return actual statistical values.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query (e.g., 'GDP', 'population', 'unemployment')"
                    },
                    "places": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of place names to filter results (e.g., ['United States', 'China'])"
                    },
                    "include_topics": {
                        "type": "boolean",
                        "description": "Whether to include topic categories in results (default: true)"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_observations",
            "description": "STEP 2: Fetch the ACTUAL statistical data values for a specific variable and place. REQUIRED after search_indicators. Use the exact variable_dcid and place_dcid extracted from search_indicators results. This is the ONLY tool that returns actual numerical data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "variable_dcid": {
                        "type": "string",
                        "description": "The DCID of the statistical variable (extracted from search_indicators results, e.g., 'Count_Person', 'Amount_EconomicActivity_GrossValue_Goods')"
                    },
                    "place_dcid": {
                        "type": "string",
                        "description": "The DCID of the place (extracted from search_indicators results, e.g., 'country/IND', 'country/USA', 'geoId/06')"
                    },
                    "date": {
                        "type": "string",
                        "description": "Date filter: 'latest', 'all', 'range', or specific date (default: 'latest')"
                    },
                    "child_place_type": {
                        "type": "string",
                        "description": "Optional - type of child places to get data for (e.g., 'State', 'County')"
                    }
                },
                "required": ["variable_dcid", "place_dcid"]
            }
        }
    }
]


async def call_tool(tool_name: str, tool_args: dict) -> str:
    """Execute a tool call"""
    if tool_name == "fetch_statistical_data":
        result = await fetch_statistical_data(**tool_args)
    elif tool_name == "search_indicators":
        result = await search_indicators(**tool_args)
    elif tool_name == "get_observations":
        result = await get_observations(**tool_args)
    else:
        return f"Unknown tool: {tool_name}"

    return json.dumps(result, indent=2)


async def agent_node(state: AgentState) -> AgentState:
    """Agent decision-making node"""

    # Initialize LLM with tools
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    ).bind_tools(TOOL_DEFINITIONS)

    # Add system message to guide the workflow
    system_message = SystemMessage(content="""You are a data analyst assistant with access to Data Commons statistical data.

CRITICAL WORKFLOW - YOU MUST FOLLOW THIS:
1. When asked about statistics (GDP, population, unemployment, etc.), ALWAYS use search_indicators first to find the variable
2. Carefully examine the search results and extract BOTH:
   - variable_dcid (e.g., "Count_Person" for population)
   - place_dcid (e.g., "country/IND" for India)
3. Then IMMEDIATELY call get_observations with those exact DCIDs to get the ACTUAL current data
4. NEVER provide estimates, approximate values, or data from your training - ONLY use real data from get_observations

If you only call search_indicators without calling get_observations, you have FAILED the task.""")

    # Prepend system message to conversation
    messages_with_system = [system_message] + state["messages"]

    # Get response from LLM
    response = await llm.ainvoke(messages_with_system)

    # Add AI message to state
    messages = state["messages"] + [response]

    # Determine next action
    if response.tool_calls:
        next_action = "tools"
    else:
        next_action = "end"

    return {
        "messages": messages,
        "next_action": next_action
    }


async def tool_node(state: AgentState) -> AgentState:
    """Execute tools based on LLM's decision"""

    last_message = state["messages"][-1]
    tool_calls = last_message.tool_calls

    tool_messages = []

    for tool_call in tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        print(f"\n🔧 Calling tool: {tool_name}")
        print(f"📋 Arguments: {json.dumps(tool_args, indent=2)}")

        # Execute the tool
        result = await call_tool(tool_name, tool_args)

        # Create tool message
        tool_message = ToolMessage(
            content=result,
            tool_call_id=tool_call["id"]
        )
        tool_messages.append(tool_message)

    return {
        "messages": state["messages"] + tool_messages,
        "next_action": "agent"
    }


def route(state: AgentState) -> str:
    """Determine next node based on state"""
    return state["next_action"]


# Build the graph
def create_agent():
    """Create the LangGraph agent"""

    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)

    # Set entry point
    workflow.set_entry_point("agent")

    # Add edges
    workflow.add_conditional_edges(
        "agent",
        route,
        {
            "tools": "tools",
            "end": END
        }
    )

    workflow.add_conditional_edges(
        "tools",
        route,
        {
            "agent": "agent",
            "end": END
        }
    )

    return workflow.compile()


async def run_query(query: str):
    """Run a query through the agent"""

    print(f"\n{'='*80}")
    print(f"🤔 User Query: {query}")
    print(f"{'='*80}\n")

    # Create initial state
    initial_state = {
        "messages": [HumanMessage(content=query)],
        "next_action": "agent"
    }

    # Create and run agent
    agent = create_agent()

    # Run the agent with increased recursion limit
    final_state = await agent.ainvoke(
        initial_state,
        config={"recursion_limit": 50}
    )

    # Get the final response
    final_message = final_state["messages"][-1]

    print(f"\n{'='*80}")
    print(f"🤖 Agent Response:")
    print(f"{'='*80}")
    print(final_message.content)
    print(f"{'='*80}\n")

    return final_message.content


async def main():
    """Main function"""

    print("Data Commons LangGraph Agent")
    print("="*80)
    print("This agent can answer questions using Data Commons data.")
    print("Make sure the MCP server is running: docker ps")
    print("="*80)

    # Example queries
    queries = [
        "What is the GDP of United States, China, and India?",
        "Compare the population of California, Texas, and Florida",
        "What health indicators are available for Kenya?"
    ]

    print("\n📝 Example Queries:")
    for i, q in enumerate(queries, 1):
        print(f"{i}. {q}")

    # Interactive mode
    print("\n" + "="*80)
    print("Interactive Mode - Enter your questions (or 'quit' to exit)")
    print("="*80)

    while True:
        try:
            query = input("\n💭 Your question: ").strip()

            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break

            if not query:
                continue

            # Run the query
            await run_query(query)

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())


