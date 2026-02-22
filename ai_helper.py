import json
from google import genai

MODEL_ID = "gemini-2.5-flash" 
API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual API key
client = genai.Client(api_key=API_KEY)

def analyze_url(user_input):
    # 1. PLATFORM ALLOTTING (Priority check for links)
    input_lower = user_input.lower()
    platform_title = "Personal Note" # Default for thoughts/dates
    
    if "instagram.com" in input_lower:
        platform_title = "Instagram Post"
    elif "youtube.com" in input_lower or "youtu.be" in input_lower:
        platform_title = "YouTube Content"
    elif "x.com" in input_lower or "twitter.com" in input_lower:
        platform_title = "X (Twitter) Post"

    # 2. UPDATED PROMPT (Handles thoughts, dates, and links)
    prompt = f"""
    Analyze this input: "{user_input}"
    It could be a URL, a random thought, an important date, or a task.
    Return ONLY a JSON object with:
    "title": A short, catchy headline (max 5 words).
    "category": A single-word category (e.g., PRODUCTIVITY, REMINDER, TECH, HEALTH).
    "summary": A concise one-sentence description.
    """
    
    try:
        response = client.models.generate_content(
            model=MODEL_ID, 
            contents=prompt,
            config={'response_mime_type': 'application/json'}
        )
        data = json.loads(response.text)
        
        # 3. SMART TITLE MERGE
        ai_title = data.get("title")
        final_title = ai_title if (ai_title and "Untitled" not in ai_title) else platform_title
        
        return (
            data.get("category", "GENERAL").upper(), 
            data.get("summary", "Analysis complete."), 
            final_title
        )
        
    except Exception as e:
        print(f"AI Error: {e}")
        return "MISC", "Saved successfully (AI currently offline).", platform_title