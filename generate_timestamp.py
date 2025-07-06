import google.generativeai as genai
import json

API_KEY = "your_api_key"
genai.configure(api_key=API_KEY)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)


def evaluate_timestamps(captions):

    prompt = f"""
    You are given a YouTube video transcript with timestamps. Your task is to extract only the important or meaningful moments from the transcript.

    🎯 For each important moment:
    - Include the timestamp (HH:MM format)
    - Write just 1 to 3 words describing what's happening
    - Each line should follow this format:  
    `timestamp label`, for example: `00:00 Intro`

    🛑 DO NOT return a JSON list.  
    ✅ Just return plain lines like:
    00:00 Intro  
    00:15 Install Add-ins  
    00:45 Formula Example  
    ...

    💡 Only include timestamps where new sections or key actions begin and i need only the super important
    only remove any unneccessary ones you know what i mean right innclude only the super important timestamp only.  
    ⛔️ Skip unimportant lines or filler content.

    Here is the transcript:
    {captions}
    """

    # Generate evaluation using GenAI
    response = model.generate_content(prompt)

    return response.text
