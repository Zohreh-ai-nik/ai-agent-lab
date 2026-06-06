"""
STEP 3: Generate Audio using ElevenLabs
Learn: How to convert text to natural-sounding audio using ElevenLabs API
"""

# ============================================================================
# SECTION 1: IMPORTS
# ============================================================================
import os
import requests
from dotenv import load_dotenv

# ============================================================================
# SECTION 2: LOAD API KEY
# ============================================================================
load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
print(f"✓ ElevenLabs API Key loaded: {ELEVENLABS_API_KEY[:10]}...\n")

# ============================================================================
# SECTION 3: READ THE PODCAST SCRIPT FROM STEP 2
# ============================================================================
def read_podcast_script():
    """
    Reads the podcast script that was created in STEP 2
    
    Returns:
        Dictionary with success status and script content
    """
    
    print("📖 Reading podcast script from STEP 2...")
    
    try:
        # Open the file created in STEP 2
        with open("podcast_script.txt", "r", encoding="utf-8") as file:
            content = file.read()
        
        # Extract title and script
        lines = content.split("\n")
        title = lines[0].replace("PODCAST SCRIPT: ", "")
        
        # Get the script (skip header lines)
        script = "\n".join(lines[3:])
        
        print(f"✓ Title: {title}")
        print(f"✓ Script length: {len(script)} characters")
        print(f"✓ Word count: {len(script.split())} words\n")
        
        return {
            "success": True,
            "title": title,
            "script": script
        }
    
    except FileNotFoundError:
        print("❌ ERROR: podcast_script.txt not found")
        print("   Please run STEP 2 first: python3 test_step2_gpt4.py\n")
        return {
            "success": False,
            "error": "File not found"
        }


# ============================================================================
# SECTION 4: GENERATE AUDIO WITH ELEVENLABS
# ============================================================================
def generate_audio_elevenlabs(podcast_script: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM"):
    """
    Converts podcast script to audio using ElevenLabs text-to-speech API
    
    Args:
        podcast_script: The podcast script text to convert
        voice_id: The ElevenLabs voice ID to use
                 Default: 21m00Tcm4TlvDq8ikWAM (Rachel - professional female voice)
                 Other options: "EXAVITQu4vr4xnSDxMaL" (Bella), etc.
    
    Returns:
        Dictionary with audio data or error message
    """
    
    print("\n" + "="*80)
    print("GENERATING AUDIO WITH ELEVENLABS")
    print("="*80)
    print(f"🎙️  Voice ID: {voice_id}")
    print(f"📝 Text length: {len(podcast_script)} characters\n")
    
    # Step 1: Prepare the API request
    print("🎵 Preparing ElevenLabs API request...")
    
    # The ElevenLabs API endpoint
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    # Headers with authentication
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    
    # Request body
    data = {
        "text": podcast_script,
        "model_id": "eleven_monolingual_v1",  # The AI model for speech synthesis
        "voice_settings": {
            "stability": 0.5,        # 0=variable, 1=consistent (0.5=balanced)
            "similarity_boost": 0.75 # How much to match the voice
        }
    }
    
    try:
        print("⏳ Calling ElevenLabs API... (this takes 1-3 minutes)\n")
        
        # Make the HTTP request to ElevenLabs
        response = requests.post(url, json=data, headers=headers)
        
        # Check if request was successful
        if response.status_code == 200:
            print("✅ Audio generation successful!\n")
            
            # Get the audio data (binary MP3 file)
            audio_data = response.content
            audio_size_mb = len(audio_data) / (1024 * 1024)
            
            print("📊 AUDIO DETAILS:")
            print("-" * 80)
            print(f"✓ File size: {audio_size_mb:.2f} MB")
            print(f"✓ Format: MP3")
            print(f"✓ Sample rate: 44.1 kHz")
            print(f"✓ Quality: High")
            print("-" * 80)
            
            return {
                "success": True,
                "audio": audio_data,
                "size_mb": audio_size_mb
            }
        
        else:
            # If API returns an error
            error_msg = f"HTTP {response.status_code}: {response.text}"
            print(f"❌ ERROR: {error_msg}\n")
            return {
                "success": False,
                "error": error_msg
            }
    
    except requests.exceptions.RequestException as error:
        # Network error
        print(f"❌ ERROR: Network request failed: {str(error)}\n")
        return {
            "success": False,
            "error": str(error)
        }


# ============================================================================
# SECTION 5: SAVE AUDIO TO FILE
# ============================================================================
def save_audio_to_file(audio_data: bytes, filename: str = "podcast_output.mp3"):
    """
    Saves the audio data to an MP3 file
    
    Args:
        audio_data: Binary audio data from ElevenLabs
        filename: Name of output file
    
    Returns:
        Dictionary with success status and file info
    """
    
    print("\n💾 Saving audio to file...")
    
    try:
        # Write binary audio data to file
        with open(filename, "wb") as file:
            file.write(audio_data)
        
        # Get file size
        file_size = os.path.getsize(filename)
        file_size_mb = file_size / (1024 * 1024)
        
        print(f"✅ Saved to '{filename}'")
        print(f"   Size: {file_size_mb:.2f} MB")
        print(f"   Location: {os.path.abspath(filename)}\n")
        
        return {
            "success": True,
            "file": filename,
            "size_mb": file_size_mb
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
    print("  BLOG TO PODCAST - STEP 3: ELEVENLABS AUDIO GENERATION")
    print("█" * 80 + "\n")
    
    # Step 1: Read the podcast script from STEP 2
    script_result = read_podcast_script()
    
    if not script_result["success"]:
        print("Cannot continue without podcast script.")
        exit(1)
    
    podcast_title = script_result["title"]
    podcast_script = script_result["script"]
    
    # Step 2: Generate audio with ElevenLabs
    audio_result = generate_audio_elevenlabs(podcast_script)
    
    if not audio_result["success"]:
        print("Cannot continue without audio generation.")
        exit(1)
    
    audio_data = audio_result["audio"]
    
    # Step 3: Save audio to file
    save_result = save_audio_to_file(audio_data)
    
    # Show final result
    print("\n" + "█" * 80)
    print("  FINAL RESULT - COMPLETE PIPELINE!")
    print("█" * 80)
    
    if script_result["success"] and audio_result["success"] and save_result["success"]:
        print(f"✅ SUCCESS! Podcast audio generated!\n")
        print(f"   Podcast: {podcast_title}")
        print(f"   Audio file: {save_result['file']}")
        print(f"   File size: {save_result['size_mb']:.2f} MB")
        print(f"\n🎉 All 3 steps completed!")
        print(f"   STEP 1 ✓ Firecrawl (Scraped blog)")
        print(f"   STEP 2 ✓ GPT-4 (Generated script)")
        print(f"   STEP 3 ✓ ElevenLabs (Generated audio)")
        print(f"\n🎵 You can now play: {save_result['file']}")
        print(f"   With: mpv, ffplay, or any MP3 player")
    else:
        print(f"❌ FAILED!")
        if not script_result["success"]:
            print(f"   Script error: {script_result['error']}")
        if not audio_result["success"]:
            print(f"   Audio error: {audio_result['error']}")
        if not save_result["success"]:
            print(f"   Save error: {save_result['error']}")
    
    print("\n")