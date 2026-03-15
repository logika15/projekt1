import socket
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

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
        tk.Label(self.root, text="Знайдіть відмінності (усього їх 8)").pack(pady=10)

        # --- ЗАГРУЗКА И ОТОБРАЖЕНИЕ КАРТИНКИ ---
        try:
            # Открываем файл изображения
            img = Image.open("foll.png")
            
            # (Опционально) Изменяем размер, если картинка слишком большая
            img = img.resize((400, 300)) 
            
            # Конвертируем для Tkinter
            self.photo = ImageTk.PhotoImage(img)
            
            # Создаем Label, который будет содержать картинку
            img_label = tk.Label(self.root, image=self.photo)
            img_label.pack(pady=10)
            
        except Exception as e:
            # Если файл не найден, выводим ошибку в консоль и показываем серый блок
            print(f"Ошибка загрузки картинки: {e}")
            tk.Label(self.root, text="Зображення не знайдено", bg="grey", width=40, height=10).pack()
        # ---------------------------------------

        entry = tk.Entry(self.root)
        entry.pack(pady=8)
        # Удаляем текст-подсказку при нажатии или оставляем пустым
        entry.insert(0, "") 

        def check():
            # В вашем коде было условие "3", хотя в тексте "8". Исправьте по логике игры.
            if entry.get() == "8": 
                self.send_score(33)
                self.level = 2
                self.main_menu()
            else:
                messagebox.showerror("помилка", "Невірно! спробуйте знову.")

        tk.Button(self.root, text="дати відповідь", command=check).pack()
        tk.Button(self.root, text="у головне меню", command=self.main_menu).pack()

    # --- УРОВЕНЬ 2: КРЕСТИКИ-НОЛИКИ (Упрощенно) ---

    def level_2(self):
        self.clear_screen()
        
        # Состояние игры
        self.wins = 0
        self.board = [""] * 9
        self.buttons = []
        
        self.info_label = tk.Label(self.root, text=f"Перемог: {self.wins} / 3", font=("Arial", 12))
        self.info_label.pack(pady=10)

        # Контейнер для сетки 3x3
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack()

        def check_winner(b):
            # Все возможные выигрышные комбинации
            win_coords = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
            for r in win_coords:
                if b[r[0]] == b[r[1]] == b[r[2]] != "":
                    return b[r[0]]
            if "" not in b:
                return "Draw"
            return None

        def reset_board():
            self.board = [""] * 9
            for btn in self.buttons:
                btn.config(text="", state=tk.NORMAL)

        def bot_move():
            # Бот ищет пустые клетки и делает случайный ход
            empty_cells = [i for i, val in enumerate(self.board) if val == ""]
            if empty_cells:
                move = random.choice(empty_cells)
                self.board[move] = "O"
                self.buttons[move].config(text="O", state=tk.DISABLED)
                
                result = check_winner(self.board)
                if result == "O":
                    messagebox.showinfo("Ой!", "Бот виграв цей раунд.")
                    reset_board()
                elif result == "Draw":
                    messagebox.showinfo("Нічия", "Спробуйте ще раз.")
                    reset_board()

        def player_click(index):
            if self.board[index] == "":
                self.board[index] = "X"
                self.buttons[index].config(text="X", state=tk.DISABLED)
                
                result = check_winner(self.board)
                if result == "X":
                    self.wins += 1
                    self.info_label.config(text=f"Перемог: {self.wins} / 3")
                    if self.wins >= 3:
                        messagebox.showinfo("Вітаємо!", "Ви пройшли рівень!")
                        self.send_score(33)
                        self.level = 3
                        self.main_menu()
                    else:
                        messagebox.showinfo("Раунд", "Ви виграли раунд!")
                        reset_board()
                elif result == "Draw":
                    messagebox.showinfo("Нічия", "Ніхто не виграв.")
                    reset_board()
                else:
                    # Если игрок не выиграл и не ничья — ходит бот
                    self.root.after(500, bot_move)

        # Создаем сетку кнопок 3x3
        for i in range(9):
            btn = tk.Button(self.grid_frame, text="", font=('Arial', 20, 'bold'), 
                            width=5, height=2, command=lambda i=i: player_click(i))
            btn.grid(row=i//3, column=i%3)
            self.buttons.append(btn)

        tk.Button(self.root, text="у головне меню", command=self.main_menu).pack()

    # --- УРОВЕНЬ 3: ЛАБИРИНТ ---

#class Game:
    # ... ваши остальные методы (__init__, clear_screen, send_score и т.д.) ...

    def level_3(self):
        self.clear_screen()
        
        # Инструкция
        instruction = tk.Label(self.root, text="Знайдіть вихід з лабіринту!\nКерування: стрілочки клавіатури", font=("Arial", 12))
        instruction.pack(pady=10)

        # --- НАСТРОЙКИ ЛАБИРИНТА ---
        self.cell_size = 40  # Размер одной ячейки (стены или прохода)
        # Карта лабиринта: 1 - стена, 0 - проход, 'S' - старт, 'E' - выход
        self.maze_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 'S', 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 0, 0, 1, 'E', 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        
        # Вычисляем размер холста на основе карты
        rows = len(self.maze_map)
        cols = len(self.maze_map[0])
        self.canvas_width = cols * self.cell_size
        self.canvas_height = rows * self.cell_size

        # Создаем Холст (Canvas)
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        # --- ОТРИСОВКА ЛАБИРИНТА И ШАРИКА ---
        self.player_pos = [0, 0] # [row, col]

        # Отрисовка стен и поиск старта/выхода
        for r in range(rows):
            for c in range(cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                cell = self.maze_map[r][c]
                
                if cell == 1: # Сцена
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="gray")
                elif cell == 'S': # Старт
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightblue", outline="gray")
                    self.player_pos = [r, c] # Ставим игрока сюда
                elif cell == 'E': # Выход
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="lime", outline="gray")

        # Создаем красный шарик (игрок)
        p_y, p_x = self.player_pos
        padding = 5 # Чтобы шарик был чуть меньше ячейки
        self.player_avatar = self.canvas.create_oval(
            p_x * self.cell_size + padding,
            p_y * self.cell_size + padding,
            (p_x + 1) * self.cell_size - padding,
            (p_y + 1) * self.cell_size - padding,
            fill="red", outline="darkred"
        )

        # --- ЛОГИКА ДВИЖЕНИЯ ---
        def move_player(event):
            # 'event.keysym' содержит имя нажатой клавиши (Up, Down, Left, Right)
            current_r, current_c = self.player_pos
            new_r, new_c = current_r, current_c

            if event.keysym == 'Up':    new_r -= 1
            elif event.keysym == 'Down':  new_r += 1
            elif event.keysym == 'Left':  new_c -= 1
            elif event.keysym == 'Right': new_c += 1
            else: return # Нажата другая клавиша

            # Проверка столкновения со стеной и границами
            if (0 <= new_r < rows and 0 <= new_c < cols and 
                self.maze_map[new_r][new_c] != 1):
                
                # Обновляем логическую позицию
                self.player_pos = [new_r, new_c]
                
                # Перемещаем графический объект на холсте
                dx = (new_c - current_c) * self.cell_size
                dy = (new_r - current_r) * self.cell_size
                self.canvas.move(self.player_avatar, dx, dy)
                
                # Проверка достижения выхода
                if self.maze_map[new_r][new_c] == 'E':
                    self.canvas.unbind_all("<Key>") # Отключаем управление
                    messagebox.showinfo("Перемога!", "Ви знайшли вихід!")
                    self.send_score(33)
                    self.level = 4
                    # self.level_4() или self.main_menu() в зависимости от вашей логики
                    # Для теста вызываем меню:
                    if hasattr(self, 'main_menu'): self.main_menu()
                    else: print("Конец теста лабиринта. Переход к уровню 4.")

        # Привязываем события клавиатуры ко всему окну
        self.root.bind_all("<Key>", move_player)

        # Добавим кнопку возврата на всякий случай
        if hasattr(self, 'main_menu'):
            tk.Button(self.root, text="Сдаться", command=self.main_menu).pack(pady=10)

