import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def get_num(num: float):
    num = round(num, 2)
    if num.is_integer():
        return int(num)
    return num


class LinearFunction:
    """Класс для представления линейной функции"""
    def __init__(self, a, b):
        self.a = a
        self.b = b
        
    def __call__(self, x):
        return self.a * x + self.b
    
    def derivative(self):
        return self.a
    
    def solve_equalition(self, y):
        return (y - self.b) / self.a
        
    
class QuadraticFunction:
    """Класс для представления квадратичной функции"""
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        
    def __call__(self, x):
        return self.a * x**2 + self.b * x + self.c
    
    def derivative(self):
        return LinearFunction(2 * self.a, self.b)
    
    
def calculate_line(linear: LinearFunction, quadratic: QuadraticFunction):
    x1 = quadratic.derivative().solve_equalition(linear.derivative())
    y1 = quadratic(x1)
    
    print(LinearFunction(linear.derivative(), y1 - x1 * linear.derivative()))
        
    return LinearFunction(linear.derivative(), y1 - x1 * linear.derivative()), x1
    
    
class ParabolaPlotter:
    """Класс для построения графика"""
    def __init__(self, master):
        self.master = master
        self.master.title("Построение касательной")

        # Поля ввода для коэффициентов
        frame = ttk.Frame(master)
        frame.pack(pady=10)

        ttk.Label(frame, text="Коэффициент a:").grid(row=0, column=0)
        self.entry_a = ttk.Entry(frame)
        self.entry_a.grid(row=0, column=1)

        ttk.Label(frame, text="Коэффициент b:").grid(row=1, column=0)
        self.entry_b = ttk.Entry(frame)
        self.entry_b.grid(row=1, column=1)

        ttk.Label(frame, text="Коэффициент c:").grid(row=2, column=0)
        self.entry_c = ttk.Entry(frame)
        self.entry_c.grid(row=2, column=1)
        
        ttk.Label(frame, text="Коэффициент прямой a:").grid(row=3, column=0)
        self.entry_a1 = ttk.Entry(frame)
        self.entry_a1.grid(row=3, column=1)

        ttk.Label(frame, text="Коэффициент прямой b:").grid(row=4, column=0)
        self.entry_b1 = ttk.Entry(frame)
        self.entry_b1.grid(row=4, column=1)

        # Кнопка для построения графика
        button = ttk.Button(master, text="Построить график", command=self.plot_graph)
        button.pack(pady=10)

        # Создание области для графика
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master)  # Создание виджета для графика
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack()

    def plot_graph(self):
        # Получаем коэффициенты из полей ввода
        a = float(self.entry_a.get())
        b = float(self.entry_b.get())
        c = float(self.entry_c.get())
        
        a1 = float(self.entry_a1.get())
        b1 = float(self.entry_b1.get())
        
        quad = QuadraticFunction(a, b, c)
        lin = LinearFunction(a1, b1)
        
        func2, x1 = calculate_line(linear=lin, quadratic=quad)

        # Генерация данных для параболы
        x = np.linspace(min(-10, x1 * 1.5), max(x1 * 1.5, 10), 400)
        y = quad(x)
        y1 = lin(x)
        y2 = func2(x)

        # Очищаем предыдущий график
        self.ax.clear()
        
        # Построение графика
        self.ax.plot(x, y, label='Парабола', color='blue')
        self.ax.plot(x, y1, label="Прямая", color="red")
        self.ax.plot(x, y2, label=f"Касательная (y = {get_num(func2.a)}x {' - ' if func2.b < 0 else ' + '} {abs(get_num(func2.b))})", color="green")
        self.ax.axhline(0, color='black', linewidth=0.5, ls='--')
        self.ax.axvline(0, color='black', linewidth=0.5, ls='--')
        self.ax.set_title('График')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.grid()
        self.ax.legend()

        # Обновление графика
        self.canvas.draw()

# Создание основного окна
if __name__ == "__main__":
    root = tk.Tk()
    app = ParabolaPlotter(root)
    root.mainloop()
    