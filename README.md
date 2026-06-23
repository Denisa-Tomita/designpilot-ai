# 🎨 DesignPilot AI

An AI-powered multi-agent system that generates complete brand identities and landing page design systems for small businesses.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-green)

---

# Problem

Creating a consistent brand identity requires multiple specialized skills:

- Brand strategy
- Design research
- Color selection
- Typography pairing
- Marketing copywriting

Small businesses often lack the time or budget to hire experts for each discipline.

---

# Solution

DesignPilot AI uses a **multi-agent architecture** where each AI agent specializes in one design task while sharing the same project context.

Instead of one large prompt, specialized agents collaborate to produce a complete design system.

```
User Prompt
      │
      ▼
Planner Agent
      │
      ▼
Research Agent
      │
      ▼
Color Agent
      │
      ▼
Typography Agent
      │
      ▼
Copywriter Agent
      │
      ▼
Export Agent
```

---

# Features

- 🤖 Multi-agent architecture
- 🎨 Professional color palette generation
- 🔤 Typography recommendations
- ✍️ Landing page copy generation
- 🔍 Brand research
- 📋 Project planning
- ⚡ Local cache system to minimize Gemini API usage
- 📁 Automatic project metadata generation
- 🔒 Secure API key management

---

# Architecture

```
app.py
│
├── Planner Agent
├── Research Agent
├── Color Agent
├── Typography Agent
├── Copywriter Agent
└── Export Agent
        │
        ▼
services/gemini_client.py
        │
        ▼
Gemini 2.5 Flash API
        │
        ▼
cache.json
```

---

# Cache System

To reduce API costs and improve response times, every project is cached locally.

Project names are normalized:

```
Luxury Coffee Shop

LUXURY COFFEE SHOP

luxury    coffee    shop
```

↓

```
luxury coffee shop
```

Cache structure:

```json
{
  "luxury coffee shop": {
    "created_at": "...",
    "planner": "...",
    "research": "...",
    "color": "...",
    "typography": "...",
    "copywriter": "..."
  }
}
```

Repeated requests are served directly from the cache without calling Gemini.

---

# Project Structure

```
designpilot-ai/

agents/
    __init__.py
    planner.py
    research.py
    colors.py
    typography.py
    copywriter.py
    exporter.py

services/
    gemini_client.py

app.py
cache.json
requirements.txt
README.md
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/Denisa-Tomita/designpilot-ai.git
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```
GEMINI_MODEL=model_here
GEMINI_API_KEY=your_api_key_here
```

Run the application:

```bash
streamlit run app.py
```

---

# Security

The project follows several security best practices:

- API keys stored in environment variables
- `.env` excluded from Git
- `.env.example` included for setup
- Local cache contains generated content only
- Prompt normalization prevents duplicate API requests

---

# Technologies

- Python 3.12
- Streamlit
- Google Gemini
- python-dotenv
- JSON local cache

---

# Future Improvements

- Export Brand Guide as Markdown/PDF
- MCP Filesystem integration
- Antigravity integration
- Multi-agent orchestration with Google ADK
- Docker deployment
- Semantic cache search

---

# Demo

Describe a business idea:

```
Luxury coffee shop in Porto
```

DesignPilot AI generates:

- Brand strategy
- Market research
- Professional color palette
- Typography pairing
- Landing page copy

while minimizing API usage through a persistent local cache.

---

# License

MIT License
