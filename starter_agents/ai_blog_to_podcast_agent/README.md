# 📰 ➡️ 🎙️ Blog to Podcast Agent

Converts any blog URL into a podcast episode using GPT-4 and ElevenLabs.

## Stack
- OpenAI GPT-4 — summarization
- Firecrawl — blog scraping  
- ElevenLabs — audio generation
- Streamlit — UI

## Quick start
cp .env.example .env  # fill in your keys
pip install -r requirements.txt
streamlit run blog_to_podcast_agent.py

## How it works
1. Firecrawl scrapes the blog URL
2. GPT-4 converts it to a podcast script
3. ElevenLabs converts the script to audio
4. You download the MP3