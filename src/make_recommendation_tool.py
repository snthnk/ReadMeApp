from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from books_db import books


def make_recommendation(user_tags, user_authors, user_types):

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

    # Сортируем книги по степени соответствия предпочтениям
    recommended_books = sorted(zip(books, similarities), key=lambda x: x[1], reverse=True)

    recommend_book = recommended_books[max(recommended_books, key=recommended_books.get)]
    return f"{recommend_book['title']} (Автор: {recommend_book['author']}, Тип: {recommend_book['type']})"