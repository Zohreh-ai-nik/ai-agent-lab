"""
COMPLETE BLOG TO PODCAST AGENT - END-TO-END
Converts a blog URL to a podcast episode in one script
No manual steps required - just run and wait!
"""

import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
from firecrawl import FirecrawlApp
from datetime import datetime

# ============================================================================
# SECTION 1: LOAD ENVIRONMENT & INITIALIZE CLIENTS
# ============================================================================
print("\n" + "█" * 80)
print("  BLOG TO PODCAST - COMPLETE PIPELINE")
print("█" * 80 + "\n")

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

print("🔑 Checking API keys...")
if not all([OPENAI_API_KEY, FIRECRAWL_API_KEY, ELEVENLABS_API_KEY]):
    print("❌ ERROR: Missing API keys in .env file")
    print("   Required: OPENAI_API_KEY, FIRECRAWL_API_KEY, ELEVENLABS_API_KEY")
    exit(1)

print("✅ All API keys loaded\n")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


# ============================================================================
# FUNCTION 1: STEP 1 - SCRAPE BLOG WITH FIRECRAWL
# ============================================================================
def step1_scrape_blog(blog_url: str) -> dict:
    """
    STEP 1: Scrapes blog content using Firecrawl
    
    Args:
        blog_url: The URL of the blog to scrape
    
    Returns:
        Dictionary with title and content
    """
    
    print("\n" + "="*80)
    print("STEP 1: FIRECRAWL - WEB SCRAPING")
    print("="*80)
    print(f"🔗 URL: {blog_url}\n")
    
    try:
        print("🕷️  Initializing Firecrawl...")
        app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
        
        print("⏳ Scraping blog... (10-30 seconds)\n")
        scrape_result = app.scrape_url(
            blog_url,
            params={"formats": ["markdown"]}
        )
        
        markdown_content = scrape_result.get("markdown", "")
        metadata = scrape_result.get("metadata", {})
        title = metadata.get("title", "Unknown Title")
        
        print("✅ Scraping successful!\n")
        print(f"   Title: {title}")
        print(f"   Content size: {len(markdown_content)} characters\n")
        
        return {
            "success": True,
            "title": title,
            "content": markdown_content
        }
    
    except Exception as error:
        print(f"❌ FAILED: {str(error)}\n")
        return {
            "success": False,
            "error": str(error)
        }


# ============================================================================
# FUNCTION 2: STEP 2 - GENERATE PODCAST SCRIPT WITH GPT-4
# ============================================================================
def step2_generate_script(blog_title: str, blog_content: str) -> dict:
    """
    STEP 2: Generates podcast script using GPT-4
    
    Args:
        blog_title: Title of the blog
        blog_content: Full content of the blog
    
    Returns:
        Dictionary with the generated script
    """
    
    print("\n" + "="*80)
    print("STEP 2: GPT-4 - PODCAST SCRIPT GENERATION")
    print("="*80)
    print(f"📝 Title: {blog_title}")
    print(f"   Content: {len(blog_content)} characters\n")
    
    # Limit content to first 3000 characters to avoid token limit
    limited_content = blog_content[:3000]
    
    prompt = f"""You are a professional podcast scriptwriter. Convert the following blog post into an engaging podcast script.

The script should:
1. Start with a catchy intro (2-3 sentences) about the topic
2. Break down main points into easy-to-understand segments
3. Use conversational language (like a host talking to listeners)
4. Include natural transitions between topics
5. Add emphasis on key points
6. End with a meaningful conclusion
7. Be approximately 8-10 minutes of speaking time (2000-2500 words)

Blog Title: {blog_title}

Blog Content:
{limited_content}

Please write the podcast script now (just the script, no meta-comments):"""

    try:
        print("🧠 Sending to GPT-4... (30-60 seconds)\n")
        
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional podcast scriptwriter who creates engaging, natural-sounding audio content."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=3000
        )
        
        podcast_script = response.choices[0].message.content
        word_count = len(podcast_script.split())
        speaking_time = word_count // 130  # Avg 130 words per minute
        
        print("✅ Script generation successful!\n")
        print(f"   Word count: {word_count} words")
        print(f"   Speaking time: ~{speaking_time} minutes\n")
        
        return {
            "success": True,
            "script": podcast_script
        }
    
    except Exception as error:
        print(f"❌ FAILED: {str(error)}\n")
        return {
            "success": False,
            "error": str(error)
        }


