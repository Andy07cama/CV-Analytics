from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import LectorDeTextos

# 1. Extraer texto desde el PDF
texto = LectorDeTextos.extraer_texto_pdf("cv_ejemplo.pdf")

# 2. Extraer datos individuales
edad = LectorDeTextos.extraer_edad(texto)
estudios = LectorDeTextos.extraer_estudios(texto)
experiencia = LectorDeTextos.extraer_experiencia_laboral(texto)

# 3. Construir texto del CV para análisis
cv = f"Tengo {edad} años. Estudios: {'Estudios ; '.join(estudios)}. Experiencia: {'; '.join(experiencia)}."

# 4. Texto de requisitos
requisitos = "Estudios: 2015 - 2019: Licenciatura en Ciencias de la Computación Universidad Nacional de. Experiencia: Experiencia Laboral; 2020 - Presente: Desarrollador Senior en Tech Solutions - Trabajé en el desarrollo"

# 5. TF-IDF vectorización
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform([cv, requisitos])

# 6. Similitud coseno
similitud = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
porcentaje = similitud * 100

# 7. Resultados
print(f"\nCV generado: {cv}\n")
print(f"Similitud entre CV y requisitos: {porcentaje:.2f}%")

# 8. Feedback
if porcentaje > 75:
    print("🟢 ¡Tenés altas chances de ser aceptado para este trabajo!")
elif porcentaje > 50:
    print("🟡 Cumplís con algunos requisitos, pero podrías mejorar tu CV.")
else:
    print("🔴 Te faltan varios requisitos. Intentá reforzar tu CV.")
