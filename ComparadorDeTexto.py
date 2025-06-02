from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def comparar_textos(cv, requisitos):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([cv, requisitos])
    similitud = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    porcentaje = similitud * 100


    if porcentaje > 75:
        feedback = "🟢 ¡Tenés altas chances de ser aceptado para este trabajo!"
    elif porcentaje > 50:
        feedback = "🟡 Cumplís con algunos requisitos, pero podrías mejorar tu CV."
    else:
        feedback = "🔴 Te faltan varios requisitos. Intentá reforzar tu CV."


    return porcentaje, feedback
