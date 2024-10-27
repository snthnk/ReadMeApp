import os
import tkinter as tk
from tkinter import filedialog, font, messagebox
from src.styles import Colors
import customtkinter as ctk
from PIL import Image, ImageTk


class BookGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("ReadMe")
        self.master.geometry("800x600")
        self.master.configure(bg=Colors.BACKGROUND_COLOR)

        # Загрузка пользовательского шрифта
        custom_font_path = "assets/fonts/YourFontName.ttf"  # Убедитесь, что путь к шрифту правильный
        self.custom_font = font.Font(family="CustomFont", size=14)
        self.master.option_add("*Font", self.custom_font)

        # Инициализация главного экрана
        self.main_frame = ctk.CTkFrame(master, fg_color=Colors.BACKGROUND_COLOR)
        self.main_frame.pack(fill="both", expand=True)

        self.create_main_screen()

    def create_main_screen(self):
        # Очистка предыдущего содержимого
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Главный экран
        self.label = ctk.CTkLabel(
            self.main_frame,
            text="Добро пожаловать в ReadMe!",
            fg_color=Colors.BACKGROUND_COLOR,
            text_color=Colors.TEXT_COLOR,
            font=("CustomFont", 24, "bold")
        )
        self.label.pack(pady=40)

        # Создание кнопок
        self.create_button(self.main_frame, "Загрузить книгу", self.load_book)
        self.create_button(self.main_frame, "Найти книгу по интересам", self.find_book_by_interest)
        self.create_button(self.main_frame, "Список книг", self.show_book_list)

        # Логотип снизу
        self.display_logo(self.main_frame)

    def create_button(self, master, text, command):
        # Создание кнопок с закругленными углами
        button = ctk.CTkButton(
            master,
            text=text,
            fg_color=Colors.BUTTON_COLOR,
            text_color=Colors.BUTTON_TEXT_COLOR,
            font=("CustomFont", 20),
            width=300,
            height=60,
            corner_radius=15,  # Радиус закругления углов
            command=command
        )
        button.pack(pady=20)

    def display_logo(self, master):
        # Загрузка изображения логотипа
        logo_path = "assets/images/logo.png"
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((150, 150), Image.LANCZOS)  # Изменение размера изображения логотипа
        self.logo_photo = ImageTk.PhotoImage(logo_image)

        # Отображение логотипа
        logo_label = ctk.CTkLabel(
            master,
            image=self.logo_photo,
            fg_color=Colors.BACKGROUND_COLOR
        )
        logo_label.pack(side="bottom", pady=20)

    def load_book(self):
        # Логика загрузки книги (только .txt)
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt")],
            title="Выберите книгу для загрузки"
        )
        if file_path:
            # Сохранение книги в папку "books"
            book_name = os.path.basename(file_path)
            destination = os.path.join("books", book_name)
            os.rename(file_path, destination)  # Перемещение книги в папку "books"
            print(f"Книга загружена: {destination}")

    def find_book_by_interest(self):
        # Логика поиска книги по интересам
        print("Функция поиска книги по интересам не реализована")

    def show_book_list(self):
        # Очистка предыдущего содержимого
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Заголовок
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="Список книг",
            font=("CustomFont", 28, "bold"),  # Увеличенный размер текста заголовка
            fg_color=Colors.BACKGROUND_COLOR,
            text_color=Colors.TEXT_COLOR
        )
        title_label.pack(pady=10)

        # Получение списка книг из папки "books"
        books = self.get_books_from_directory("books")
        if not books:
            messagebox.showinfo("Список книг", "Нет загруженных книг.")
            self.create_main_screen()  # Возвращаемся на главный экран, если книг нет
            return

        # Кнопки для каждой книги
        for book in books:
            book_button = ctk.CTkButton(
                self.main_frame,
                text=book,
                command=lambda b=book: self.open_book(b),
                fg_color=Colors.BUTTON_COLOR,  # Цвет кнопки книги из класса Colors
                text_color=Colors.BUTTON_TEXT_COLOR,  # Цвет текста кнопки книги из класса Colors
                font=("CustomFont", 18),  # Размер шрифта для кнопки книги
                width=400,  # Ширина кнопки книги
                height=80,  # Высота кнопки книги
                corner_radius=15
            )
            book_button.pack(pady=5)

        # Кнопка "Назад" в левом нижнем углу
        back_icon = Image.open("assets/images/icons/prev.png").resize((20, 20), Image.LANCZOS)
        self.back_icon_photo = ImageTk.PhotoImage(back_icon)

        back_button = ctk.CTkButton(
            self.main_frame,
            image=self.back_icon_photo,
            text=" Назад",
            command=self.create_main_screen,
            fg_color=Colors.BUTTON_COLOR,
            text_color=Colors.BUTTON_TEXT_COLOR,
            font=("CustomFont", 14),  # Размер шрифта для кнопки назад
            width=120,  # Ширина кнопки назад
            height=40,  # Высота кнопки назад
            corner_radius=10
        )
        back_button.pack(side="left", padx=10, pady=10)  # Размещение кнопки "Назад" в левом нижнем углу

    def get_books_from_directory(self, directory):
        # Получение списка названий книг из указанной директории
        return [f for f in os.listdir(directory) if f.endswith('.txt')]

    def open_book(self, book_name):
        book_path = os.path.join("books", book_name)
        encodings = ['utf-8', 'latin-1', 'cp1251']  # Список кодировок для проверки

        for encoding in encodings:
            try:
                with open(book_path, 'r', encoding=encoding) as book_file:
                    content = book_file.readlines()
                break  # Если файл успешно прочитан, выходим из цикла
            except UnicodeDecodeError:
                continue  # Пытаемся следующую кодировку

        # Открытие нового окна для отображения книги
        self.book_window = tk.Toplevel(self.master)
        self.book_window.title(book_name)
        self.book_window.geometry("800x600")
        self.book_window.configure(bg=Colors.BACKGROUND_COLOR)

        # Заголовок книги
        title_label = ctk.CTkLabel(
            self.book_window,
            text=book_name,
            font=("CustomFont", 24, "bold"),
            fg_color=Colors.BACKGROUND_COLOR,
            text_color=Colors.TEXT_COLOR
        )
        title_label.pack(pady=10)

        # Текстовая область для отображения страницы
        self.page_text = tk.Text(self.book_window, wrap=tk.WORD, bg="white", fg="black", font=("CustomFont", 16))
        self.page_text.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Инициализация переменных для управления страницами
        self.content = content
        self.current_page = 0

        # Кнопка "Назад" для возврата к списку книг
        back_button = ctk.CTkButton(
            self.book_window,
            image=self.back_icon_photo,
            text=" Назад",
            command=self.book_window.destroy,
            fg_color=Colors.BUTTON_COLOR,
            text_color=Colors.BUTTON_TEXT_COLOR,
            font=("CustomFont", 14),
            width=120,
            height=40,
            corner_radius=10
        )
        back_button.pack(side="left", padx=10, pady=10)

        # Кнопка "Назад" для листания
        prev_icon = Image.open("assets/images/icons/prev.png").resize((20, 20), Image.LANCZOS)
        self.prev_icon_photo = ImageTk.PhotoImage(prev_icon)

        prev_button = ctk.CTkButton(
            self.book_window,
            image=self.prev_icon_photo,
            command=lambda: self.change_page(-1),
            fg_color=Colors.BUTTON_COLOR,
            text_color=Colors.BUTTON_TEXT_COLOR,
            font=("CustomFont", 14),
            width=60,
            height=40,
            corner_radius=10
        )
        prev_button.pack(side="left", padx=10, pady=10)

        # Кнопка "Вперед" для листания
        next_icon = Image.open("assets/images/icons/next.png").resize((20, 20), Image.LANCZOS)
        self.next_icon_photo = ImageTk.PhotoImage(next_icon)

        next_button = ctk.CTkButton(
            self.book_window,
            image=self.next_icon_photo,
            command=lambda: self.change_page(1),
            fg_color=Colors.BUTTON_COLOR,
            text_color=Colors.BUTTON_TEXT_COLOR,
            font=("CustomFont", 14),
            width=60,
            height=40,
            corner_radius=10
        )
        next_button.pack(side="left", padx=10, pady=10)

        # Метка для отображения номера текущей страницы
        self.page_label = ctk.CTkLabel(
            self.book_window,
            text=f"Страница {self.current_page + 1} из {len(self.content)}",
            fg_color=Colors.BACKGROUND_COLOR,
            text_color=Colors.TEXT_COLOR,
            font=("CustomFont", 14)
        )
        self.page_label.pack(side="bottom", pady=10)

        # Инициализация отображения первой страницы
        self.display_page()

    def change_page(self, direction):
        # Изменение текущей страницы и обновление отображения
        new_page = self.current_page + direction
        if 0 <= new_page < len(self.content):
            self.current_page = new_page
            self.display_page()

    def display_page(self):
        # Отображение текста текущей страницы
        self.page_text.delete(1.0, tk.END)  # Очистка текстовой области
        self.page_text.insert(tk.END, self.content[self.current_page])  # Вставка текста текущей страницы

        # Обновление метки с номером страницы
        self.page_label.configure(text=f"Страница {self.current_page + 1} из {len(self.content)}")









