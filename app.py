from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/extract', methods=['GET'])
def extract():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": "error", "message": "URL missing"}), 400
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android']
            }
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            stream_url = info.get('url', '')
            title = info.get('title', 'Unknown')
            
            return jsonify({
                "status": "success", 
                "stream_url": stream_url,
                "title": title
            })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
