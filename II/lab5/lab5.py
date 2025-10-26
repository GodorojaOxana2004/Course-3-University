import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk


class FuzzyBurnRiskSystem:
    def __init__(self):
        self.temp_range = np.linspace(0, 45, 100)
        self.uv_range = np.linspace(0, 12, 100)
        self.humidity_range = np.linspace(0, 100, 100)
        self.risk_range = np.linspace(0, 100, 100)

    # --- Температура ---
    def temp_low(self, t):
        if t <= 15: return 1
        elif t >= 25: return 0
        else: return (25 - t) / 10

    def temp_medium(self, t):
        if t <= 15 or t >= 35: return 0
        elif 15 < t <= 25: return (t - 15) / 10
        else: return (35 - t) / 10

    def temp_high(self, t):
        if t <= 25: return 0
        elif t >= 35: return 1
        else: return (t - 25) / 10

    # --- UV ---
    def uv_low(self, u):
        if u <= 2: return 1
        elif u >= 5: return 0
        else: return (5 - u) / 3

    def uv_moderate(self, u):
        if u <= 2 or u >= 7: return 0
        elif 2 < u <= 5: return (u - 2) / 3
        else: return (7 - u) / 2

    def uv_high(self, u):
        if u <= 5 or u >= 10: return 0
        elif 5 < u <= 7: return (u - 5) / 2
        else: return (10 - u) / 3

    def uv_extreme(self, u):
        if u <= 7: return 0
        elif u >= 10: return 1
        else: return (u - 7) / 3

    # --- Влажность ---
    def humidity_low(self, h):
        if h <= 30: return 1
        elif h >= 60: return 0
        else: return (60 - h) / 30

    def humidity_high(self, h):
        if h <= 30: return 0
        elif h >= 60: return 1
        else: return (h - 30) / 30

    # --- Расчёт риска ---
    def calculate_risk(self, temperature, uv_index, humidity):
        t_low = self.temp_low(temperature)
        t_med = self.temp_medium(temperature)
        t_high = self.temp_high(temperature)
        u_low = self.uv_low(uv_index)
        u_mod = self.uv_moderate(uv_index)
        u_high = self.uv_high(uv_index)
        u_ext = self.uv_extreme(uv_index)
        h_low = self.humidity_low(humidity)
        h_high = self.humidity_high(humidity)

        rules = [
            (min(u_high, t_high), 90),
            (min(u_ext, t_high), 98),
            (min(u_mod, h_high), 50),
            (min(u_low, t_low), 15),
            (min(u_high, h_low), 90),
            (min(u_ext, t_med), 85),
            (min(u_mod, t_low), 30),
            (min(u_low, h_high), 20),
            (min(u_mod, t_med, h_low), 55),
            (min(u_high, t_med), 75),
            (min(u_ext, h_high), 80),
            (min(u_low, t_high), 35)
        ]

        weighted = sum((s ** 2) * v for s, v in rules)
        total = sum((s ** 2) for s, _ in rules)
        risk = weighted / total if total > 0 else 0
        strong = max(s for s, _ in rules)
        max_risk = max(v for _, v in rules)
        risk = max(risk, strong * max_risk * 0.7)
        return risk

    def get_recommendation(self, risk):
        if risk < 30:
            return ("НИЗКИЙ", "#4caf50", "Риск минимален. Крем SPF 15+.")
        elif risk < 60:
            return ("СРЕДНИЙ", "#ff9800", "Умеренный риск. Крем SPF 30+, избегайте солнца в полдень.")
        else:
            return ("ВЫСОКИЙ", "#f44336", "⚠️ Высокий риск! SPF 50+, избегайте солнца 10:00–16:00.")


class BurnRiskGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("☀️ Прогноз риска солнечного ожога")
        self.root.geometry("1400x900")

        self.system = FuzzyBurnRiskSystem()
        self.temperature = tk.DoubleVar(value=25)
        self.uv = tk.DoubleVar(value=5)
        self.humidity = tk.DoubleVar(value=50)

        self.create_ui()
        self.update_all()

    def create_ui(self):
        header = tk.Label(self.root, text="Прогнозирование риска солнечного ожога",
                          font=("Arial", 20, "bold"), bg="#ff9800", fg="white")
        header.pack(fill=tk.X, pady=10)

        main = tk.Frame(self.root)
        main.pack(fill=tk.BOTH, expand=True)

        left = tk.Frame(main, width=300)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        right = tk.Frame(main)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- Ползунки ---
        tk.Label(left, text="🌡 Температура (°C)", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        tk.Scale(left, from_=0, to=45, variable=self.temperature, orient=tk.HORIZONTAL, command=self.on_change).pack()

        tk.Label(left, text="☀️ UV-индекс", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        tk.Scale(left, from_=0, to=12, resolution=0.1, variable=self.uv, orient=tk.HORIZONTAL, command=self.on_change).pack()

        tk.Label(left, text="💧 Влажность (%)", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        tk.Scale(left, from_=0, to=100, variable=self.humidity, orient=tk.HORIZONTAL, command=self.on_change).pack()

        # --- Результаты ---
        self.result_label = tk.Label(left, text="", font=("Arial", 14, "bold"), wraplength=250)
        self.result_label.pack(pady=20)

        # --- Графики ---
        self.fig = plt.Figure(figsize=(11, 7))
        self.ax_t = self.fig.add_subplot(2, 2, 1)
        self.ax_u = self.fig.add_subplot(2, 2, 2)
        self.ax_h = self.fig.add_subplot(2, 2, 3)
        self.ax_3d = self.fig.add_subplot(2, 2, 4, projection="3d")
        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def on_change(self, event=None):
        self.update_all()

    def update_all(self):
        t = self.temperature.get()
        u = self.uv.get()
        h = self.humidity.get()
        risk = self.system.calculate_risk(t, u, h)
        level, color, msg = self.system.get_recommendation(risk)

        self.result_label.config(
            text=f"Риск: {risk:.1f}%\nУровень: {level}\n\n{msg}", fg=color
        )

        self.plot_temp(t)
        self.plot_uv(u)
        self.plot_humidity(h)
        self.plot_3d(h)
        self.canvas.draw()

    def plot_temp(self, val):
        x = self.system.temp_range
        self.ax_t.clear()
        self.ax_t.plot(x, [self.system.temp_low(v) for v in x], 'g', label="Низкая")
        self.ax_t.plot(x, [self.system.temp_medium(v) for v in x], 'orange', label="Средняя")
        self.ax_t.plot(x, [self.system.temp_high(v) for v in x], 'r', label="Высокая")
        self.ax_t.axvline(val, color='black', linestyle='--')
        self.ax_t.set_title("Температура (°C)")
        self.ax_t.legend()

    def plot_uv(self, val):
        x = self.system.uv_range
        self.ax_u.clear()
        self.ax_u.plot(x, [self.system.uv_low(v) for v in x], 'g', label="Низкий")
        self.ax_u.plot(x, [self.system.uv_moderate(v) for v in x], 'orange', label="Умеренный")
        self.ax_u.plot(x, [self.system.uv_high(v) for v in x], 'r', label="Высокий")
        self.ax_u.plot(x, [self.system.uv_extreme(v) for v in x], 'purple', label="Экстремальный")
        self.ax_u.axvline(val, color='black', linestyle='--')
        self.ax_u.set_title("UV-индекс")
        self.ax_u.legend()

    def plot_humidity(self, val):
        x = self.system.humidity_range
        self.ax_h.clear()
        self.ax_h.plot(x, [self.system.humidity_low(v) for v in x], 'g', label="Низкая")
        self.ax_h.plot(x, [self.system.humidity_high(v) for v in x], 'b', label="Высокая")
        self.ax_h.axvline(val, color='black', linestyle='--')
        self.ax_h.set_title("Влажность (%)")
        self.ax_h.legend()

    def plot_3d(self, humidity):
        self.ax_3d.clear()
        t_vals = np.linspace(10, 40, 30)
        u_vals = np.linspace(0, 12, 30)
        T, U = np.meshgrid(t_vals, u_vals)
        R = np.zeros_like(T)
        for i in range(T.shape[0]):
            for j in range(T.shape[1]):
                R[i, j] = self.system.calculate_risk(T[i, j], U[i, j], humidity)
        surf = self.ax_3d.plot_surface(T, U, R, cmap='inferno', alpha=0.8)
        self.ax_3d.set_title("3D поверхность риска (зависит от влажности)")
        self.ax_3d.set_xlabel("Температура (°C)")
        self.ax_3d.set_ylabel("UV-индекс")
        self.ax_3d.set_zlabel("Риск (%)")


if __name__ == "__main__":
    root = tk.Tk()
    app = BurnRiskGUI(root)
    root.mainloop()
