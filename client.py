import socket
import tkinter as tk
from tkinter import messagebox

class QuestClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Quest 2026")
        self.score = 0
        self.level = 1
        
        # Подключение к серверу
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(('localhost', 12345))
        except:
            print("Ошибка: Запустите сначала server.py!")
            self.root.destroy()
            return

        self.main_menu()

    def send_score(self, points):
        self.score += points
        self.client.send(f"SCORE:{points}".encode('utf-8'))
        response = self.client.recv(1024).decode('utf-8')
        messagebox.showinfo("Уровень завершен", f"Вы получили {points} б.\n{response}")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def main_menu(self):
        self.clear_screen()
        tk.Label(self.root, text=f"ГЛАВНОЕ МЕНЮ\nТекущие баллы: {self.score}", font=("Arial", 16)).pack(pady=20)
        
        if self.level == 1:
            tk.Button(self.root, text="Начать Уровень 1 (Отличия)", command=self.level_1).pack(pady=10)
        elif self.level == 2:
            tk.Button(self.root, text="Начать Уровень 2 (Крестики-Нолики)", command=self.level_2).pack(pady=10)
        elif self.level == 3:
            tk.Button(self.root, text="Начать Уровень 3 (Лабиринт)", command=self.level_3).pack(pady=10)
        else:
            self.show_final_results()

    # --- УРОВЕНЬ 1: ОТЛИЧИЯ ---
    def level_1(self):
        self.clear_screen()
        tk.Label(self.root, text="знайдить відміності (усього їх 8)").pack()
        # В реальном коде здесь отрисовка Canvas с картинками
        tk.Label(self.root, text="[foll.fif]", bg="grey", width=40, height=10).pack()
        
        entry = tk.Entry(self.root)
        entry.pack(pady=8)
        entry.insert(0, "скільки знайшли?")

        def check():
            if entry.get() == "3":
                self.send_score(33)
                self.level = 2
                self.main_menu()
            else:
                messagebox.showerror("помилка", "Невірно! спробуйте знову.")

        tk.Button(self.root, text="дати відповіть", command=check).pack()
        tk.Button(self.root, text="у головне меню", command=self.main_menu).pack()

    # --- УРОВЕНЬ 2: КРЕСТИКИ-НОЛИКИ (Упрощенно) ---
    def level_2(self):
        self.clear_screen()
        wins = 0
        tk.Label(self.root, text=f"потрібно виграти у бота три вийграши: {wins}").pack()
        
        # Для краткости: имитация логики игры
        def simulate_win():
            nonlocal wins
            wins += 1
            if wins >= 3:
                self.send_score(33)
                self.level = 3
                self.main_menu()
            else:
                messagebox.showinfo("Раунд", f"перемога у раунді: {3-wins}")

        tk.Button(self.root, text="зробти ход (імітація)", command=simulate_win).pack(pady=20)

    # --- УРОВЕНЬ 3: ЛАБИРИНТ ---
    def level_3(self):
        self.clear_screen()
        tk.Label(self.root, text="знайдіть віход. користуючись кнопками:").pack()
        
        path = []
        correct_path = ["у низ", "у право", "у гору"]

        def move(direction):
            path.append(direction)
            if len(path) == 3:
                if path == correct_path:
                    self.send_score(33)
                    self.level = 4
                    self.main_menu()
                else:
                    messagebox.showwarning("Тупик", "Ви загубились! почнить спочатку.")
                    path.clear()

        for d in ["Вверх", "Вниз", "Влево", "Вправо"]:
            tk.Button(self.root, text=d, command=lambda x=d: move(x)).pack(side="left", padx=5)

    def show_final_results(self):
        self.clear_screen()
        self.client.send("GET_TOTAL".encode('utf-8'))
        final_data = self.client.recv(1024).decode('utf-8')
        tk.Label(self.root, text="КВЕСТ завіршенно", font=("Arial", 20)).pack(pady=20)
        tk.Label(self.root, text=final_data, font=("Arial", 14)).pack()
        tk.Button(self.root, text="Вихід", command=self.root.quit).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")
    app = QuestClient(root)
    root.mainloop()