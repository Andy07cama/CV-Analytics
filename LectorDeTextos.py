import pdfplumber
import re
import unicodedata
from datetime import datetime
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from PIL import Image
import os

#pip install pdfplumber

#pip install pytesseract
#pytesseract necesita Tesseract OCR instalado en tu sistema:Windows:
#Descargá el instalador desde Tesseract OCR
#y anotá la ruta de instalación (ej: C:\Program Files\Tesseract-OCR\tesseract.exe).
#En tu lectordetextos.py si estás en Windows, descomentá y ajustá:
#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#pip install pillow
#pip install re


def extraer_texto_pdf(ruta_pdf):
    texto = ""
    with pdfplumber.open(ruta_pdf) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text() + "\n"
    return texto

def extraer_texto_imagen(ruta_imagen):
    """Extrae texto desde una imagen (JPG, PNG, etc.) usando OCR."""
    try:
        img = Image.open(ruta_imagen)
        texto = pytesseract.image_to_string(img, lang="spa")  # OCR en español
        return texto
    except Exception as e:
        print(f"Error al leer imagen: {e}")
        return ""


def extraer_texto_archivo(ruta_archivo):
    """Detecta el tipo de archivo (PDF o imagen) y aplica el método correcto."""
    extension = os.path.splitext(ruta_archivo)[1].lower()
    if extension == ".pdf":
        return extraer_texto_pdf(ruta_archivo)
    elif extension in [".png", ".jpg", ".jpeg"]:
        return extraer_texto_imagen(ruta_archivo)
    else:
        print(f"⚠️ Tipo de archivo no soportado: {extension}")
        return ""


def normalizar_texto(texto: str) -> str:
    """
    Normaliza: pasa a minúsculas, elimina acentos/diacríticos y 
    conserva solo letras, dígitos, espacios y separadores útiles (/-:).
    Colapsa espacios múltiples a 1.
    """
    if not isinstance(texto, str):
        return ""
    t = texto.lower()
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"[^a-z0-9 /\-:]", " ", t)   # conserva / - :
    t = re.sub(r"\s+", " ", t).strip()
    return t

def _calcular_edad(fecha_nac: datetime.date) -> int:
    hoy = datetime.now().date()
    return hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))

def extraer_edad(texto: str) -> str:
    """
    Estrategia:
    1) Busca 'edad: XX' (o variaciones con 'años/anios/years').
    2) Si no, intenta fecha de nacimiento en formato dd/mm/yyyy o dd-mm-yyyy.
    3) Si no, intenta '15 marzo 1998' (nombre de mes).
    4) Si no, intenta un año suelto junto a 'nacimiento'/'f. nac'.
    Devuelve str con la edad o 'No especificada'.
    """
    t = normalizar_texto(texto)

    # 1) EDAD DIRECTA: 'edad: 28', 'edad 28 anos'
    m = re.search(r"\bedad\s*[:\-]?\s*(\d{1,2})\s*(?:anos|anios|years)?\b", t)
    if m:
        try:
            edad = int(m.group(1))
            if 14 <= edad <= 99:
                return str(edad)
        except ValueError:
            pass

    # 2) FECHA DE NACIMIENTO NUMERICA: 'fecha de nacimiento: 01/05/1995' o '15-08-2000'
    m = re.search(
        r"\b(?:fecha\s*de\s*nacimiento|nacimiento|f\s*\.?\s*nac)\s*[:\-]?\s*(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2,4})\b",
        t
    )
    if m:
        d, mo, y = m.groups()
        try:
            d, mo, y = int(d), int(mo), int(y)
            if y < 100:  # Manejo de año a 2 dígitos (opcional)
                y += 1900 if y > (datetime.now().year % 100) else 2000
            fecha = datetime(y, mo, d).date()
            edad = _calcular_edad(fecha)
            if 14 <= edad <= 99:
                return str(edad)
        except ValueError:
            pass

    # 3) FECHA CON NOMBRE DE MES: '15 marzo 1998', con o sin prefijo 'nacimiento'
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
        "julio": 7, "agosto": 8, "septiembre": 9, "setiembre": 9, "octubre": 10,
        "noviembre": 11, "diciembre": 12
    }
    m = re.search(
        r"\b(?:fecha\s*de\s*nacimiento|nacimiento|nacido(?:a)?\s*el)?\s*[:\-]?\s*(\d{1,2})\s+"
        r"(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|setiembre|octubre|noviembre|diciembre)\s+(\d{4})\b",
        t
    )
    if m:
        try:
            d = int(m.group(1))
            mo = meses[m.group(2)]
            y = int(m.group(3))
            fecha = datetime(y, mo, d).date()
            edad = _calcular_edad(fecha)
            if 14 <= edad <= 99:
                return str(edad)
        except ValueError:
            pass

    # 4) SOLO AÑO CERCA DE 'NACIMIENTO' (evita confundir años de empleo/estudios)
    m = re.search(r"\b(?:fecha\s*de\s*nacimiento|nacimiento|f\s*\.?\s*nac)\s*[:\-]?\s*(\d{4})\b", t)
    if m:
        try:
            y = int(m.group(1))
            # Tomamos 1 de julio como aproximación para evitar sesgo por mes/día desconocidos
            fecha = datetime(y, 7, 1).date()
            edad = _calcular_edad(fecha)
            if 14 <= edad <= 99:
                return str(edad)
        except ValueError:
            pass

    return "No especificada"

def extraer_estudios(texto):
    estudios = []
    for linea in texto.split("\n"):
        if "universidad" in linea.lower() or "licenciatura" in linea.lower():
            estudios.append(linea.strip())
    return estudios


def extraer_experiencia_laboral(texto):
    experiencias = []
    for linea in texto.split("\n"):
        if "trabajé en" in linea.lower() or "experiencia laboral" in linea.lower():
            experiencias.append(linea.strip())
    return experiencias
