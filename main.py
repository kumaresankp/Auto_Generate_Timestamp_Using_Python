from youtube_transcript_api import YouTubeTranscriptApi
import datetime
from generate_timestamp import evaluate_timestamps

# Format seconds to HH:MM:SS
def format_time(seconds):
    return str(datetime.timedelta(seconds=int(seconds)))

# Get transcript and format as "timestamp - text"
def get_transcript_lines(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return [f"{format_time(entry['start'])} - {entry['text'].replace('\n', ' ')}" for entry in transcript]

def clean_list_output(output):
    # Remove square brackets
    output = output.strip()
    if output.startswith("["):
        output = output[1:]
    if output.endswith("]"):
        output = output[:-1]
    
    # Remove quotes and strip each line
    lines = output.split("\n")
    cleaned = [line.strip().strip('",') for line in lines if line.strip()]
    return cleaned

# Main function
if __name__ == "__main__":
    video_id = input("Enter YouTube Video ID: ").strip()
    
    print("📥 Getting transcript...")
    captions = get_transcript_lines(video_id)

    print("🤖 Extracting important timestamps using Gemini...")
    important_points = evaluate_timestamps(captions)

    print("\n✅ Important Moments:\n")
    for line in clean_list_output(important_points):
        print(line)