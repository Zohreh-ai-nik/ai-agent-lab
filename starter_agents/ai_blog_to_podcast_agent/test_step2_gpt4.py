"""
STEP 2: Generate Podcast Script using GPT-4
Learn: How to use AI to convert blog content into a podcast script
"""

# ============================================================================
# SECTION 1: IMPORTS
# ============================================================================
import os
from dotenv import load_dotenv
from openai import OpenAI

# ============================================================================
# SECTION 2: LOAD API KEY
# ============================================================================
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(f"✓ OpenAI API Key loaded: {OPENAI_API_KEY[:10]}...\n")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# ============================================================================
# SECTION 3: READ THE BLOG CONTENT FROM STEP 1
# ============================================================================
def read_scraped_blog():
    """
    Reads the blog content that was saved in STEP 1
    
    Returns:
        Dictionary with title and content
    """
    
    print("📖 Reading scraped blog from STEP 1...")
    
    try:
        # Open the file created in STEP 1
        with open("scraped_blog.txt", "r", encoding="utf-8") as file:
            content = file.read()
        
        # Extract title (it's on the first line)
        lines = content.split("\n")
        title = lines[0].replace("TITLE: ", "")
        
        # Get the rest as blog content (skip header lines)
        blog_content = "\n".join(lines[3:])  # Skip title, URL, and dashes
        
        print(f"✓ Title: {title}")
        print(f"✓ Content size: {len(blog_content)} characters\n")
        
        return {
            "success": True,
            "title": title,
            "content": blog_content
        }
    
    except FileNotFoundError:
        print("❌ ERROR: scraped_blog.txt not found")
        print("   Please run STEP 1 first: python3 test_step1_firecrawl.py\n")
        return {
            "success": False,
            "error": "File not found"
        }


# ============================================================================
# SECTION 4: GENERATE PODCAST SCRIPT WITH GPT-4
# ============================================================================
def generate_podcast_script(blog_title: str, blog_content: str):
    """
    Uses GPT-4 to convert blog content into a podcast script
    
    Args:
        blog_title: The title of the blog
        blog_content: The main content of the blog
    
    Returns:
        Dictionary with the generated script
    """
    
    print("\n" + "="*80)
    print("GENERATING PODCAST SCRIPT WITH GPT-4")
    print("="*80)
    print(f"📝 Blog title: {blog_title}\n")
    
    # Step 1: Create a detailed prompt for GPT-4
    prompt = f"""You are a professional podcast scriptwriter. Convert the following blog post into an engaging podcast script.

The script should:
1. Start with a catchy intro (2-3 sentences) about the topic
2. Break down the main points into easy-to-understand segments
3. Use conversational language (like a host talking to listeners)
4. Include natural transitions between topics
5. Add emphasis on key points
6. End with a meaningful conclusion
7. Be approximately 8-10 minutes of speaking time (about 2000-2500 words)

Blog Title: {blog_title}

Blog Content:
{blog_content}

Please write the podcast script now (just the script, no meta-comments):"""

    try:
        print("🧠 Sending to GPT-4... (this takes 30-60 seconds)\n")
        
        # Call GPT-4 API
        response = client.chat.completions.create(
            model="gpt-4-turbo",  # Using GPT-4 for better quality
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
            temperature=0.7,  # Creativity level (0.7 = balanced)
            max_tokens=3000   # Maximum length of response
        )
        
        # Extract the script from response
        podcast_script = response.choices[0].message.content
        word_count = len(podcast_script.split())
        speaking_time = word_count // 130  # Average 130 words per minute
        
        print("✅ GPT-4 script generation successful!\n")
        
        # Show results
        print("📊 SCRIPT DETAILS:")
        print("-" * 80)
        print(f"✓ Word count: {word_count} words")
        print(f"✓ Estimated speaking time: ~{speaking_time} minutes")
        print(f"✓ First 800 characters of script:")
        print("-" * 80)
        print(podcast_script[:800])
        print("\n...")
        print("-" * 80)
        
        return {
            "success": True,
            "script": podcast_script,
            "word_count": word_count,
            "speaking_time": speaking_time
        }
    
    except Exception as error:
        print(f"❌ ERROR: {str(error)}\n")
        return {
            "success": False,
            "error": str(error)
        }


# ============================================================================
# SECTION 5: SAVE SCRIPT TO FILE
# ============================================================================
def save_script_to_file(podcast_script: str, blog_title: str):
    """
    Saves the podcast script to a file for STEP 3
    
    Args:
        podcast_script: The generated script
        blog_title: The title (for naming the file)
    
    Returns:
        File path
    """
    
    print("\n💾 Saving script to file...")
    
    try:
        filename = "podcast_script.txt"
        
        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"PODCAST SCRIPT: {blog_title}\n")
            file.write("=" * 80 + "\n\n")
            file.write(podcast_script)
        
        print(f"✅ Saved to '{filename}'\n")
        
        return {
            "success": True,
            "file": filename
        }
    
    except Exception as error:
        print(f"❌ ERROR saving file: {str(error)}\n")
        return {
            "success": False,
            "error": str(error)
        }


# ============================================================================
# SECTION 6: MAIN PROGRAM
# ============================================================================
if __name__ == "__main__":
    
    # Print header
    print("\n" + "█" * 80)
    print("  BLOG TO PODCAST - STEP 2: GPT-4 SCRIPT GENERATION")
    print("█" * 80 + "\n")
    
    # Step 1: Read the blog from STEP 1
    blog_result = read_scraped_blog()
    
    if not blog_result["success"]:
        print("Cannot continue without blog content.")
        exit(1)
    
    blog_title = blog_result["title"]
    blog_content = blog_result["content"]
    
    # Step 2: Generate script with GPT-4
    script_result = generate_podcast_script(blog_title, blog_content)
    
    if not script_result["success"]:
        print("Cannot continue without generated script.")
        exit(1)
    
    podcast_script = script_result["script"]
    
    # Step 3: Save script to file
    save_result = save_script_to_file(podcast_script, blog_title)
    
    # Show final result
    print("\n" + "█" * 80)
    print("  FINAL RESULT")
    print("█" * 80)
    
    if script_result["success"] and save_result["success"]:
        print(f"✅ SUCCESS!")
        print(f"   Blog: {blog_title}")
        print(f"   Word count: {script_result['word_count']}")
        print(f"   Speaking time: ~{script_result['speaking_time']} minutes")
        print(f"   Saved to: {save_result['file']}")
        print("\n📝 Next step: Use this script with ElevenLabs in test_step3_elevenlabs.py")
    else:
        print(f"❌ FAILED!")
        if not script_result["success"]:
            print(f"   Script error: {script_result['error']}")
        if not save_result["success"]:
            print(f"   Save error: {save_result['error']}")
    
    print("\n")