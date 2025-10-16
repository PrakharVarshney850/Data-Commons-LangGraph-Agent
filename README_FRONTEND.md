# 🎨 Streamlit Frontend User Guide

Complete guide for the Data Commons Agent Streamlit interface.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Features](#features)
5. [Customization](#customization)
6. [Troubleshooting](#troubleshooting)
7. [Deployment](#deployment)

---

## 🎯 Overview

The Streamlit frontend provides a beautiful, professional web interface for querying Data Commons statistical data using natural language.

### Key Highlights

- ✨ **Beautiful UI** - Professional chat interface with modern design
- 📊 **Auto Visualization** - Automatic chart generation for comparisons
- 🔧 **Transparency** - See exactly what the agent does (debug mode)
- 💡 **Quick Start** - One-click example queries organized by category
- 📈 **Statistics** - Track your session and usage
- ⚙️ **Configurable** - Customize colors, themes, and behavior

---

## 💾 Installation

### Prerequisites

1. **Python 3.12+** installed
2. **Docker** running with datacommons-mcp container
3. **Virtual environment** set up

### Install Dependencies

```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Install frontend dependencies
pip install -r requirements.txt
```

This installs:
- `streamlit` - Web framework
- `plotly` - Interactive charts
- `pandas` - Data handling

### Verify Installation

```bash
streamlit --version
# Should show: Streamlit, version 1.50.0 or higher
```

---

## 🎮 Usage

### Basic Usage

```bash
streamlit run app.py
```

Your browser opens automatically to **http://localhost:8501**

### Advanced Options

```bash
# Custom port
streamlit run app.py --server.port 8502

# Auto-reload on save
streamlit run app.py --server.runOnSave true

# Headless mode (no auto-open browser)
streamlit run app.py --server.headless true

# Custom address
streamlit run app.py --server.address 0.0.0.0
```

---

## ✨ Features

### 1. Chat Interface

**Clean conversational UI:**
- User messages on the right
- AI responses on the left with avatar
- Auto-scroll to latest message
- Message history preserved during session

**Example:**
```
You: What is the population of India?
Agent: The current population of India is approximately
       1,450,935,791 (about 1.45 billion) as of 2024.
```

---

### 2. Automatic Data Visualization

When you ask comparison questions, charts appear automatically!

**Supported queries:**
- "Compare the population of California and Texas"
- "What's the GDP of USA, China, and India?"
- "Compare poverty rates in different states"

**Chart features:**
- Interactive Plotly bar charts
- Hover to see exact values
- Responsive design
- Professional styling

**Example output:**
```
Text Response:
• California: 39,431,263
• Texas: 31,290,831

[Bar Chart]
California: ████████████████████ 39.4M
Texas:      ████████████ 31.3M
```

---

### 3. Tool Call Transparency (Debug Mode)

**Enable in sidebar:** Toggle "Show debug info"

**What you'll see:**
```
🔧 Tool Calls (2)

  #1 search_indicators
     {
       "query": "population",
       "places": ["India"]
     }

  #2 get_observations
     {
       "variable_dcid": "Count_Person",
       "place_dcid": "country/IND",
       "date": "latest"
     }
```

**Why it's useful:**
- Learn how the agent works
- Debug issues
- Understand the two-step workflow
- See exact parameters used

---

### 4. Example Query Buttons

**Sidebar organized by category:**

**📊 Population:**
- What is the population of India?
- Compare the population of California and Texas
- What is the population trend of China?

**💰 Economy:**
- What is the GDP of United States?
- Compare GDP of USA, China, and India
- What is the unemployment rate in Germany?

**🏥 Health:**
- What health indicators are available for Kenya?
- What is the life expectancy in Japan?
- Compare infant mortality rates across countries

**🌍 Demographics:**
- What is the median age in South Korea?
- Compare poverty rates in different states
- What are the education statistics for Brazil?

**How to use:**
1. Browse categories in sidebar
2. Click any question
3. Query runs automatically
4. See results immediately

---

### 5. Session Statistics

**Top of page shows:**
- **Data Sources:** 1,346 Topics | 8,444 Variables
- **Conversation Messages:** Count of messages in session
- **Total Queries:** Number of user queries asked

**Resets when:**
- Clear History button clicked
- Browser refreshed
- App restarted

---

### 6. Settings Panel

**Located in sidebar:**

**Show debug info** (checkbox)
- Toggles tool call visibility
- Shows DCIDs and parameters
- Helps understand agent workflow

**Clear History** (button)
- Removes all messages
- Starts fresh conversation
- Resets statistics

**MCP Server Status** (info box)
- Shows server is running on port 8889
- Reminds to check Docker container

---

## 🐛 Troubleshooting

### Problem: Port 8501 already in use

**Error:**
```
StreamlitAddressException: Port 8501 is already in use
```

**Solution 1 - Use different port:**
```bash
streamlit run app.py --server.port 8502
```

**Solution 2 - Kill existing process (Windows):**
```bash
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

**Solution 3 - Kill existing process (Mac/Linux):**
```bash
lsof -ti:8501 | xargs kill -9
```

---

### Problem: Cannot connect to MCP server

**Error in UI:**
```
❌ Error: Connection refused
```

**Check Docker:**
```bash
docker ps | grep datacommons-mcp
```

**If not running:**
```bash
docker start datacommons-mcp
```

**Check logs:**
```bash
docker logs datacommons-mcp
# Look for: "Server running on port 8889"
```

**Verify API key:**
```bash
cat .env | grep DC_API_KEY
# Should show: DC_API_KEY=l6joiuknneHKFukNnydo2CjzOYjGb5DBXU2pl2zAkMh6xDu1
```

---

### Problem: ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution:**
```bash
# Make sure venv is activated
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

---

### Problem: Charts not displaying

**Symptoms:**
- Text response shows but no chart
- Blank space where chart should be
- "Failed to load component" error

**Solution:**
```bash
# Reinstall plotly
pip install --upgrade plotly

# Clear Streamlit cache
streamlit cache clear

# Restart Streamlit
streamlit run app.py
```

---

### Problem: Agent returns errors

**Check these:**

1. **Docker container running:**
   ```bash
   docker ps
   ```

2. **MCP server logs:**
   ```bash
   docker logs datacommons-mcp
   ```

3. **API key correct:**
   ```bash
   cat .env
   ```

4. **Test agent directly:**
   ```bash
   python -c "from agent import create_agent; print('OK')"
   ```

---

### Problem: Slow responses

**Possible causes:**
- Complex query requiring multiple tool calls
- Network latency to Data Commons API
- Large result sets

**Solutions:**
- Be patient (some queries take 10-15 seconds)
- Try simpler queries first
- Clear history if session is very long
- Check internet connection

---

## 🎨 Customization

### Change Theme

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"        # Blue accent
backgroundColor = "#FFFFFF"      # White background
secondaryBackgroundColor = "#F0F2F6"  # Light gray
textColor = "#262730"           # Dark text
font = "sans serif"             # Font family
```

**Built-in themes:**
```toml
[theme]
base = "light"  # or "dark"
```

**Restart Streamlit to see changes.**

---

### Modify Colors in Code

Edit `app.py` CSS section (around line 24-43):

```python
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #YOUR_COLOR;  # Change header color
    }
    .tool-call-box {
        background-color: #YOUR_BG;
        border-left: 4px solid #YOUR_ACCENT;
    }
</style>
""", unsafe_allow_html=True)
```

---

### Add More Example Queries

Edit `app.py` EXAMPLE_QUERIES dict (around line 66-88):

```python
EXAMPLE_QUERIES = {
    "📊 Population": [
        "What is the population of India?",
        "Your new query here",  # Add yours!
    ],
    "🌟 Your Category": [      # New category!
        "Custom query 1",
        "Custom query 2"
    ]
}
```

---

### Customize Page Config

Edit `app.py` page config (around line 19-23):

```python
st.set_page_config(
    page_title="Your Custom Title",  # Browser tab
    page_icon="🌟",                  # Browser icon
    layout="wide",                   # or "centered"
    initial_sidebar_state="expanded"  # or "collapsed"
)
```

---

### Add Custom Logo

1. **Create `static/` folder:**
   ```bash
   mkdir static
   ```

2. **Add logo file:**
   ```
   static/logo.png
   ```

3. **Display in app:**
   ```python
   # In app.py
   st.sidebar.image("static/logo.png", width=200)
   ```

---

## 🚀 Deployment

### Deploy to Streamlit Cloud (Free)

1. **Push code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Add Streamlit frontend"
   git push origin main
   ```

2. **Go to:** https://streamlit.io/cloud

3. **Sign in** with GitHub

4. **Click "New app"**

5. **Configure:**
   - Repository: your-repo
   - Branch: main
   - Main file path: app.py

6. **Add secrets:**
   - Settings → Secrets
   - Paste your .env contents
   ```toml
   DC_API_KEY = "your-key"
   OPENAI_API_KEY = "your-key"
   ```

7. **Deploy!** (takes 2-3 minutes)

**Your app gets a URL like:**
`https://your-app.streamlit.app`

---

### Deploy to Custom Server

**Using Docker:**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

**Build and run:**
```bash
docker build -t datacommons-frontend .
docker run -p 8501:8501 datacommons-frontend
```

---

### Environment Variables for Production

Create `.streamlit/secrets.toml` for production:

```toml
DC_API_KEY = "your-production-key"
OPENAI_API_KEY = "your-openai-key"
MCP_SERVER_URL = "http://your-server:8889"
```

Access in code:
```python
import streamlit as st
api_key = st.secrets["DC_API_KEY"]
```

---

## 📈 Best Practices

### Performance

1. **Use st.cache_data for expensive operations:**
   ```python
   @st.cache_data
   def load_data():
       return expensive_operation()
   ```

2. **Clear cache periodically:**
   ```bash
   streamlit cache clear
   ```

3. **Limit message history:**
   - Clear history after long sessions
   - Consider adding auto-clear after N messages

---

### Security

1. **Never commit .env file:**
   ```bash
   # Add to .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use secrets for production:**
   - Streamlit Cloud: Use Secrets management
   - Custom server: Environment variables

3. **Validate user input:**
   - Already handled by LangGraph
   - Agent has built-in safety

---

### User Experience

1. **Add loading indicators:**
   ```python
   with st.spinner("🤔 Thinking..."):
       response = query_agent(input)
   ```

2. **Show progress for long operations:**
   ```python
   progress = st.progress(0)
   # Update as task progresses
   ```

3. **Handle errors gracefully:**
   ```python
   try:
       response = query_agent(input)
   except Exception as e:
       st.error(f"Error: {e}")
       st.info("Try rephrasing your question")
   ```

---

## 💡 Tips & Tricks

### Keyboard Shortcuts

- **Send message:** Enter
- **New line in input:** Shift + Enter
- **Rerun app:** Ctrl/Cmd + R (in browser)
- **Stop app:** Ctrl + C (in terminal)

---

### Session State

Access conversation history:
```python
# In app.py
st.session_state.messages  # All messages
len(st.session_state.messages)  # Count
```

---

### Debug Mode

**Always run with debug during development:**
```bash
streamlit run app.py --logger.level=debug
```

**Check logs:**
```bash
# Logs are in:
~/.streamlit/logs/
```

---

## 🎓 Learning Resources

### Streamlit Documentation

- Official docs: https://docs.streamlit.io
- API reference: https://docs.streamlit.io/api
- Gallery: https://streamlit.io/gallery
- Forum: https://discuss.streamlit.io

### Plotly Charts

- Docs: https://plotly.com/python/
- Examples: https://plotly.com/python/plotly-express/

### Data Commons

- API docs: https://docs.datacommons.org
- Available data: https://datacommons.org/place

---

## 📞 Support

### Getting Help

1. **Check documentation:**
   - This file (README_FRONTEND.md)
   - QUICK_START.md
   - PROJECT_DOCUMENTATION.md

2. **Test components:**
   ```bash
   # Test agent
   python agent.py

   # Test MCP server
   docker logs datacommons-mcp

   # Test Streamlit
   streamlit --version
   ```

3. **Common issues:**
   - See Troubleshooting section above

---

## 🎉 Summary

Your Streamlit frontend provides:

✅ Beautiful, professional UI
✅ Automatic data visualization
✅ Tool call transparency
✅ Example queries
✅ Session statistics
✅ Full customization
✅ Easy deployment

**Launch command:**
```bash
streamlit run app.py
```

**Access at:** http://localhost:8501

---

**Happy querying! 📊✨**
