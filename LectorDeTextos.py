import pdfplumber
import re

def extraer_texto_pdf(ruta_pdf):
    texto = ""
    with pdfplumber.open(ruta_pdf) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text() + "\n"
    return texto


def extraer_edad(texto):
    coincidencias = re.findall(r'Edad\s*[:\-]?\s*(\d{2})', texto)
    if coincidencias:
        return coincidencias[0]
    return "No especificada"

#import unicodedata
#from datetime import datetime

def extraer_texto_pdf(ruta_pdf):
    texto = ""
    with pdfplumber.open(ruta_pdf) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text() + "\n"
    return texto

#def normalizar_texto(texto):
 #   texto = texto.lower()
  #  texto = "".join(c for c in texto if c.isalnum() or c.isspace())
   # texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("utf-8")
    #texto = re.sub(r"\s+", "" , texto).strip()
    #return texto

#def extraer_edad(texto):
 #   texto_normalizado = normalizar_texto(texto)
    
  #  coincidencias_edad = re.findall(r"edad\s*[:\-]?\s*(\d{1,2})\s*(?:anos|anios|years)?", texto_normalizado)
   # if coincidencias_edad:
    #    return coincidencias_edad[0]

    #patrones_fecha_nacimiento = 
    #[
     #   r"fecha de nacimiento\s*[:\-]?\s*(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})",
      #  r"nacimiento\s*[:\-]?\s*(\d{1,2}\s*(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s*\d{4})",
       # r"(\d{4})"
    #]
    
    #for patron in patrones_fecha_nacimiento:
     #   coincidencias_fecha = re.findall(patron, texto_original.lower())
      #  if coincidencias_fecha:
       #     fecha_str = coincidencias_fecha[0]
        #    try:
         #       if re.match(r"\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}", fecha_str):
          #          if "-" in fecha_str:
           #             fecha_nac = datetime.strptime(fecha_str, "%d-%m-%Y")
            #        else:
             #           fecha_nac = datetime.strptime(fecha_str, "%d/%m/%Y")
              #  elif re.match(r"\d{1,2}\s*(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s*\d{4}", fecha_str):
               #     meses = {
                #        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
                 #       'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
                  #  }
                   # partes = fecha_str.split()
                    #dia = int(partes[0])
                    #mes = meses[partes[1]]
                    #año = int(partes[2])
                    #fecha_nac = datetime(anio, mes, dia)
                #elif re.match(r"\d{4}", fecha_str) and len(fecha_str) == 4:
                 #   anio_nac = int(fecha_str)
                  #  edad_calc = datetime.now().year - anio_nac
                   # if 18 <= edad_calc <= 99:
                    #    return str(edad_calc)
                    #continue

                #today = datetime.now()
                #edad_calc = today.year - fecha_nac.year - ((today.month, today.day) < (fecha_nac.month, fecha_nac.day))
                #if 18 <= edad_calc <= 99:
                 #   return str(edad_calc)
            #except ValueError:
             #   pass
    #return "No especificada"


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
