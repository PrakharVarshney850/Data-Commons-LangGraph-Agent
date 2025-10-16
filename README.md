# 📊 Data Commons LangGraph Agent

A powerful AI agent that queries global statistical data from Data Commons using natural language, built with LangGraph and featuring a beautiful Streamlit web interface.

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.50+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 🤖 **AI-Powered Agent** - Uses GPT-4o-mini with LangGraph for intelligent query processing
- 📊 **Real Data** - Fetches actual statistics from Data Commons (1,346 topics, 8,444 variables)
- 🎨 **Beautiful UI** - Professional Streamlit interface with dark mode support
- 📈 **Auto Visualization** - Automatic chart generation for comparison queries
- 🔧 **Debug Mode** - See exactly what the agent does behind the scenes
- 💡 **Example Queries** - Quick-start buttons for common questions
- 🐳 **Docker Support** - MCP server runs in isolated container

## 🎯 What Can It Do?

Ask questions in natural language about:

- **Population**: "What is the population of India?"
- **Economy**: "Compare GDP of USA, China, and India"
- **Health**: "What is the life expectancy in Japan?"
- **Demographics**: "Compare poverty rates in California and Texas"
- **Trends**: "What is the population trend of China over the years?"

The agent automatically:
1. Searches for relevant indicators
2. Extracts the correct data identifiers
3. Fetches real-time statistical data
4. Presents results with visualizations

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Docker Desktop
- OpenAI API key
- Data Commons API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/PrakharVarshney850/Data-Commons-LangGraph-Agent.git
   cd Data-Commons-LangGraph-Agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # Mac/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy example file
   cp .env.example .env

   # Edit .env and add your API keys
   # DC_API_KEY=your_key_here
   # OPENAI_API_KEY=your_key_here
   ```

5. **Start MCP server (Docker)**
   ```bash
   docker build -t datacommons-mcp .
   docker run -d --name datacommons-mcp -p 8889:8889 datacommons-mcp
   ```

6. **Launch Streamlit app**
   ```bash
   streamlit run app.py
   ```

7. **Open browser**
   - Navigate to `http://localhost:8501`
   - Start asking questions!

## 📖 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Get running in 30 seconds
- **[README_FRONTEND.md](README_FRONTEND.md)** - Complete Streamlit guide
- **[PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)** - Full project overview
- **[AGENT_CODE_EXPLANATION.md](AGENT_CODE_EXPLANATION.md)** - Line-by-line code explanation

## 📁 Project Structure

```
Data_Common_Agent/
├── agent.py                    # Core LangGraph agent
├── app.py                      # Streamlit frontend
├── requirements.txt            # Python dependencies
├── Dockerfile                  # MCP server container
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
├── QUICK_START.md              # Quick start guide
├── README_FRONTEND.md          # Frontend documentation
├── PROJECT_DOCUMENTATION.md    # Project overview
└── AGENT_CODE_EXPLANATION.md   # Code explanation
```

## 🎨 Streamlit Interface

### Main Features

- **Chat Interface** - Conversational UI with message history
- **Auto Charts** - Bar charts for comparison queries
- **Debug Mode** - View tool calls and DCIDs
- **Example Queries** - Categorized by topic
- **Session Stats** - Track messages and queries
- **Dark Mode** - Full theme support

### Screenshots

The interface includes:
- Sidebar with settings and examples
- Main chat area with responses
- Automatic data visualizations
- Tool call transparency
- Clean input box at bottom

## 🔧 How It Works

### Architecture

```
User Query → Streamlit UI → LangGraph Agent → OpenAI GPT-4o-mini
                                    ↓
                            Tool Execution
                                    ↓
                        MCP Server (Docker) → Data Commons API
                                    ↓
                            Real Data ← Response
```

### Two-Step Workflow

1. **search_indicators** - Find relevant variables and places
2. **get_observations** - Fetch actual statistical values

The agent intelligently handles:
- DCID extraction from search results
- Multiple comparisons (California vs Texas)
- Historical trends (all years data)
- Child place types (states, counties)

## 🛠️ Technologies

- **[LangGraph](https://github.com/langchain-ai/langgraph)** - Agent framework
- **[LangChain](https://github.com/langchain-ai/langchain)** - LLM orchestration
- **[OpenAI](https://openai.com/)** - GPT-4o-mini for reasoning
- **[Data Commons](https://datacommons.org/)** - Statistical data source
- **[Streamlit](https://streamlit.io/)** - Web interface
- **[Plotly](https://plotly.com/)** - Interactive charts
- **[Docker](https://docker.com/)** - MCP server containerization

## 📊 Data Sources

The agent has access to Data Commons data including:

- **1,346 Topics** covering various domains
- **8,444 Variables** with statistical indicators
- **Global Coverage** - Countries, states, cities
- **Historical Data** - Multi-year trends
- **Real-Time** - Latest available statistics

Data types include:
- Population & Demographics
- Economic Indicators (GDP, Unemployment)
- Health Statistics
- Education Metrics
- Climate & Environment
- And much more!

## 🐛 Troubleshooting

### MCP Server Issues

```bash
# Check if container is running
docker ps | grep datacommons-mcp

# View logs
docker logs datacommons-mcp

# Restart container
docker restart datacommons-mcp
```

### Frontend Issues

```bash
# Clear Streamlit cache
streamlit cache clear

# Run with debug logging
streamlit run app.py --logger.level=debug
```

### Common Errors

- **"I/O operation on closed file"** - Fixed in latest version
- **"Port already in use"** - Change port or kill existing process
- **"Module not found"** - Activate venv and reinstall dependencies

See [README_FRONTEND.md](README_FRONTEND.md) for detailed troubleshooting.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Data Commons](https://datacommons.org/) for providing amazing statistical data
- [LangChain](https://langchain.com/) and [LangGraph](https://github.com/langchain-ai/langgraph) for the agent framework
- [Streamlit](https://streamlit.io/) for the beautiful web framework
- [OpenAI](https://openai.com/) for GPT-4o-mini

## 📞 Support

- **Documentation**: See the docs/ folder
- **Issues**: [GitHub Issues](https://github.com/PrakharVarshney850/Data-Commons-LangGraph-Agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/PrakharVarshney850/Data-Commons-LangGraph-Agent/discussions)

## 🌟 Star This Repo!

If you find this project helpful, please give it a star ⭐️

---

**Built with ❤️ using LangGraph, Streamlit, and Data Commons**
