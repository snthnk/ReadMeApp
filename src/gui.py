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
        # Получение пути к книге
        book_path = os.path.join("books", book_name)
        encodings = ['utf-8', 'latin-1', 'cp1251']

        # Чтение содержимого книги
        for encoding in encodings:
            try:
                with open(book_path, 'r', encoding=encoding) as book_file:
                    content = book_file.readlines()
                break
            except UnicodeDecodeError:
                continue

        # Очистка предыдущего содержимого
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Заголовок книги
        title_label = ctk.CTkLabel(
            self.main_frame,
            text=book_name,
            font=("CustomFont", 24, "bold"),
            fg_color=Colors.BACKGROUND_COLOR,
            text_color=Colors.TEXT_COLOR
        )
        title_label.pack(pady=10)

        # Создание фрейма для текста книги
        text_frame = ctk.CTkFrame(self.main_frame, fg_color="white", width=600, height=400)
        text_frame.place(relx=0.5, rely=0.5, anchor="center")  # Центрируем фрейм

        # Текстовая область для отображения страницы
        self.page_text = tk.Text(text_frame, wrap=tk.WORD, bg="white", fg="black", font=("CustomFont", 16))
        self.page_text.pack(fill=tk.BOTH, expand=True)

        # Инициализация переменных для управления страницами
        self.content = content
        self.current_page = 0

        # Кнопка "Назад" для возврата к списку книг в левом нижнем углу
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
        back_button.pack(side=tk.BOTTOM, anchor="sw", padx=10, pady=(10, 20))  # Левый нижний угол с отступом

        # Кнопка "Назад" для листания с иконкой
        prev_icon = Image.open("assets/images/icons/prev.png").resize((20, 20), Image.LANCZOS)
        self.prev_icon_photo = ctk.CTkImage(prev_icon)  # Используем CTkImage вместо PIL.ImageTk.PhotoImage

        prev_button = ctk.CTkButton(
            self.main_frame,
            text=" ",
            image=self.prev_icon_photo,
            command=lambda: self.change_page(-1),
            fg_color=Colors.BUTTON_COLOR,
            text_color=Colors.BUTTON_TEXT_COLOR,
            font=("CustomFont", 14),
            width=60,
            height=40,
            corner_radius=10
        )
        prev_button.place(relx=0.1, rely=0.7, anchor="sw")  # Левый нижний угол (подняли выше)

        # Кнопка "Вперед" для листания с иконкой
        next_icon = Image.open("assets/images/icons/next.png").resize((20, 20), Image.LANCZOS)
        self.next_icon_photo = ctk.CTkImage(next_icon)  # Используем CTkImage вместо PIL.ImageTk.PhotoImage

        next_button = ctk.CTkButton(
            self.main_frame,
            text=" ",
            image=self.next_icon_photo,
            command=lambda: self.change_page(1),
            fg_color=Colors.BUTTON_COLOR,
            text_color=Colors.BUTTON_TEXT_COLOR,
            font=("CustomFont", 14),
            width=60,
            height=40,
            corner_radius=10
        )
        next_button.place(relx=0.9, rely=0.7, anchor="se")  # Правый нижний угол (подняли выше)

        # Метка для отображения номера текущей страницы в правом нижнем углу
        self.page_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Страница {self.current_page + 1} из {len(self.content)}",
            fg_color=Colors.BACKGROUND_COLOR,
            text_color=Colors.TEXT_COLOR,
            font=("CustomFont", 14)
        )
        self.page_label.place(relx=0.9, rely=1, anchor="se", padx=10, pady=10)  # Правый нижний угол

        # Инициализация отображения первой страницы
        self.page_text.delete(1.0, tk.END)  # Очистка текстовой области
        self.page_text.insert(tk.END, self.content[self.current_page])  # Вставка текста текущей страницы














