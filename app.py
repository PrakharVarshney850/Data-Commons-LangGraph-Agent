"""
Streamlit Frontend for Data Commons LangGraph Agent

A beautiful web interface for querying statistical data from Data Commons.
Run with: streamlit run app.py
"""

import streamlit as st
import asyncio
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict
import re

# Import the agent
from agent import create_agent, AgentState
from langchain_core.messages import HumanMessage

# Page configuration
st.set_page_config(
    page_title="Data Commons Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling (theme-aware)
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        margin-bottom: 2rem;
        opacity: 0.8;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "tool_calls" not in st.session_state:
    st.session_state.tool_calls = []

if "show_debug" not in st.session_state:
    st.session_state.show_debug = False


# Example queries categorized
EXAMPLE_QUERIES = {
    "📊 Population": [
        "What is the population of India?",
        "Compare the population of California and Texas",
        "What is the population trend of China over the years?"
    ],
    "💰 Economy": [
        "What is the GDP of United States?",
        "Compare GDP of USA, China, and India",
        "What is the unemployment rate in Germany?"
    ],
    "🏥 Health": [
        "What health indicators are available for Kenya?",
        "What is the life expectancy in Japan?",
        "Compare infant mortality rates across countries"
    ],
    "🌍 Demographics": [
        "What is the median age in South Korea?",
        "Compare poverty rates in different states",
        "What are the education statistics for Brazil?"
    ]
}


def extract_numerical_data(text: str) -> List[Dict]:
    """Extract numerical data from agent response for visualization"""
    data_points = []

    # Pattern: "Location: Number" or "Location has Number"
    patterns = [
        r'\*\*([^*]+)\*\*:\s*([0-9,.$]+)',  # **California**: 39,431,263
        r'([A-Za-z\s]+):\s*\$?([0-9,.$]+)',  # California: 39,431,263
        r'([A-Za-z\s]+)\s+is\s+\$?([0-9,.$]+)',  # California is 39,431,263
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            location = match[0].strip()
            value_str = match[1].replace(',', '').replace('$', '')
            try:
                value = float(value_str)
                data_points.append({"location": location, "value": value})
            except:
                pass

    return data_points


def create_visualization(data_points: List[Dict], title: str = "Data Comparison"):
    """Create a bar chart from extracted data"""
    if not data_points or len(data_points) < 2:
        return None

    df = pd.DataFrame(data_points)

    fig = go.Figure(data=[
        go.Bar(
            x=df['location'],
            y=df['value'],
            marker_color='#1f77b4',
            text=df['value'].apply(lambda x: f"{x:,.0f}"),
            textposition='auto',
        )
    ])

    fig.update_layout(
        title=title,
        xaxis_title="Location",
        yaxis_title="Value",
        template="plotly_white",
        height=400,
        showlegend=False
    )

    return fig


async def query_agent(user_query: str):
    """Query the agent and return response"""

    # Create initial state
    initial_state = {
        "messages": [HumanMessage(content=user_query)],
        "next_action": "agent"
    }

    # Create and run agent
    agent = create_agent()

    # Store tool calls
    tool_calls_log = []

    # Run the agent
    final_state = await agent.ainvoke(
        initial_state,
        config={"recursion_limit": 50}
    )

    # Extract tool calls from messages
    for msg in final_state["messages"]:
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            for tool_call in msg.tool_calls:
                tool_calls_log.append({
                    "name": tool_call["name"],
                    "args": tool_call["args"]
                })

    # Get final response
    final_message = final_state["messages"][-1]

    return final_message.content, tool_calls_log


def display_tool_calls(tool_calls: List[Dict]):
    """Display tool calls in a nice format"""
    if not tool_calls:
        return

    with st.expander(f"🔧 Tool Calls ({len(tool_calls)})", expanded=st.session_state.show_debug):
        for i, tool_call in enumerate(tool_calls, 1):
            st.markdown(f"**#{i} `{tool_call['name']}`**")
            st.code(json.dumps(tool_call['args'], indent=2), language="json")


# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Settings")

    st.session_state.show_debug = st.checkbox(
        "Show debug info",
        value=st.session_state.show_debug,
        help="Display tool calls and internal processing"
    )

    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.tool_calls = []
        st.rerun()

    st.markdown("---")

    # MCP Server Status
    st.markdown("### 🌐 MCP Server")
    st.info("**Status:** Running on port 8889")
    st.caption("Make sure Docker container is running")

    st.markdown("---")

    # Example Queries
    st.markdown("### 💡 Example Queries")

    for category, queries in EXAMPLE_QUERIES.items():
        st.markdown(f"**{category}**")
        for query in queries:
            if st.button(query, key=query, use_container_width=True):
                st.session_state.example_query = query
                st.rerun()


# Main content
st.markdown('<div class="main-header">📊 Data Commons Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Query global statistical data with AI-powered natural language</div>', unsafe_allow_html=True)

# Info cards
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Data Sources", "1,346 Topics", "8,444 Variables")

with col2:
    st.metric("Conversation Messages", len(st.session_state.messages))

with col3:
    st.metric("Total Queries", len([m for m in st.session_state.messages if m["role"] == "user"]))

st.markdown("---")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Show visualization if available
        if "data_points" in message and message["data_points"]:
            fig = create_visualization(message["data_points"], "Data Comparison")
            if fig:
                st.plotly_chart(fig, use_container_width=True)

        # Show tool calls if in debug mode
        if "tool_calls" in message and message["tool_calls"]:
            display_tool_calls(message["tool_calls"])

# Chat input at the bottom (using form to keep it visible)
st.markdown("---")

# Handle example query from sidebar
if "example_query" in st.session_state:
    user_input = st.session_state.example_query
    del st.session_state.example_query
    process_query = True
else:
    # Use columns to create a better input layout
    col1, col2 = st.columns([6, 1])

    with col1:
        user_input = st.text_input(
            "Ask a question",
            placeholder="Ask me about population, GDP, health data, and more...",
            label_visibility="collapsed",
            key="user_query_input"
        )

    with col2:
        send_button = st.button("Send 🚀", use_container_width=True, type="primary")

    process_query = send_button and user_input

# Process user input
if process_query and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking and fetching data..."):
            try:
                # Run async query
                response, tool_calls = asyncio.run(query_agent(user_input))

                # Display response
                st.markdown(response)

                # Extract and visualize data
                data_points = extract_numerical_data(response)
                if data_points and len(data_points) >= 2:
                    fig = create_visualization(data_points, "Data Comparison")
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)

                # Show tool calls if debug mode
                if tool_calls:
                    display_tool_calls(tool_calls)

                # Add to message history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "tool_calls": tool_calls,
                    "data_points": data_points
                })

                # Clear the input and refresh
                if "user_query_input" in st.session_state:
                    del st.session_state.user_query_input
                st.rerun()

            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "tool_calls": [],
                    "data_points": []
                })

                # Clear the input and refresh
                if "user_query_input" in st.session_state:
                    del st.session_state.user_query_input
                st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    Built with LangGraph + Data Commons MCP Server |
    <a href="https://datacommons.org" target="_blank">Data Commons</a> |
    <a href="https://github.com/langchain-ai/langgraph" target="_blank">LangGraph</a>
</div>
""", unsafe_allow_html=True)