# --- БЛОК ДЛЯ ТЕСТИРОВАНИЯ (если вы запускаете этот файл отдельно) ---
if __name__ == "__main__":

    # Имитация вашего основного класса для теста
    class TestGame:
        def __init__(self):
            self.root = tk.Tk()
            self.root.title("Тест Лабиринта")
            self.level = 3
            self.level_3()
            self.root.mainloop()

        def clear_screen(self):
            for widget in self.root.winfo_children():
                widget.destroy()
        
        def send_score(self, score):
            print(f"Очки отправлены: {score}")

        # Подключаем метод level_3, описанный выше
        def level_3(self):
            # Скопируйте сюда весь код метода level_3, который я написал выше
            pass 
    def show_final_results(self):
        self.clear_screen()
        self.root.config(bg=self.colors["bg"])
        
        tk.Label(
            self.root, 
            text="QUEST COMPLETED!", 
            font=("Segoe UI", 24, "bold"), 
            fg=self.colors["gold"], 
            bg=self.colors["bg"]
        ).pack(pady=30)

        tk.Label(
            self.root, 
            text=f"Ваш финальный счет: {self.score}", 
            font=("Segoe UI", 16), 
            fg=self.colors["text"], 
            bg=self.colors["bg"]
        ).pack(pady=10)

        # Кнопка выхода
        tk.Button(
            self.root, 
            text="Выйти из игры", 
            command=self.quit_game, 
            **self.btn_style
        ).pack(pady=20)

    def quit_game(self):
        # Закрываем сокет перед выходом, чтобы сервер не выдал ошибку
        try:
            self.client.send("QUIT".encode('utf-8'))
            self.client.close()
        except:
            pass
        self.root.destroy()

    def restart_game(self):
        self.score = 0
        self.level = 1
        # Можно отправить серверу уведомление о рестарте, если нужно
        try:
            self.client.send("RESTART:0".encode('utf-8'))
        except:
            pass
        self.main_menu()
        
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x450")
    app = QuestClient(root)
    root.mainloop()