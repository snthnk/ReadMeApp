import os

class FileManager:
    def __init__(self, books_folder="books"):
        self.books_folder = books_folder
        os.makedirs(self.books_folder, exist_ok=True)

    def save_book(self, file_path):
        if os.path.isfile(file_path):
            book_name = os.path.basename(file_path)
            new_path = os.path.join(self.books_folder, book_name)
            with open(file_path, 'r', encoding='utf-8') as src_file:
                content = src_file.read()
                with open(new_path, 'w', encoding='utf-8') as dest_file:
                    dest_file.write(content)
            return new_path
        return None

    def get_books(self):
        return [f for f in os.listdir(self.books_folder) if f.endswith('.txt')]
