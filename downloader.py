from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"  # Folder to save videos
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)  # Create folder if not exists

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    try:
        command = [
            "yt-dlp",
            "-o", f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",  # Save in folder with title
            url
        ]
        subprocess.run(command, check=True)
        
        return jsonify({"message": "Download started", "url": url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
