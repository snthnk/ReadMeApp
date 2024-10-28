import os
import tkinter as tk
from tkinter import filedialog, font, messagebox
from src.styles import Colors
import customtkinter as ctk
from PIL import Image, ImageTk
from src.make_recommendation_tool import make_recommendation  # Импорт функции make_recommendation


class BookGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("ReadMe")
        self.master.geometry("800x600")
        self.master.configure(bg=Colors.BACKGROUND_COLOR)

        # Загрузка пользовательского шрифта
        custom_font_path = "assets/fonts/Outfit-Black.ttf"
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

        back_icon = Image.open("assets/images/icons/prev.png").resize((20, 20), Image.LANCZOS)
        self.back_icon_photo = ImageTk.PhotoImage(back_icon)

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
            corner_radius=15,
            command=command
        )
        button.pack(pady=20)

    def display_logo(self, master):
        # Загрузка изображения логотипа
        logo_path = "assets/images/logo.png"
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((150, 150), Image.LANCZOS)
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
            book_name = os.path.basename(file_path)
            destination = os.path.join("books", book_name)
            os.rename(file_path, destination)
            print(f"Книга загружена: {destination}")

    def find_book_by_interest(self):
        # Очистка основного экрана
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Назад к главному экрану
        back_button = ctk.CTkButton(
            self.main_frame,
            text="Назад",
            command=self.create_main_screen,
            fg_color=Colors.BUTTON_COLOR,
            text_color=Colors.BUTTON_TEXT_COLOR,
            font=("CustomFont", 14),
            width=120,
            height=40,
            corner_radius=10
        )
        back_button.pack(side="top", anchor="nw", padx=10, pady=10)

        # Заголовок
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="Выберите интересы для поиска книги",
            font=("CustomFont", 24, "bold"),
            fg_color=Colors.BACKGROUND_COLOR,
            text_color=Colors.TEXT_COLOR
        )
        title_label.pack(pady=20)

        # Поле для ввода автора
        author_label = ctk.CTkLabel(self.main_frame, text="Автор:")
        author_label.pack()
        author_entry = ctk.CTkEntry(self.main_frame, width=300)
        author_entry.pack(pady=5)

        # Кнопки выбора тегов
        self.selected_tags = []
        tags = ["классика", "мистика", "философия", "любовь", "антиутопия", "фантастика", "приключения", "драма"]
        for tag in tags:
            tag_button = ctk.CTkCheckBox(
                self.main_frame,
                text=tag,
                command=lambda t=tag: self.toggle_tag(t)
            )
            tag_button.pack(pady=2)

        # Кнопки выбора типа книги
        self.selected_type = tk.StringVar()
        types = ["роман", "фэнтези", "научно-популярная", "триллер", "драма"]
        for t in types:
            type_button = ctk.CTkRadioButton(
                self.main_frame,
                text=t,
                variable=self.selected_type,
                value=t
            )
            type_button.pack(pady=2)

        # Кнопка поиска
        search_button = ctk.CTkButton(
            self.main_frame,
            text="Найти книгу",
            command=lambda: self.show_recommendation(
                author_entry.get(),
                self.selected_tags,
                self.selected_type.get()
            )
        )
        search_button.pack(pady=20)

    def toggle_tag(self, tag):
        if tag in self.selected_tags:
            self.selected_tags.remove(tag)
        else:
            self.selected_tags.append(tag)

    def show_recommendation(self, tags, author, book_type):
        # Получаем рекомендации
        recommended_books = make_recommendation(tags, author, book_type)

        # Очистка предыдущего содержимого
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        if recommended_books:
            recommendation_text = ""
            for book in recommended_books:
                recommendation_text += (
                    f"Рекомендуемая книга: {book['title']}\n"
                    f"Автор: {book['author']}\n"
                    f"Тип: {book['type']}\n"
                    f"Теги: {', '.join(book['tags'])}\n"
                    "-------------------------\n"
                )
        else:
            recommendation_text = "Рекомендации не найдены."

        recommendation_label = ctk.CTkLabel(
            self.main_frame,
            text=recommendation_text,
            fg_color=Colors.BACKGROUND_COLOR,
            text_color=Colors.TEXT_COLOR,
            font=("CustomFont", 18),
            wraplength=700,
            justify="left"
        )
        recommendation_label.pack(pady=20)

        # Добавляем кнопку "Назад"
        back_button = ctk.CTkButton(
            self.main_frame,
            text=" Назад",
            image=self.back_icon_photo,
            command=self.create_main_screen,
            fg_color=Colors.BUTTON_COLOR,
            text_color=Colors.BUTTON_TEXT_COLOR,
            font=("CustomFont", 14),
            width=120,
            height=40,
            corner_radius=10
        )
        back_button.pack(side="left", padx=10, pady=10)

    def show_book_list(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(
            self.main_frame,
            text="Список книг",
            font=("CustomFont", 28, "bold"),
            fg_color=Colors.BACKGROUND_COLOR,
            text_color=Colors.TEXT_COLOR
        )
        title_label.pack(pady=10)

        books = self.get_books_from_directory("books")
        if not books:
            messagebox.showinfo("Список книг", "Нет загруженных книг.")
            self.create_main_screen()
            return

        for book in books:
            book_button = ctk.CTkButton(
                self.main_frame,
                text=book,
                command=lambda b=book: self.open_book(b),
                fg_color=Colors.BUTTON_COLOR,
                text_color=Colors.BUTTON_TEXT_COLOR,
                font=("CustomFont", 18),
                width=400,
                height=80,
                corner_radius=15
            )
            book_button.pack(pady=5)


        back_button = ctk.CTkButton(
            self.main_frame,
            image=self.back_icon_photo,
            text=" Назад",
            command=self.create_main_screen,
            fg_color=Colors.BUTTON_COLOR,
            text_color=Colors.BUTTON_TEXT_COLOR,
            font=("CustomFont", 14),
            width=120,
            height=40,
            corner_radius=10
        )
        back_button.pack(side="left", padx=10, pady=10)

    def get_books_from_directory(self, directory):
        return [f for f in os.listdir(directory) if f.endswith('.txt')]

    def open_book(self, book_name):
        book_path = os.path.join("books", book_name)
        encodings = ['utf-8', 'latin-1', 'cp1251']

        for encoding in encodings:
            try:
                with open(book_path, "r", encoding=encoding) as file:
                    book_content = file.read()
                break
            except UnicodeDecodeError:
                continue

        # Отображение содержимого книги
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        back_button = ctk.CTkButton(
            self.main_frame,
            text="Назад",
            command=self.show_book_list,
            fg_color=Colors.BUTTON_COLOR,
            text_color=Colors.BUTTON_TEXT_COLOR,
            font=("CustomFont", 14),
            width=120,
            height=40,
            corner_radius=10
        )
        back_button.pack(side="top", anchor="nw", padx=10, pady=10)

        text_box = tk.Text(self.main_frame, wrap="word", font=("CustomFont", 14), bg=Colors.BACKGROUND_COLOR)
        text_box.insert("1.0", book_content)
        text_box.config(state="disabled")
        text_box.pack(fill="both", expand=True, padx=10, pady=10)















