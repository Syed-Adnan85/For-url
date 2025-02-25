from flask import Flask, request, jsonify, send_file
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Video Downloader API is running!"

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        response = requests.get(url, stream=True)
        filename = "downloaded_video.mp4"

        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        # **Instead of just returning a message, send the file to the user**
        return send_file(filename, as_attachment=True)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
