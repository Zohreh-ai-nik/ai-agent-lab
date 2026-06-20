# ai-agent-lab
# 🤖 AI Agent Lab

> 100+ AI Agent & RAG apps you can actually run — clone, customize, ship.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Stars](https://img.shields.io/github/stars/Zohreh-ai-nik/ai-agent-lab?style=social)](https://github.com/Zohreh-ai-nik/ai-agent-lab/stargazers)

**Works with Claude · OpenAI · Gemini · Llama · Qwen**  
AI Agents · Multi-agent Teams · MCP Agents · RAG · Voice Agents · Fine-tuning

---

## 💡 Why this exists

You shouldn't have to rebuild the same RAG pipeline, agent loop, or MCP integration from scratch every time you start a new LLM project.

**AI Agent Lab is a cookbook of ready-to-run templates** — starter code you can fork, customize, and ship as a production LLM app. Every template is self-contained with full source code, built from scratch.

- 🛠️ **Hand-built, not curated** — every template is original work, tested end-to-end before it ships
- ⚡ **Runs in 3 commands** — no broken dependencies, no "figure it out yourself" scaffolding
- 🧠 **Covers the modern AI stack** — AI Agents, Multi-agent Teams, MCP Agents, Voice AI, RAG, Fine-tuning
- 🌐 **Provider-agnostic** — switch between Claude, OpenAI, Gemini, Llama with a config change
- 📖 **Apache-2.0** — fork it, ship it, sell it. No paywall, no signup, no telemetry

---

## 🚀 Quick Start

Run your first agent in 30 seconds:

```bash
git clone https://github.com/Zohreh-ai-nik/ai-agent-lab
cd ai-agent-lab/starter_agents/ai_travel_agent
pip install -r requirements.txt
streamlit run travel_agent.py
```

---

## 📁 Project Structure

```
ai-agent-lab/
├── starter_agents/        # Single-file agents — great place to start
├── advanced_agents/       # Production-style agents with tools & memory
├── multi_agent_teams/     # Multiple agents collaborating on complex tasks
├── rag_tutorials/         # RAG from basic to agentic pipelines
├── mcp_agents/            # MCP server integrations
├── voice_agents/          # Speech-in, speech-out agents
└── docs/                  # Architecture diagrams and guides
```

---

## 🌱 Starter AI Agents

Single-file agents that run with just an API key — a great place to start.

| Agent | What it does | Stack |
|-------|-------------|-------|
| 🧳 AI Travel Agent | Plans multi-city trips with real-time search | Claude + Tavily |
| 📊 AI Data Analysis Agent | Analyzes CSV data and generates insights | Claude + Pandas |
| 🎵 AI Music Generator Agent | Generates music ideas and lyrics | Claude + OpenAI |
| 🌐 Web Scraping AI Agent | Scrapes and summarizes web content | Claude + BeautifulSoup |
| 📝 AI Blog to Podcast Agent | Converts blog posts to podcast scripts | Claude |

---

## 🚀 Advanced AI Agents

Production-style agents with tools, memory, and multi-step reasoning.

| Agent | What it does | Stack |
|-------|-------------|-------|
| 🔍 AI Deep Research Agent | Autonomous multi-source research | Claude + Tavily |
| 💰 AI Financial Coach Agent | Personalized financial planning | Claude + Tools |
| 🎬 AI Movie Production Agent | Full screenplay and production planning | Claude |
| 📈 AI Investment Agent | Market analysis and portfolio insights | Claude + yFinance |
| 🏥 AI Health & Fitness Agent | Personalized wellness planning | Claude |

---

## 🤝 Multi-agent Teams

Multiple agents collaborating to accomplish complex, cross-domain tasks.

| Team | What it does | Stack |
|------|-------------|-------|
| ⚖️ AI Legal Agent Team | Legal document analysis and drafting | Claude + CrewAI |
| 💼 AI Recruitment Agent Team | End-to-end hiring pipeline | Claude + LangGraph |
| 🏠 AI Real Estate Agent Team | Property research and valuation | Claude + Tools |
| 🎮 AI Game Design Agent Team | Full game concept and design | Claude + CrewAI |

---

## 🧠 RAG Tutorials

From basic retrieval to full agentic RAG pipelines.

| Tutorial | What it does | Stack |
|----------|-------------|-------|
| 📚 Basic RAG | Simple document Q&A | Claude + ChromaDB |
| 🔄 Agentic RAG | RAG with autonomous retrieval decisions | Claude + LangGraph |
| 🖼️ Multimodal RAG | Images + text retrieval | Claude + ChromaDB |
| 💾 RAG with Memory | Persistent conversation memory | Claude + Pinecone |

---

## 🔧 MCP Agents

Agents powered by Model Context Protocol server integrations.

| Agent | What it does | Stack |
|-------|-------------|-------|
| 🛠️ AI MCP App Builder | Builds MCP-powered applications | Claude + MCP |
| 📊 MCP Dashboard Agent | Real-time data dashboards via MCP | Claude + MCP |

---

## 🎙️ Voice AI Agents

Speech-in, speech-out agents using real-time voice APIs.

| Agent | What it does | Stack |
|-------|-------------|-------|
| 🎧 Customer Support Voice Agent | Real-time voice customer service | Claude + ElevenLabs |
| 🎙️ Voice RAG Agent | Ask questions by voice, get spoken answers | OpenAI SDK |

---

## ⚙️ Setup

### Prerequisites

- Python 3.10+
- Git
- API key for your chosen LLM provider (Claude, OpenAI, etc.)

### Environment Variables

Each project has its own `.env.example`. Copy and fill in your keys:

```bash
cp .env.example .env
```

Common variables:

```env
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

---

## 🤝 Contributing

Contributions are welcome! Please follow the workflow:

1. Open an issue describing what you want to build
2. Create a branch: `feat/your-agent-name`
3. Commit with conventional commits: `feat:`, `fix:`, `docs:`
4. Open a pull request linking the issue
5. Merge after review

---

## 📄 License

Apache-2.0 — fork it, ship it, sell it. See [LICENSE](LICENSE) for details.

---

## ⭐ If this saves you time, star the repo — that's how the next developer discovers it.

