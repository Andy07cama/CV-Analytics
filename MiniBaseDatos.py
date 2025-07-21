from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from ComparadorDeTexto import comparar_textos
import LectorDeTextos

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("pantalla_principal.html")

@app.route("/subir")
def subir():
    return render_template("index.html")

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

    texto_cv = LectorDeTextos.extraer_texto_pdf(cv_path)
    texto_req = LectorDeTextos.extraer_texto_pdf(req_path)
    
    if not texto_cv.strip() or not texto_req.strip():
        return render_template("resultado.html", similitud="0%", feedback="❗ No se pudo leer el contenido de uno o ambos archivos PDF. Verificá que no estén vacíos y que tengan texto real.")

    resultado = comparar_textos(texto_cv, texto_req)

    similitud = f"{resultado[0]:.2f}%"
    feedback = resultado[1]
    return render_template("resultado.html", similitud=similitud, feedback=feedback)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
