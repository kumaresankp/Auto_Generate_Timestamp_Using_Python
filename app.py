from flask import Flask, render_template, request
from youtube_transcript_api import YouTubeTranscriptApi
import datetime
import re
from generate_timestamp import evaluate_timestamps

app = Flask(__name__)

def extract_video_id(url_or_id):
    if len(url_or_id) == 11:
        return url_or_id
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url_or_id)
    return match.group(1) if match else None

def format_time(seconds):
    return str(datetime.timedelta(seconds=int(seconds)))

def get_transcript_lines(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return [f"{format_time(entry['start'])} - {entry['text'].replace('\n', ' ')}" for entry in transcript]

def clean_list_output(output):
    output = output.strip()
    if output.startswith("["):
        output = output[1:]
    if output.endswith("]"):
        output = output[:-1]
    lines = output.split("\n")
    cleaned = [line.strip().strip('",') for line in lines if line.strip()]
    return cleaned

@app.route("/", methods=["GET", "POST"])
def index():
    timestamps = []
    error = ""
    if request.method == "POST":
        url = request.form.get("youtube_url")
        video_id = extract_video_id(url)
        if not video_id:
            error = "Invalid YouTube URL."
        else:
            try:
                captions = get_transcript_lines(video_id)
                raw_output = evaluate_timestamps(captions)
                timestamps = clean_list_output(raw_output)
            except Exception as e:
                error = f"Error: {str(e)}"

    return render_template("index.html", timestamps=timestamps, error=error)

if __name__ == "__main__":
    app.run(debug=True)
