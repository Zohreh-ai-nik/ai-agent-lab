#step 1.1: just print "hello"
print("Blog to Podcast Agent Starting...")
 #add environment loading
from dotenv import load_dotenv
import os
from firecrawl import FirecrawlApp #the scraper tool
load_dotenv()
 #add api key loading
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

def scrape_blog(blog_url: str):
    """
    Scrapes a blog post from a URL using Firecrawl
    
    Args:
        blog_url: The URL of the blog
    
    Returns:
        Dictionary with success status, title, content, or error
    """
    
    # Show user what we're doing
    print("\n" + "="*80)
    print("STARTING FIRECRAWL SCRAPING")
    print("="*80)
    print(f"📍 Target URL: {blog_url}\n")
    
    # Try to scrape (catch errors if something goes wrong)
    try:
        print("🕷️  Initializing Firecrawl...")
        
        # Create Firecrawl instance with API key
        app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
        
        print("⏳ Scraping... (10-30 seconds)\n")
        
        # Scrape the URL
        scrape_result = app.scrape_url(
            blog_url,
            params={"formats": ["markdown"]}  # Get clean markdown format
        )
        
        print("✅ Scraping successful!\n")
        
        # Extract the data from result
        markdown_content = scrape_result.get("markdown", "")
        metadata = scrape_result.get("metadata", {})
        title = metadata.get("title", "Unknown")
        
        # Show the results
        print("📊 RESULTS:")
        print("-" * 80)
        print(f"✓ Title: {title}")
        print(f"✓ Content size: {len(markdown_content)} characters")
        print(f"✓ First 500 characters:")
        print("-" * 80)
        print(markdown_content[:500])
        print("-" * 80)
        
        # Save to file for next step
        print("\n💾 Saving to file...")
        with open("scraped_blog.txt", "w", encoding="utf-8") as file:
            file.write(f"TITLE: {title}\n")
            file.write(f"URL: {blog_url}\n")
            file.write("-" * 80 + "\n\n")
            file.write(markdown_content)
        
        print("✅ Saved to 'scraped_blog.txt'\n")
        
        # Return success result
        return {
            "success": True,
            "title": title,
            "content": markdown_content
        }
    
    # If error happens, catch it
    except Exception as error:
        print(f"❌ ERROR: {str(error)}\n")
        return {
            "success": False,
            "error": str(error)
        }
        
if __name__ == "__main__":
    
    # Print header
    print("\n" + "█" * 80)
    print("  BLOG TO PODCAST - STEP 1: FIRECRAWL TEST")
    print("█" * 80)
    
    # Show examples
    print("\nExample URLs to try:")
    print("  - https://www.theverge.com/2024/1/15/24038284/ai-regulation-2024")
    print("  - https://medium.com/@example/your-post\n")
    
    # Ask user for URL
    blog_url = input("🔗 Enter a blog URL: ").strip()
    
    # Check if empty
    if not blog_url:
        print("❌ No URL provided.")
        exit(1)
    
    # Call the scrape function
    result = scrape_blog(blog_url)
    
    # Show result
    print("\n" + "█" * 80)
    print("  FINAL RESULT")
    print("█" * 80)
    
    if result["success"]:
        print(f"✅ SUCCESS!")
        print(f"   Title: {result['title']}")
        print("\n📝 Next: Use test_step2_gpt4.py")
    else:
        print(f"❌ FAILED!")
        print(f"   Error: {result['error']}")
        print("\n💡 Troubleshooting:")
        print("   1. Check .env has FIRECRAWL_API_KEY")
        print("   2. Check internet connection")
        print("   3. Try different URL")
    
    print("\n")