from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recipes.models import Recipes
from .models import RecipeSimilarity

def calculate_recipe_similarities(batch_size=100, top_n=5):
    RecipeSimilarity.objects.all().delete()
    print("RecipeSimilarity table data cleared.")

    recipes = list(Recipes.objects.all())
    if not recipes:
        print("No recipes found in the database to calculate similarities.")
        return

    titles = [recipe.title for recipe in recipes]
    ingredients = [recipe.ingredients if recipe.ingredients else "" for recipe in recipes]
    combined_features = [f"{title} {ingredients}" for title, ingredients in zip(titles, ingredients)]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(combined_features)
    print("TF-IDF matrix calculated.")

    cosine_sim = cosine_similarity(tfidf_matrix)

    # Save only the Top-N similarities
    bulk_data = []
    for i, recipe in enumerate(recipes):
        similar_indices = cosine_sim[i].argsort()[-top_n - 1:][::-1]  
        for idx in similar_indices:
            if idx != i and cosine_sim[i][idx] > 0.1:  # Similarity threshold
                bulk_data.append(RecipeSimilarity(
                    recipe=recipe,
                    similar_recipe=recipes[idx],
                    similarity_score=cosine_sim[i][idx]
                ))

            if len(bulk_data) >= batch_size:
                RecipeSimilarity.objects.bulk_create(bulk_data)
                bulk_data = []  # Clear the buffer after saving

    if bulk_data:
        RecipeSimilarity.objects.bulk_create(bulk_data)

    print("Similarities calculated and stored successfully.")
