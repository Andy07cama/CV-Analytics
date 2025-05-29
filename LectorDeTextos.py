import pdfplumber
import re

def extraer_texto_pdf(ruta_pdf):
    texto = ""
    with pdfplumber.open(ruta_pdf) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text() + "\n"
    return texto
    
def extraer_edad(texto):
    import re
    coincidencias = re.findall(r'Edad\s*[:\-]?\s*(\d{2})', texto)
    if coincidencias:
        return coincidencias[0] 
    return None

def extraer_estudios(texto):
    estudios = []
    lineas = texto.split("\n")
    for linea in lineas:
        if "universidad" in linea.lower() or "licenciatura" in linea.lower():
            estudios.append(linea.strip())
    return estudios

def extraer_experiencia_laboral(texto):
    experiencias = []
    lineas = texto.split("\n")
    for linea in lineas:
        if "trabajé en" in linea.lower() or "experiencia laboral" in linea.lower():
            experiencias.append(linea.strip())
    return experiencias



texto = extraer_texto_pdf("cv_ejemplo.pdf")

edad = extraer_edad(texto)
estudios = extraer_estudios(texto)
experiencia = extraer_experiencia_laboral(texto)
