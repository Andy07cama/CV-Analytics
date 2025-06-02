from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import LectorDeTextos
import os
from ComparadorDeTexto import comparar_textos




app = Flask(__name__)
@app.route("/")
def home():
    return "✅ Flask está corriendo correctamente."


UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/comparar', methods=['POST'])
def comparar():
    if 'cv' not in request.files or 'requisitos' not in request.files:
        return jsonify({'error': 'Faltan archivos'}), 400


    cv_file = request.files['cv']
    req_file = request.files['requisitos']


    if cv_file.filename == '' or req_file.filename == '':
        return jsonify({'error': 'Archivos vacíos'}), 400


    if not allowed_file(cv_file.filename) or not allowed_file(req_file.filename):
        return jsonify({'error': 'Tipo de archivo no permitido. Solo PDF.'}), 400


    cv_filename = secure_filename(cv_file.filename)
    req_filename = secure_filename(req_file.filename)


    cv_path = os.path.join(app.config['UPLOAD_FOLDER'], cv_filename)
    req_path = os.path.join(app.config['UPLOAD_FOLDER'], req_filename)


    try:
        cv_file.save(cv_path)
        req_file.save(req_path)
    except Exception as e:
        return jsonify({'error': f'No se pudieron guardar los archivos: {str(e)}'}), 500


    print(f"✅ CV guardado en: {cv_path}")
    print(f"✅ Requisitos guardado en: {req_path}")


    resultado = comparar_textos(cv_path, req_path)
    return jsonify({'resultado': resultado})


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)


