from src.app import BookApp
import tkinter as tk


if __name__ == "__main__":
    root = tk.Tk()
    app = BookApp(root)
    root.mainloop()