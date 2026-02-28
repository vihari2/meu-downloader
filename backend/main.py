from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import yt_dlp
import requests

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def get_video_link():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"error": "Link vazio!"}), 400

    try:
        ydl_opts = {'format': 'best', 'quiet': True}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            
            video_data = requests.get(video_url, stream=True)
            
            # Criamos uma resposta que o navegador entende como "Arquivo para baixar"
            return Response(
                video_data.content,
                mimetype="video/mp4",
                headers={
                    "Content-Disposition": "attachment; filename=video_instagram.mp4"
                }
            )

    except Exception as e:
        return jsonify({"error": "Erro ao processar vídeo: " + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)