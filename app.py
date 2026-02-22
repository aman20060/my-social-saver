from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import ai_helper
import db

app = Flask(__name__)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').strip()
    media_url = request.values.get('MediaUrl0')
    content_type = request.values.get('MediaContentType0', '')

    # Initialize fallback values
    url = incoming_msg
    category, summary, title = "MISC", "Processing...", "New Entry"

    try:
        # 1. HANDLE MEDIA (Images, Voice, Video)
        if media_url:
            url = media_url
            if 'image' in content_type:
                category, summary, title = "IMAGE", "Image saved from WhatsApp", "Captured Image"
            elif 'audio' in content_type:
                category, summary, title = "VOICE", "Voice note received", "Voice Memo"
            elif 'video' in content_type:
                category, summary, title = "VIDEO", "Video content saved", "Stored Video"
        
        # 2. HANDLE TEXT (Links, Thoughts, Dates)
        else:
            if not incoming_msg:
                return "" # Ignore empty messages
            
            # Use AI helper for everything else (Links or Thoughts)
            # This is where your previous 404/429 error happened
            category, summary, title = ai_helper.analyze_url(incoming_msg)

        # 3. SAVE TO DATABASE
        db.save_link(url, category, summary, title)
        reply_text = f"✅ Saved to {category} bucket!\nTitle: {title}"

    except Exception as e:
        # Safety fallback so the server never crashes
        print(f"CRITICAL ERROR: {e}")
        db.save_link(url, "ERROR", "Something went wrong during analysis", "Unanalyzed Entry")
        reply_text = "⚠️ Saved, but AI analysis failed. Check your terminal for details."

    resp = MessagingResponse()
    resp.message(reply_text)
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)