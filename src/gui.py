import os
import tkinter as tk
from tkinter import filedialog, font, messagebox, simpledialog, scrolledtext, Toplevel
from src.styles import Colors
import customtkinter as ctk
from PIL import Image, ImageTk
from src.text_compress_tool import compress_text
from src.make_recommendation_tool import make_recommendation
from llama_cpp import Llama
from googletrans import Translator

# Инициализация модели и переводчика
llm = Llama.from_pretrained(
    repo_id="AlekseiPravdin/Seamaiiza-7B-v1-gguf",
    filename="Seamaiiza-7B-v1.q2_k.gguf",
)
translator = Translator()


class BookGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("ReadMe")
        self.master.geometry("800x600")
        self.master.configure(bg=Colors.BACKGROUND_COLOR)
        self.chat_history = ""
        self.chat_context = []

        # Загрузка пользовательского шрифта
        custom_font_path = "assets/fonts/Outfit-Black.ttf"
        self.custom_font = font.Font(family="CustomFont", size=14)
        self.master.option_add("*Font", self.custom_font)

        # Инициализация главного экрана
        self.main_frame = ctk.CTkFrame(master, fg_color=Colors.BACKGROUND_COLOR)
        self.main_frame.pack(fill="both", expand=True)

        self.create_main_screen()

    def create_main_screen(self):
        # Очистка истории чата с анализом содержания
        self.chat_history = ""
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
    def open_analysis_window(self):
        analysis_window = Toplevel(self.master)
        analysis_window.title("Анализ содержания")
        analysis_window.geometry("600x400")
        analysis_window.configure(bg=Colors.BACKGROUND_COLOR)

        # Заголовок
        title_label = ctk.CTkLabel(
            analysis_window,
            text="Анализ содержания",
            font=("CustomFont", 24, "bold"),
            fg_color=Colors.BACKGROUND_COLOR,
            text_color=Colors.TEXT_COLOR
        )
        title_label.pack(pady=10)

        # Создание области для чата
        self.chat_box = scrolledtext.ScrolledText(analysis_window, wrap=tk.WORD, width=70, height=15, bg=Colors.BACKGROUND_COLOR, fg=Colors.TEXT_COLOR, font=("CustomFont", 12, "bold"))
        self.chat_box.insert(tk.END, self.chat_history)
        self.chat_box.pack(pady=10)

        # Поле для ввода сообщения
        self.entry = tk.Entry(analysis_window, width=50, font=("CustomFont", 12))
        self.entry.pack(pady=10)

        def ask_bot():
            user_input = self.entry.get()
            if user_input:
                self.chat_box.insert(tk.END, f"You: {user_input}\n")
                self.entry.delete(0, tk.END)
                translated_input = translator.translate(user_input, dest='en').text
                # Добавляем сообщение пользователя в историю
                self.chat_context.append({"role": "user", "content": translated_input})
                
                # Получаем ответ от модели, передавая историю чата и задавая требование о краткости
                response = llm.create_chat_completion(
                    messages=self.chat_context + [{"role": "user", "content": "Please answer briefly."}], 
                )
                english_response = response['choices'][0]['message']['content']

                translated_response = translator.translate(english_response, dest='ru').text
                self.chat_box.insert(tk.END, f"Bot: {translated_response}\n\n")
                self.chat_context.append({"role": "assistant", "content": english_response})
                self.chat_box.yview(tk.END)

                # Сохраняем историю чата
                self.chat_history = self.chat_box.get("1.0", tk.END)

        send_button = ctk.CTkButton(  # Изменено на ctk.CTkButton
            analysis_window,
            text="Отправить",
            command=ask_bot,
            font=("CustomFont", 12),
            fg_color=Colors.BUTTON_COLOR,
            text_color=Colors.BUTTON_TEXT_COLOR
        )
        send_button.pack()

        # Кнопка для закрытия окна
        close_button = ctk.CTkButton(  # Изменено на ctk.CTkButton
            analysis_window,
            text="Закрыть",
            command=analysis_window.destroy,
            font=("CustomFont", 12),
            fg_color=Colors.BUTTON_COLOR,
            text_color=Colors.BUTTON_TEXT_COLOR
        )
        close_button.pack(pady=10)

    def open_book(self, book_name):
        book_path = os.path.join("books", book_name)
        encodings = ['utf-8', 'latin-1', 'cp1251']
        first_open = not os.path.exists(f"{book_path}.opened")

        for encoding in encodings:
            try:
                with open(book_path, "r", encoding=encoding) as file:
                    book_content = file.read()
                break
            except UnicodeDecodeError:
                continue

      # При первом открытии книги спрашиваем о сжатии
        if first_open:
            result = messagebox.askquestion(
                "Сжатие книги",
                "Хотите ли вы сжать книгу?",
                icon="question",
                type=messagebox.YESNO,
            )
            if result == 'yes':
                pages_per_day = simpledialog.askinteger(
                    "Количество страниц в день",
                    "Введите количество страниц, которое вы хотите читать в день:",
                    minvalue=1,
                )
                days = simpledialog.askinteger(
                    "Количество дней",
                    "Введите количество дней, в течение которых вы планируете прочитать книгу:",
                    minvalue=1,
                )
                # Сжатие содержимого книги
                book_content = compress_text(book_content, pages_per_day, days)
                
                # Сохранение сжатого содержимого обратно в файл
                with open(book_path, "w", encoding="utf-8") as file:
                    file.write(book_content)
                
            # Создаем метку о первом открытии книги
            with open(f"{book_path}.opened", "w") as file:
                file.write("opened")

        # Разделение текста на страницы (например, 6500 символов на страницу)
        cleaned_content = ' '.join(book_content.split())  # Убирает лишние пробелы
        self.page_content = [cleaned_content[i:i+7000] for i in range(0, len(cleaned_content), 7000)]
        self.current_page = 0

        def show_page():
            # Очистка текущего содержимого
            for widget in self.main_frame.winfo_children():
                widget.destroy()
            # Кнопка назад
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

            # Текст страницы
            text_font = font.Font(family="CustomFont", size=14, weight="bold")  # Устанавливаем жирный шрифт
            text_box = tk.Text(
                self.main_frame,
                wrap="word",
                font=text_font,
                bg=Colors.BACKGROUND_COLOR,
                fg=Colors.TEXT_COLOR,
                padx=10,
                pady=10
            )
            text_box.insert("1.0", self.page_content[self.current_page])
            text_box.config(state="disabled")
            text_box.pack(fill="both", expand=True, padx=10, pady=10)

            # Показ текущей страницы
            page_label = tk.Label(
                self.main_frame,
                text=f"Страница {self.current_page + 1} из {len(self.page_content)}",
                font=("CustomFont", 12),
                bg=Colors.BACKGROUND_COLOR,
                fg=Colors.BUTTON_TEXT_COLOR
            )
            page_label.pack(side="bottom", pady=5)

            # Кнопки переключения страниц
            prev_button = ctk.CTkButton(
                self.main_frame,
                text="Предыдущая страница",
                command=prev_page,
                fg_color=Colors.BUTTON_COLOR,
                text_color=Colors.BUTTON_TEXT_COLOR,
                font=("CustomFont", 14),
                width=120,
                height=40,
                corner_radius=10
            )
            prev_button.pack(side="left", padx=10, pady=10)

            next_button = ctk.CTkButton(
                self.main_frame,
                text="Следующая страница",
                command=next_page,
                fg_color=Colors.BUTTON_COLOR,
                text_color=Colors.BUTTON_TEXT_COLOR,
                font=("CustomFont", 14),
                width=120,
                height=40,
                corner_radius=10
            )
            next_button.pack(side="right", padx=10, pady=10)
            
            # Добавление кнопки анализа содержания
            analysis_button = ctk.CTkButton(
                self.main_frame,
                text="Анализ содержания",
                command=self.open_analysis_window,
                fg_color=Colors.BUTTON_COLOR,
                text_color=Colors.BUTTON_TEXT_COLOR,
                font=("CustomFont", 14),
                width=150,
                height=40,
                corner_radius=10
            )
            analysis_button.pack(pady=10)

        # Функции для переключения страниц
        def next_page():
            if self.current_page < len(self.page_content) - 1:
                self.current_page += 1
                show_page()

        def prev_page():
            if self.current_page > 0:
                self.current_page -= 1
                show_page()
        # Отображение первой страницы
        show_page()











