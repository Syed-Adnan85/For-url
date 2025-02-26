import re
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def extract_video_links(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": "Failed to fetch the webpage."}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    video_links = set()

    # Extract videos from <video> tags
    for video in soup.find_all("video"):
        for source in video.find_all("source"):
            if source.get("src"):
                video_links.add(source["src"])
    
    # Extract videos from <iframe> and <embed> (for embedded videos)
    for iframe in soup.find_all(["iframe", "embed"]):
        src = iframe.get("src")
        if src and ("youtube.com" in src or "vimeo.com" in src):
            video_links.add(src)
    
    # Extract video links from script tags (hidden sources)
    scripts = soup.find_all("script")
    for script in scripts:
        if script.string:
            matches = re.findall(r'(https?://[^\s]+?\.mp4)', script.string)
            video_links.update(matches)

    return list(video_links)

@app.route('/get-video', methods=['GET'])
def get_video():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Please provide a URL"}), 400
    
    video_urls = extract_video_links(url)
    return jsonify({"videos": video_urls})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
