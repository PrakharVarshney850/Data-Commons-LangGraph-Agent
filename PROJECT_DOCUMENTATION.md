# Data Commons LangGraph Agent - Complete Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [What is This Project?](#what-is-this-project)
3. [How It Works](#how-it-works)
4. [Project Architecture](#project-architecture)
5. [Technologies Used](#technologies-used)
6. [Installation Guide](#installation-guide)
7. [Usage Guide](#usage-guide)
8. [File Structure](#file-structure)
9. [Troubleshooting](#troubleshooting)
10. [Future Enhancements](#future-enhancements)

---

## Project Overview

### What is This Project?

This project is an **AI-powered question-answering system** that can answer questions about real-world statistical data like GDP, population, unemployment rates, and much more.

Think of it as a smart assistant that can:
- Answer questions like "What is the GDP of United States?"
- Compare data: "Compare the population of California and Texas"
- Find information: "What health data is available for Africa?"

The system uses **real, verified data** from Google's Data Commons database instead of making up answers, which makes it very reliable for research and analysis.

### The Problem It Solves

Traditional AI chatbots sometimes "hallucinate" or make up facts. This project solves that by:
1. Connecting to a **real database** (Data Commons) with verified statistics
2. Using an **intelligent agent** (LangGraph) that knows how to search and retrieve data
3. Providing **accurate, sourced information** backed by real data

---

## How It Works

### Simple Explanation

Imagine you have three components:

1. **You (The User)**: Ask questions in plain English
2. **The Agent (LangGraph)**: A smart AI that understands your question and knows how to find data
3. **The Data Source (Data Commons MCP Server)**: A database with millions of statistics about the world

**The Flow:**
```
You ask: "What is the population of California?"
    ↓
Agent thinks: "I need to search for population data for California"
    ↓
Agent asks Data Commons: "Search for population indicator for California"
    ↓
Data Commons responds: "Here's the population variable ID"
    ↓
Agent asks Data Commons: "Get me the latest population data using that ID"
    ↓
Data Commons responds: "California population is 39.5 million (2023)"
    ↓
Agent tells you: "The population of California is approximately 39.5 million people."
```

### Technical Explanation

The system uses:

1. **MCP (Model Context Protocol)**: A standardized way for AI systems to access external data sources
2. **LangGraph**: A framework for building AI agents that can use tools and make decisions
3. **Data Commons**: Google's public dataset with millions of statistical variables
4. **Docker**: Containers to run the MCP server reliably

---

## Project Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                │
│                    (Asks Questions)                         │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   LANGGRAPH AGENT                           │
│                   (agent.py)                                │
│                                                             │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Agent     │───▶│   Tools      │───▶│   Response   │  │
│  │   Node      │    │   Node       │    │   Generator  │  │
│  └─────────────┘    └──────────────┘    └──────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼ (HTTP Requests)
┌─────────────────────────────────────────────────────────────┐
│              DATA COMMONS MCP SERVER                        │
│              (Running in Docker)                            │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────┐               │
│  │ search_indicators│  │ get_observations │               │
│  │                  │  │                  │               │
│  │ Finds variables  │  │ Gets actual data │               │
│  └──────────────────┘  └──────────────────┘               │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼ (API Calls)
┌─────────────────────────────────────────────────────────────┐
│              GOOGLE DATA COMMONS API                        │
│         (Millions of statistical variables)                 │
│                                                             │
│  GDP, Population, Health, Economics, Climate, etc.          │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Input** → Text question (e.g., "What is GDP of USA?")
2. **Agent Processing** → Analyzes question, plans tool calls
3. **MCP Server** → Searches for relevant data variables
4. **Data Commons API** → Returns actual statistical data
5. **Agent Response** → Formats answer in natural language
6. **User Output** → Receives answer

---

## Technologies Used

### 1. **LangGraph** (AI Agent Framework)
- **What**: Framework for building AI agents with decision-making capabilities
- **Why**: Allows the agent to think, plan, and use tools autonomously
- **Version**: 0.6.10

### 2. **LangChain** (LLM Framework)
- **What**: Framework for building applications with Large Language Models
- **Why**: Provides tools to connect OpenAI's GPT with our custom tools
- **Version**: 0.3.27

### 3. **OpenAI GPT-4** (Language Model)
- **What**: Advanced AI model that understands and generates human language
- **Why**: Powers the agent's natural language understanding and reasoning
- **Model**: gpt-4o-mini

### 4. **Data Commons MCP Server** (Data Source)
- **What**: Server that exposes Data Commons data through MCP protocol
- **Why**: Provides standardized access to millions of statistical variables
- **Protocol**: MCP (Model Context Protocol)

### 5. **Docker** (Containerization)
- **What**: Platform for running applications in isolated containers
- **Why**: Ensures MCP server runs consistently across different systems
- **Version**: Latest

### 6. **Python** (Programming Language)
- **What**: High-level programming language
- **Why**: Excellent ecosystem for AI/ML and data processing
- **Version**: 3.12

---

## Installation Guide

### Prerequisites

Before you start, you need:
- **Docker Desktop** installed and running
- **Python 3.12** or higher
- **OpenAI API Key** (from https://platform.openai.com/api-keys)
- **Data Commons API Key** (already provided in .env file)

### Step 1: Verify Prerequisites

```bash
# Check Docker is installed
docker --version
# Should show: Docker version 20.x.x or higher

# Check Python is installed
python --version
# Should show: Python 3.12.x

# Check Docker is running
docker ps
# Should show running containers (or empty list)
```

### Step 2: Set Up Environment

```bash
# Navigate to project directory
cd /path/to/Data_Common_Agent

# Create Python virtual environment (if not exists)
python -m venv .venv

# Activate virtual environment
# On Windows:
.\.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### Step 3: Configure API Keys

Edit the `.env` file:
```
DC_API_KEY=pF84J3x4L7C1PTLnvp0EXsA7ebtmmVXu0mO9ODRfmA9q6MMa0DglA0Grx8WghTFh
OPENAI_API_KEY=your-openai-api-key-here
```

**Important**: Replace `your-openai-api-key-here` with your actual OpenAI API key.

### Step 4: Build and Run MCP Server

```bash
# Build Docker image
docker build -t datacommons-mcp .

# Run MCP server
docker run -d -p 8889:8889 --name datacommons-mcp datacommons-mcp

# Verify it's running
docker logs datacommons-mcp
# Should see: "Uvicorn running on http://0.0.0.0:8889"
```

### Step 5: Test the Agent

```python
# Create a test file: test.py
from agent import run_query
import asyncio

async def main():
    result = await run_query("What is the population of California?")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

```bash
# Run the test
python test.py
```

---

## Usage Guide

### Running the Agent Interactively

```bash
# Activate virtual environment
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Run the agent
python agent.py
```

You'll see:
```
Data Commons LangGraph Agent
================================================================================
This agent can answer questions using Data Commons data.
Make sure the MCP server is running: docker ps
================================================================================

📝 Example Queries:
1. What is the GDP of United States, China, and India?
2. Compare the population of California, Texas, and Florida
3. What health indicators are available for Kenya?

================================================================================
Interactive Mode - Enter your questions (or 'quit' to exit)
================================================================================

💭 Your question:
```

### Example Queries

**Economics:**
- "What is the GDP of United States?"
- "Compare the GDP of USA, China, and India"
- "Show me unemployment rates for European countries"

**Demographics:**
- "What is the population of California?"
- "Compare population growth in Texas and Florida"
- "Show me population density for Asian countries"

**Health:**
- "What health indicators are available for Kenya?"
- "Compare life expectancy in developed vs developing countries"

**Climate:**
- "What climate data is available for South America?"
- "Show me CO2 emissions by country"

### Programmatic Usage

```python
import asyncio
from agent import run_query

async def main():
    # Single query
    result = await run_query("What is the GDP of USA?")
    print(result)

    # Multiple queries
    queries = [
        "Population of California",
        "Unemployment rate in India",
        "GDP of China"
    ]

    for query in queries:
        result = await run_query(query)
        print(f"Query: {query}")
        print(f"Answer: {result}\n")

asyncio.run(main())
```

---

## File Structure

```
Data_Common_Agent/
│
├── .env                    # API keys (KEEP SECRET!)
│   └── DC_API_KEY         # Data Commons API key
│   └── OPENAI_API_KEY     # OpenAI API key
│
├── .dockerignore          # Files to exclude from Docker build
├── .venv/                 # Python virtual environment (auto-generated)
│
├── Dockerfile             # Docker configuration for MCP server
│   └── Builds the MCP server container
│
├── requirements.txt       # Python dependencies
│   └── langgraph          # AI agent framework
│   └── langchain          # LLM framework
│   └── langchain-openai   # OpenAI integration
│   └── httpx              # HTTP client for API calls
│   └── python-dotenv      # Environment variable loader
│
├── agent.py              # Main agent code (THE CORE)
│   └── MCPClient         # Communicates with MCP server
│   └── search_indicators  # Searches for data variables
│   └── get_observations   # Fetches actual data
│   └── create_agent       # Builds the LangGraph agent
│   └── run_query          # Runs queries through the agent
│
├── cleanup.sh            # Unix cleanup script
└── cleanup.bat           # Windows cleanup script
```

### Important Files Explained

**`.env`**
- Stores sensitive API keys
- **NEVER** commit to Git or share publicly
- Required for both MCP server and OpenAI access

**`Dockerfile`**
- Instructions to build the MCP server container
- Installs `uv` package manager
- Exposes port 8889 for HTTP communication
- Runs `datacommons-mcp serve http`

**`requirements.txt`**
- Lists all Python dependencies with versions
- Install with: `pip install -r requirements.txt`

**`agent.py`**
- Main application code
- Contains all the AI agent logic
- See AGENT_CODE_EXPLANATION.md for detailed explanation

---

## Troubleshooting

### Problem: Docker container exits immediately

**Symptoms:**
```bash
docker ps -a
# Shows: Exited (1) 2 seconds ago
```

**Solution:**
```bash
# Check logs
docker logs datacommons-mcp

# Common issue: Missing API key
# Fix: Add DC_API_KEY to .env file

# Restart
docker stop datacommons-mcp
docker rm datacommons-mcp
docker run -d -p 8889:8889 --name datacommons-mcp datacommons-mcp
```

### Problem: Agent can't connect to MCP server

**Symptoms:**
```
Error: Connection refused
```

**Solution:**
```bash
# Verify MCP server is running
docker ps | grep datacommons-mcp

# Check port is accessible
curl http://localhost:8889/mcp
# Should return error 406 (this is normal - MCP requires special headers)

# Restart MCP server if needed
docker restart datacommons-mcp
```

### Problem: OpenAI API errors

**Symptoms:**
```
Error: Invalid API key
Error: Rate limit exceeded
```

**Solution:**
```bash
# Verify API key in .env
cat .env | grep OPENAI_API_KEY

# Check OpenAI account has credits
# Visit: https://platform.openai.com/account/usage

# Use correct API key format
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```

### Problem: Unicode/Encoding errors on Windows

**Symptoms:**
```
UnicodeEncodeError: 'charmap' codec can't encode character
```

**Solution:**
This is already fixed in agent.py with UTF-8 encoding setup.
If you still see errors:
```bash
# Set environment variable before running
set PYTHONIOENCODING=utf-8
python agent.py
```

### Problem: Recursion limit exceeded

**Symptoms:**
```
GraphRecursionError: Recursion limit of 25 reached
```

**Solution:**
This is already fixed in agent.py (recursion_limit=50).
If you need more:
```python
# In agent.py, increase the limit:
final_state = await agent.ainvoke(
    initial_state,
    config={"recursion_limit": 100}  # Increase this number
)
```

---

## Future Enhancements

### Planned Features

1. **Web Interface**
   - Build a web UI using Streamlit or Gradio
   - Allow users to interact through browser
   - Visualize data with charts and graphs

2. **Data Caching**
   - Cache frequently requested data
   - Reduce API calls and improve speed
   - Store results in local database

3. **Multi-Agent System**
   - Create specialized agents for different domains
   - Economics agent, health agent, climate agent
   - Coordinate between agents for complex queries

4. **Voice Interface**
   - Add speech-to-text input
   - Text-to-speech output
   - Create voice-activated assistant

5. **Data Export**
   - Export results to CSV, Excel, PDF
   - Generate reports with visualizations
   - Schedule automated data updates

6. **Advanced Analytics**
   - Trend analysis and forecasting
   - Comparative analysis across regions
   - Statistical significance testing

### Contributing

If you want to contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## Security Best Practices

### API Key Security

1. **Never commit .env file to Git**
   ```bash
   # Add to .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use environment variables in production**
   ```bash
   # Instead of .env file, use system environment variables
   export DC_API_KEY="your-key"
   export OPENAI_API_KEY="your-key"
   ```

3. **Rotate keys regularly**
   - Change API keys every 3-6 months
   - Immediately rotate if compromised

4. **Use separate keys for development and production**
   - Dev key with rate limits
   - Production key with monitoring

### Docker Security

1. **Don't run as root in containers**
   - Already configured in Dockerfile
   - Uses non-privileged user

2. **Keep images updated**
   ```bash
   docker pull python:3.12-slim
   docker build -t datacommons-mcp .
   ```

3. **Scan for vulnerabilities**
   ```bash
   docker scout quickview datacommons-mcp
   ```

---

## Performance Optimization

### Tips for Better Performance

1. **Use connection pooling**
   - Already implemented in httpx AsyncClient
   - Reuses HTTP connections

2. **Implement caching**
   ```python
   from functools import lru_cache

   @lru_cache(maxsize=128)
   def cached_query(query):
       # Cache results
       pass
   ```

3. **Batch queries**
   - Group similar queries together
   - Reduce API calls

4. **Monitor usage**
   ```bash
   # Check Docker resource usage
   docker stats datacommons-mcp
   ```

---

## Frequently Asked Questions

**Q: How much does it cost to run this?**
A: Main cost is OpenAI API usage (~$0.001 per query with gpt-4o-mini). Data Commons is free.

**Q: Can I use this offline?**
A: No, requires internet for OpenAI API and Data Commons API.

**Q: What data is available in Data Commons?**
A: 250+ billion data points covering economics, demographics, health, climate, and more.

**Q: Can I add my own data sources?**
A: Yes! Create custom MCP tools or modify existing ones.

**Q: Is this production-ready?**
A: It's a prototype. For production, add error handling, monitoring, and security hardening.

**Q: How accurate is the data?**
A: Data comes from authoritative sources (World Bank, UN, CDC, etc.) but verify critical information.

---

## Resources

### Documentation
- [Data Commons API Docs](https://docs.datacommons.org/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [MCP Protocol Spec](https://modelcontextprotocol.io/)
- [OpenAI API Docs](https://platform.openai.com/docs)

### Learning Materials
- [LangChain Tutorials](https://python.langchain.com/docs/tutorials/)
- [Docker Getting Started](https://docs.docker.com/get-started/)
- [Python Async Programming](https://docs.python.org/3/library/asyncio.html)

### Community
- [LangChain Discord](https://discord.gg/langchain)
- [Data Commons Google Group](https://groups.google.com/g/datacommons)

---

## License

This project uses:
- Data Commons: Apache 2.0 License
- LangChain: MIT License
- OpenAI: Commercial API (paid usage)

**Your code**: Choose your own license (MIT, Apache, etc.)

---

## Support

For issues or questions:
1. Check this documentation
2. Review error messages carefully
3. Search existing issues on GitHub
4. Create new issue with detailed description

**Include in bug reports:**
- Error message
- Steps to reproduce
- Docker logs: `docker logs datacommons-mcp`
- Python version, OS, Docker version

---

## Acknowledgments

- **Google Data Commons** - For providing free access to world data
- **LangChain Team** - For LangGraph framework
- **OpenAI** - For GPT models
- **Anthropic** - For Claude (used in development)

---

**Last Updated**: October 16, 2025
**Version**: 1.0.0
**Author**: Your Name
**Contact**: your.email@example.com
