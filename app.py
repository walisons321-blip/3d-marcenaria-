from pathlib import Path
import os, shutil, subprocess, uuid
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

BASE = Path(__file__).resolve().parent
UPLOADS = BASE / 'uploads'
CONVERTED = BASE / 'converted'
UPLOADS.mkdir(exist_ok=True); CONVERTED.mkdir(exist_ok=True)
app = Flask(__name__, static_folder='static', static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

@app.get('/')
def index(): return app.send_static_file('index.html')

@app.get('/api/health')
def health():
    blender = os.getenv('BLENDER_BIN') or shutil.which('blender')
    return jsonify(ok=True, blender=bool(blender), blender_path=blender)

@app.post('/api/convert-blend')
def convert_blend():
    f = request.files.get('file')
    if not f or not f.filename.lower().endswith('.blend'):
        return jsonify(error='Envie um arquivo .blend'), 400
    blender = os.getenv('BLENDER_BIN') or shutil.which('blender')
    if not blender:
        return jsonify(error='Blender não está instalado no servidor. Veja o README.'), 503
    job = uuid.uuid4().hex
    src = UPLOADS / f'{job}_{secure_filename(f.filename)}'
    out = CONVERTED / f'{job}.glb'
    f.save(src)
    script = BASE / 'convert_blend.py'
    try:
        p = subprocess.run([blender, '-b', str(src), '--python', str(script), '--', str(out)],
                           capture_output=True, text=True, timeout=300)
        if p.returncode != 0 or not out.exists():
            tail = (p.stderr or p.stdout or '')[-3000:]
            return jsonify(error='Falha na conversão.', details=tail), 500
        return jsonify(url=f'/converted/{out.name}', name=Path(f.filename).stem)
    except subprocess.TimeoutExpired:
        return jsonify(error='A conversão excedeu 5 minutos.'), 504
    finally:
        try: src.unlink(missing_ok=True)
        except Exception: pass

@app.get('/converted/<path:name>')
def converted(name): return send_from_directory(CONVERTED, name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '8000')), debug=True)
