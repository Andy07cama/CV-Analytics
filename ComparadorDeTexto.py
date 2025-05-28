from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Textos
cv = "Soy estudiante de programación con experiencia en HTML, CSS y trabajo en equipo."
requisitos = "Buscamos desarrollador web con experiencia en HTML, CSS y trabajo en equipo."
import LectorDeTextos #probar si esta conectado
print("Edad", LectorDeTextos)

# TF-IDF vectorización
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform([cv, requisitos])

# Similitud coseno
similitud = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
porcentaje = similitud * 100

print(f"Similitud entre CV y requisitos: {porcentaje:.2f}%")

# Feedback
if porcentaje > 75:
    print("🟢 ¡Tenés altas chances de ser aceptado para este trabajo!")
elif porcentaje > 50:
    print("🟡 Cumplís con algunos requisitos, pero podrías mejorar tu CV.")
else:
    print("🔴 Te faltan varios requisitos. Intentá reforzar tu CV.")