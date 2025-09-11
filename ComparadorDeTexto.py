import google.generativeai as genai

def comparar_textos(texto_cv, texto_req):
    """
    Compara un CV con los requisitos de un puesto usando la API de Gemini.
    Devuelve (porcentaje, feedback).
    """

    prompt = f"""
    Actúa como un experto en selección de personal.
    Analiza la compatibilidad entre el siguiente CV y los requisitos del puesto.

    CV:
    {texto_cv}

    REQUISITOS:
    {texto_req}

    Indica SOLO lo siguiente en tu respuesta:
    - Un porcentaje de similitud en número (0 a 100).
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        texto_respuesta = response.text.strip()

        # Buscar porcentaje en el texto
        import re
        match = re.search(r"(\d{1,3})", texto_respuesta)
        if match:
            porcentaje = int(match.group(1))
        else:
            porcentaje = 0

        # El resto del texto es feedback
        feedback = texto_respuesta.replace(str(porcentaje), "").strip()

        return porcentaje, feedback

    except Exception as e:
        return 0, f"❗ Error al usar Gemini: {str(e)}"
