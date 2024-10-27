import tkinter as tk
from tkinter import filedialog, font
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
        custom_font_path = "assets/fonts/YourFontName.ttf"  # Убедись, что путь к шрифту правильный
        self.custom_font = font.Font(family="CustomFont", size=14)
        self.master.option_add("*Font", self.custom_font)

        # Главный экран
        self.label = ctk.CTkLabel(
            master,
            text="Добро пожаловать в ReadMe!",
            fg_color=Colors.BACKGROUND_COLOR,
            text_color=Colors.TEXT_COLOR,
            font=("CustomFont", 24, "bold")
        )
        self.label.pack(pady=40)

        # Создание кнопок
        self.create_button(master, "Загрузить книгу", self.load_book)
        self.create_button(master, "Найти книгу по интересам", self.find_book_by_interest)

        # Логотип снизу
        self.display_logo(master)

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
            # Здесь можно добавить логику для обработки файла
            print(f"Книга загружена: {file_path}")

    def find_book_by_interest(self):
        # Логика поиска книги по интересам
        print("Функция поиска книги по интересам не реализована")


