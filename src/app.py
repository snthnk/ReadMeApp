import tkinter as tk
from tkinter import messagebox
from src.gui import BookGUI


class BookApp:
    def __init__(self, master):
        self.master = master
        master.title("ReadMe - Приложение для чтения книг")

        # Инициализация GUI
        self.gui = BookGUI(master)

    def load_book(self, file_path):
        if file_path.endswith('.txt'):
            # Загрузка книги и вызов метода для обработки текста
            with open(file_path, 'r', encoding='utf-8') as file:
                book_content = file.read()
            messagebox.showinfo("Информация", "Книга успешно загружена!")
            return book_content
        else:
            messagebox.showerror("Ошибка", "Формат файла должен быть .txt")

    def find_books(self, preferences):
        # Логика поиска книг по интересам
        # Пока заглушка, позже можно связать с базой данных
        return ["Книга 1", "Книга 2", "Книга 3"]
