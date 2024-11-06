import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk

# Загрузка данных nltk для токенизации
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

from nltk.tokenize import sent_tokenize

# Функция для чтения текста из файла с гибкой кодировкой
def read_text_file(file_path):
    try:
        # Попробуем открыть с кодировкой utf-8
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            return file.read()
    except UnicodeDecodeError:
        # Если utf-8 не работает, попробуем cp1251 (часто используется для русского текста)
        with open(file_path, 'r', encoding='cp1251') as file:
            return file.read()

# Разбитие текста на предложения
def split_into_sentences(text):
    """Токенизация текста в список предложений."""
    return sent_tokenize(text)

# Вычисление матрицы TF-IDF для предложений
def compute_tfidf(sentences):
    """Вычислить матрицу TF-IDF для списка предложений.

    Аргументы:
        sentences (list of str): Список предложений.

    Возвращает:
        scipy.sparse.csr_matrix: Матрица TF-IDF для предложений.
    """
    vectorizer = TfidfVectorizer()
    return vectorizer.fit_transform(sentences)

# Генерация резюме на основе TF-IDF для заданного количества предложений
def get_tfidf_summary(text, num_sentences):
    """Сделать резюме текста, выбирая предложения с наивысшими оценками TF-IDF.

    Аргументы:
        text (str): Входной текст для резюме.
        num_sentences (int): Количество предложений, включаемых в резюме.

    Возвращает:
        str: Сжатый текст, содержащий наиболее важные предложения.
    """
    sentences = split_into_sentences(text)
    if len(sentences) <= num_sentences:
        return text  # Вернуть полный текст, если он короче желаемого объёма.

    tfidf_matrix = compute_tfidf(sentences)
    sentence_scores = np.sum(tfidf_matrix.toarray(), axis=1)

    # Получение индексов верхних `num_sentences` предложений на основе оценок TF-IDF
    ranked_sentence_indices = np.argsort(sentence_scores)[-num_sentences:]

    # Создание резюме, упорядочивая выбранные предложения по их появлению
    summary = [sentences[i] for i in sorted(ranked_sentence_indices)]
    return ' '.join(summary)

# Функция для вычисления целевого количества предложений на основе страниц и дней
def calculate_target_sentences(pages_per_day, days, average_sentences_per_page=15):
    """Рассчитать целевое количество предложений.

    Аргументы:
        pages_per_day (int): Количество страниц, которые пользователь готов читать в день.
        days (int): Количество дней, за которые пользователь хочет прочитать книгу.
        average_sentences_per_page (int): Среднее количество предложений на странице (по умолчанию 15).

    Возвращает:
        int: Целевое количество предложений.
    """
    return pages_per_day * days * average_sentences_per_page

# Основная функция для сжатия текста
def compress_text(text, pages_per_day, days):
    """Сжать текст на основе количества страниц в день и дней.

    Аргументы:
        text (str): Входной текст для сжатия.
        pages_per_day (int): Количество страниц, которые пользователь готов читать в день.
        days (int): Количество дней, за которые пользователь хочет прочитать книгу.

    Возвращает:
        str: Сжатый текст, содержащий наиболее важные предложения.
    """
    target_sentences = calculate_target_sentences(pages_per_day, days)
    return get_tfidf_summary(text, target_sentences)
