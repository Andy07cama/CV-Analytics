from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import LectorDeTextos
from ComparadorDeTexto import comparar_textos
import google.generativeai as genai

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

try:
    
    API_KEY = "..." 
    
    if not API_KEY or API_KEY == "TU_NUEVA_API_KEY":
        print("ADVERTENCIA: No se ha configurado una clave de API de Gemini en MiniBaseDatos.py.")
        API_KEY = None
    else:
        genai.configure(api_key=API_KEY)
except Exception as e:
    print(f"Error fatal al configurar la API de Gemini: {e}")
    API_KEY = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generar_sugerencias_con_gemini(texto_cv, texto_req):
    """
    Usa la API de Gemini para generar sugerencias de mejora para el CV con un prompt detallado.
    """
    if not API_KEY:
        return "Error de Configuración\nNo se pueden generar sugerencias porque la clave de API de Gemini no ha sido configurada correctamente en el archivo `MiniBaseDatos.py`."

    prompt = f"""
    Rol: Eres un asistente experto en Recursos Humanos y especialista en selector de carrera profesional.

    Tarea: Analiza el siguiente currículum (texto_cv) en el contexto de los requisitos para el puesto de trabajo (texto_req). Tu objetivo es proporcionar consejos constructivos en lista y enumerados y accionables para que el candidato pueda mejorar su CV y aumentar sus posibilidades de ser seleccionado.

    Contexto:
    CV DEL CANDIDATO:
    {texto_cv}
    REQUISITOS DEL PUESTO:
    {texto_req}

    Instrucciones para la respuesta:
    1.  No inventes información: Basa tus sugerencias únicamente en la información proporcionada.
    2.  Sé constructivo: Enfócate en cómo mejorar y adaptar lo que ya existe, en lugar de solo señalar las carencias.
    3.  Formato de Salida: Genera la respuesta en formato Markdown. Usa un encabezado principal y una lista de viñetas para las sugerencias. Cada sugerencia debe ser clara y explicar el "porqué" del cambio. Hacelo en lista mostrando 1./n 2./n y asi consecutivamente
    4.  Da solo 5 sugerencias no más
    5.  Al final de todo en un parrafo aparte pone lo que vos crees que tienen de acierto. Es decir, el porcentaje de probabilidad de que sea contratado para el trabajo con el cv actual.

    Ahora, genera las sugerencias para el CV y los requisitos proporcionados con las intrucciones proporcionadas.
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"[❗] Error al generar sugerencias con Gemini: {e}")
        error_message = f"⚠️ Error al contactar la API de Gemini\nNo se pudieron generar las sugerencias.\n\nDetalle del error: {str(e)}"
        return error_message

# --- RUTAS DE LA APLICACIÓN ---

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

    sugerencias = ""
    # Se generan sugerencias si la compatibilidad no es casi perfecta
    if resultado[0] < 95: 
        sugerencias = generar_sugerencias_con_gemini(texto_cv, texto_req)

    try:
        os.remove(cv_path)
        os.remove(req_path)
    except OSError as e:
        print(f"Error al eliminar archivos: {e}")

    return render_template("resultado.html", similitud=similitud, feedback=feedback, sugerencias=sugerencias)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)