# ============================================================================
# FUNCTION 3: STEP 3 - GENERATE AUDIO WITH ELEVENLABS
# ============================================================================
def step3_generate_audio(podcast_script: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> dict:
    """
    STEP 3: Generates audio using ElevenLabs text-to-speech
    
    Args:
        podcast_script: The podcast script to convert to audio
        voice_id: ElevenLabs voice ID (default: Rachel)
    
    Returns:
        Dictionary with audio data
    """
    
    print("\n" + "="*80)
    print("STEP 3: ELEVENLABS - AUDIO GENERATION")
    print("="*80)
    print(f"🎙️  Voice: Rachel (Professional Female)")
    print(f"   Script: {len(podcast_script)} characters\n")
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "text": podcast_script,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    try:
        print("🎵 Calling ElevenLabs API... (1-3 minutes)\n")
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            audio_data = response.content
            audio_size_mb = len(audio_data) / (1024 * 1024)
            
            print("✅ Audio generation successful!\n")
            print(f"   File size: {audio_size_mb:.2f} MB")
            print(f"   Format: MP3\n")
            
            return {
                "success": True,
                "audio": audio_data,
                "size_mb": audio_size_mb
            }
        else:
            error_msg = f"HTTP {response.status_code}: {response.text}"
            print(f"❌ FAILED: {error_msg}\n")
            return {
                "success": False,
                "error": error_msg
            }
    
    except Exception as error:
        print(f"❌ FAILED: {str(error)}\n")
        return {
            "success": False,
            "error": str(error)
        }


# ============================================================================
# FUNCTION 4: SAVE AUDIO TO FILE
# ============================================================================
def save_audio(audio_data: bytes, filename: str = None) -> dict:
    """
    Saves audio to MP3 file
    
    Args:
        audio_data: Binary audio data
        filename: Output filename (auto-generated if not provided)
    
    Returns:
        Dictionary with file info
    """
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"podcast_{timestamp}.mp3"
    
    try:
        with open(filename, "wb") as file:
            file.write(audio_data)
        
        file_size = os.path.getsize(filename)
        file_size_mb = file_size / (1024 * 1024)
        
        return {
            "success": True,
            "file": filename,
            "size_mb": file_size_mb
        }
    
    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }


# ============================================================================
# MAIN EXECUTION - END-TO-END PIPELINE
# ============================================================================
if __name__ == "__main__":
    
    # Get blog URL from user
    print("ℹ️  Example URLs:")
    print("  - https://medium.com/@ilya_gorbunov/how-to-learn-python-in-2024-2b6c9a5e5a5f")
    print("  - https://dev.to/codenewbie/how-to-start-learning-to-code-1h2g")
    print("  - https://www.theverge.com/2024/1/15/24038284/ai-regulation-2024\n")
    
    blog_url = input("🔗 Enter a blog URL: ").strip()
    
    if not blog_url:
        print("❌ No URL provided. Exiting.")
        exit(1)
    
    # ========================================================================
    # RUN THE COMPLETE PIPELINE
    # ========================================================================
    
    # STEP 1: Scrape blog
    scrape_result = step1_scrape_blog(blog_url)
    if not scrape_result["success"]:
        print("\n❌ Pipeline failed at STEP 1")
        exit(1)
    
    blog_title = scrape_result["title"]
    blog_content = scrape_result["content"]
    
    # STEP 2: Generate script
    script_result = step2_generate_script(blog_title, blog_content)
    if not script_result["success"]:
        print("\n❌ Pipeline failed at STEP 2")
        exit(1)
    
    podcast_script = script_result["script"]
    
    # STEP 3: Generate audio
    audio_result = step3_generate_audio(podcast_script)
    if not audio_result["success"]:
        print("\n❌ Pipeline failed at STEP 3")
        exit(1)
    
    audio_data = audio_result["audio"]
    
    # Save audio to file
    save_result = save_audio(audio_data)
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    
    print("\n" + "█" * 80)
    print("  COMPLETE! PODCAST GENERATED SUCCESSFULLY")
    print("█" * 80)
    
    if all([scrape_result["success"], script_result["success"], 
            audio_result["success"], save_result["success"]]):
        
        print(f"\n✅ SUCCESS!\n")
        print(f"📰 Blog Title: {blog_title}")
        print(f"🎙️  Audio File: {save_result['file']}")
        print(f"📊 File Size: {save_result['size_mb']:.2f} MB")
        print(f"\n✨ Pipeline Summary:")
        print(f"   ✓ STEP 1: Firecrawl (Blog scraping)")
        print(f"   ✓ STEP 2: GPT-4 (Podcast script)")
        print(f"   ✓ STEP 3: ElevenLabs (Audio generation)")
        print(f"\n🎵 Play your podcast:")
        print(f"   mpv {save_result['file']}")
        print(f"   ffplay {save_result['file']}")
        print(f"   vlc {save_result['file']}")
    else:
        print(f"\n❌ Pipeline failed!")
        if not save_result["success"]:
            print(f"   Save error: {save_result['error']}")
    
    print("\n")
