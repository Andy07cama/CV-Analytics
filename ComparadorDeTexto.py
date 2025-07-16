from sentence_transformers import SentenceTransformer, util
import re
import nltk
import string
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('spanish'))
nltk.data.path.append("nltk_data")

model = SentenceTransformer('distiluse-base-multilingual-cased-v1')

def limpiar_texto(texto):
    texto = texto.translate(str.maketrans("", "", string.punctuation))
    palabras = texto.split()
    palabras_limpias = [p for p in palabras if p.lower() not in stop_words]
    return ' '.join(palabras_limpias)

def detectar_rango_edad(texto_requisitos, edad_cv):
    if not edad_cv:
        return True
    try:
        edad_cv = int(edad_cv)
        rango = re.search(r'entre\s+(\d{2})\s+y\s+(\d{2})\s+años', texto_requisitos.lower())
        if rango:
            min_edad = int(rango.group(1))
            max_edad = int(rango.group(2))
            return min_edad <= edad_cv <= max_edad
    except:
        pass
    return True

def comparar_textos(texto_cv, texto_req):
    from LectorDeTextos import extraer_edad, extraer_estudios, extraer_experiencia_laboral

    texto_cv_limpio = limpiar_texto(texto_cv)
    estudios = limpiar_texto(" ".join(extraer_estudios(texto_cv)))
    experiencia = limpiar_texto(" ".join(extraer_experiencia_laboral(texto_cv)))
    texto_cv_ponderado = (
        texto_cv_limpio +
        " " + (estudios + " ") * 3 +
        " " + (experiencia + " ") * 4
    )
    texto_req_limpio = limpiar_texto(texto_req)

    #print(texto_cv_limpio)
    #print(texto_req_limpio)

    emb_cv = model.encode(texto_cv_ponderado, convert_to_tensor=True)
    emb_req = model.encode(texto_req_limpio, convert_to_tensor=True)

    similitud = float(util.pytorch_cos_sim(emb_cv, emb_req)[0][0])
    porcentaje = similitud * 100

    edad = extraer_edad(texto_cv)
    edad_ok = detectar_rango_edad(texto_req, edad)

    if porcentaje > 75 and edad_ok:
        feedback = "🟢 ¡Tenés altas chances de ser aceptado para este trabajo!"
    elif porcentaje > 50:
        feedback = "🟡 Cumplís con algunos requisitos, pero podrías mejorar tu CV."
    else:
        feedback = "🔴 Te faltan varios requisitos. Intentá reforzar tu CV."

    return porcentaje, feedback
