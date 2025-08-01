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
        return "⚠️ Error de Configuración\nNo se pueden generar sugerencias porque la clave de API de Gemini no ha sido configurada correctamente en el archivo `MiniBaseDatos.py`."

    prompt = f"""
    Rol: Eres un asistente experto en Recursos Humanos y un coach de carrera profesional. Tu tono debe ser profesional, alentador y constructivo.

    Tarea Principal: Analizar un CV en comparación con los requisitos de un puesto y generar un informe claro y accionable.

    Documentos para Análisis:
    ---
    CV DEL CANDIDATO:
    {texto_cv}
    ---
    REQUISITOS DEL PUESTO:
    {texto_req}
    ---

    FORMATO DE SALIDA OBLIGATORIO (MUY IMPORTANTE):
    Usa saltos de línea dobles (párrafos separados) entre cada punto de la lista.
    NO uses NINGÚN carácter de formato Markdown. No incluyas `#`, `*`, `-`, o cualquier otro símbolo de formato.
    La salida debe ser texto plano, estructurado exactamente como se describe a continuación.
    
    ESTRUCTURA EXACTA DE LA RESPUESTA:

    Sugerencias para Mejorar tu Perfil:

    1. [Aquí va la primera sugerencia, redactada en un párrafo completo. Explica el qué y el porqué de la sugerencia, conectando el CV con los requisitos del puesto.] n/

    2. [Aquí va la segunda sugerencia, en su propio párrafo.] n/

    3. [Aquí va la tercera sugerencia, en su propio párrafo.] n/ 

    4. [Aquí va la cuarta sugerencia, en su propio párrafo.] n/

    5. [Aquí va la quinta y última sugerencia, en su propio párrafo.] n/
 
    Evaluación Final:
    [En este párrafo final, proporciona una breve evaluación profesional sobre la adecuación general del candidato para el puesto y ofrece un porcentaje estimado de compatibilidad basado en tu análisis experto.]

    Instrucciones Adicionales sobre el Contenido:
    Sé Específico: No des consejos genéricos. Basa cada sugerencia en una discrepancia o área de mejora que observes entre el CV y los requisitos.
    Sé Constructivo: Enfócate en cómo el candidato puede adaptar y resaltar mejor su experiencia actual.
    Límite: Proporciona exactamente 5 sugerencias.
    No Inventes: Basa todo tu análisis estrictamente en los textos proporcionados.

    Ahora, genera el informe siguiendo todas estas instrucciones al pie de la letra.
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        # No es necesario procesar el texto, ya que le hemos pedido a la IA que lo genere limpio.
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