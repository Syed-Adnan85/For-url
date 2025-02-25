from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

def extract_video_links(url):
    """ Extracts all possible video links from a given webpage. """
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            return None, f"Failed to load page. Status code: {response.status_code}"

        soup = BeautifulSoup(response.text, "html.parser")
        video_links = set()

        # ✅ Extract from <video> and <source> tags
        for video in soup.find_all("video"):
            if video.get("src"):
                video_links.add(video["src"])
        for source in soup.find_all("source"):
            if source.get("src"):
                video_links.add(source["src"])

        # ✅ Extract from iframes (embedded videos)
        for iframe in soup.find_all("iframe"):
            iframe_src = iframe.get("src")
            if iframe_src and "youtube" not in iframe_src:  # Exclude YouTube embeds
                video_links.add(iframe_src)

        # ✅ Extract from scripts (hidden video URLs)
        scripts = soup.find_all("script")
        for script in scripts:
            script_text = script.text
            urls = re.findall(r'(https?://[^\s"\']+\.mp4)', script_text)  # Find .mp4 links in JS
            video_links.update(urls)

        return list(video_links), None if video_links else "No video found on the webpage."

    except Exception as e:
        return None, str(e)

@app.route('/get_video', methods=['GET'])
def get_video():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    video_urls, error = extract_video_links(url)
    if video_urls:
        return jsonify({"video_urls": video_urls})
    else:
        return jsonify({"error": error}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
