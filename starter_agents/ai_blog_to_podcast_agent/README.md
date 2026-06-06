# 📰 ➡️ 🎙️ Blog to Podcast Agent

Converts any blog URL into a podcast episode using GPT-4 and ElevenLabs.

## Stack
- OpenAI GPT-4 — summarization
- Firecrawl — blog scraping  
- ElevenLabs — audio generation
- Streamlit — UI

## Quick start

### Setup (First Time Only)
```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Copy and fill environment variables
cp .env.example .env  # Add your API keys

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the web app
streamlit run blog_to_podcast_agent.py
```

### Every Time You Use It
```bash
# Activate virtual environment
source venv/bin/activate

# Run the app
streamlit run blog_to_podcast_agent.py
```

## How it works

The application works as a **3-step pipeline**:

```
Blog URL (Input)
    ↓
[STEP 1] FIRECRAWL - Web Scraping
    ↓ Saves: scraped_blog.txt
[STEP 2] GPT-4 - Script Generation
    ↓ Saves: podcast_script.txt
[STEP 3] ELEVENLABS - Audio Generation
    ↓ Saves: podcast_output.mp3
Audio File (Output)
```

## Testing the Pipeline

### Step-by-Step Testing (For Learning)

#### **STEP 1: Test Firecrawl Scraping**
```bash
python3 test_step1_firecrawl.py
```
- **Input:** Blog URL (you type it)
- **Output:** `scraped_blog.txt` (blog content extracted)
- **Time:** 10-30 seconds

Example URL tested:
```
https://medium.com/@ilya_gorbunov/how-to-learn-python-in-2024-2b6c9a5e5a5f
```

#### **STEP 2: Test GPT-4 Script Generation**
```bash
python3 test_step2_gpt4.py
```
- **Input:** `scraped_blog.txt` (from STEP 1)
- **Output:** `podcast_script.txt` (podcast script)
- **Time:** 30-60 seconds

The script **automatically reads** the file created by STEP 1.

#### **STEP 3: Test ElevenLabs Audio Generation**
```bash
python3 test_step3_elevenlabs.py
```
- **Input:** `podcast_script.txt` (from STEP 2)
- **Output:** `podcast_output.mp3` (audio file)
- **Time:** 1-3 minutes

The script **automatically reads** the file created by STEP 2.

## How Files Are Created (Data Pipeline)

### The Chain of Data

1. **STEP 1: Firecrawl Scraping**
   ```python
   # Scrapes blog from URL
   # Saves to file:
   with open("scraped_blog.txt", "w") as file:
       file.write(blog_content)
   ```
   **Creates:** `scraped_blog.txt`

2. **STEP 2: GPT-4 Script Generation**
   ```python
   # Reads STEP 1 output
   with open("scraped_blog.txt", "r") as file:
       blog_content = file.read()
   
   # Processes it with GPT-4
   podcast_script = generate_script(blog_content)
   
   # Saves to new file:
   with open("podcast_script.txt", "w") as file:
       file.write(podcast_script)
   ```
   **Uses:** `scraped_blog.txt` (from STEP 1)
   **Creates:** `podcast_script.txt`

3. **STEP 3: ElevenLabs Audio Generation**
   ```python
   # Reads STEP 2 output
   with open("podcast_script.txt", "r") as file:
       podcast_script = file.read()
   
   # Processes it with ElevenLabs API
   audio_data = generate_audio(podcast_script)
   
   # Saves to new file:
   with open("podcast_output.mp3", "wb") as file:
       file.write(audio_data)
   ```
   **Uses:** `podcast_script.txt` (from STEP 2)
   **Creates:** `podcast_output.mp3`

### Files After Complete Execution

```bash
ls -la
```

Output:
```
scraped_blog.txt          # 50-200 KB (blog content)
podcast_script.txt        # 10-20 KB (podcast script)
podcast_output.mp3        # 1-5 MB (audio file)
```

## Test Session Example

### URL Used
```
https://medium.com/@ilya_gorbunov/how-to-learn-python-in-2024-2b6c9a5e5a5f
```

### Execution Steps
```bash
# Step 1: Scrape the blog
$ python3 test_step1_firecrawl.py
✓ Title: How to Learn Python in 2024
✓ Content size: 15234 characters
✅ Saved to 'scraped_blog.txt'

# Step 2: Generate script
$ python3 test_step2_gpt4.py
✓ Title: How to Learn Python in 2024
✓ Content size: 15234 characters
🧠 Sending to GPT-4... (30-60 seconds)
✓ Word count: 2456 words
✅ Saved to 'podcast_script.txt'

# Step 3: Generate audio
$ python3 test_step3_elevenlabs.py
✓ Title: How to Learn Python in 2024
✓ Script length: 12800 characters
🎵 Calling ElevenLabs API... (1-3 minutes)
✓ File size: 2.34 MB
✅ Saved to 'podcast_output.mp3'
```

## Play the Generated Audio

```bash
# Option 1: MPV player
mpv podcast_output.mp3

# Option 2: FFplay
ffplay podcast_output.mp3

# Option 3: VLC
vlc podcast_output.mp3
```

## Troubleshooting

### "scraped_blog.txt not found"
- Make sure you ran STEP 1 first
- Check file exists: `ls -la scraped_blog.txt`

### "podcast_script.txt not found"
- Make sure you ran STEP 2 first
- Check file exists: `ls -la podcast_script.txt`

### "Context length exceeded" error
- The blog URL was too long
- Try a shorter blog or article
- Good examples: Medium, Dev.to, TechCrunch

### "API key not found" error
- Make sure `.env` file has the API keys
- Check: `cat .env`
- Keys needed: `OPENAI_API_KEY`, `FIRECRAWL_API_KEY`, `ELEVENLABS_API_KEY`