from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from books_db import books

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def make_recommendation(user_tags, user_authors, user_types):
    # Преобразуем автора и типы пользователя в списки, если они не списки
    if isinstance(user_tags, str):
        user_tags = [user_tags]
    if isinstance(user_authors, str):
        user_authors = [user_authors]
    if isinstance(user_types, str):
        user_types = [user_types]

    # Объединяем все теги, авторов и типы для каждой книги в одну строку
    book_data = [
        " ".join(book["tags"] + [book["author"]] + [book["type"]]) for book in books
    ]

    # Объединяем предпочтения пользователя в одну строку
    user_preferences = " ".join(user_tags + user_authors + user_types)

    # Преобразуем данные в векторное представление с помощью CountVectorizer
    vectorizer = CountVectorizer().fit(book_data + [user_preferences])
    book_vectors = vectorizer.transform(book_data)
    user_vector = vectorizer.transform([user_preferences])

    # Рассчитываем косинусное сходство между книгами и предпочтениями пользователя
    similarities = cosine_similarity(user_vector, book_vectors).flatten()

    # Сортируем книги по степени соответствия предпочтениям и берем топ-3
    recommended_books = sorted(zip(books, similarities), key=lambda x: x[1], reverse=True)[:3]

    # Возвращаем список из топ-3 рекомендованных книг
    return [book for book, similarity in recommended_books]



