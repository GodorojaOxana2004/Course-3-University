import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import random

class GameOfLife:
    def __init__(self, width=30, height=30, alive_probability=0.3, seed=None):
        """
        Инициализация игры Жизнь
        
        Args:
            width: ширина сетки
            height: высота сетки
            alive_probability: вероятность живой клетки при случайной генерации
            seed: семя для генератора случайных чисел (для воспроизводимости)
        """
        self.width = width
        self.height = height
        
        # Установка семени для уникальности каждого студента
        if seed is None:
            seed = random.randint(1, 10000)
        np.random.seed(seed)
        random.seed(seed)
        
        print(f"Семя генератора: {seed} (сохраните для воспроизводимости)")
        
        # Создание случайной сетки
        self.grid = self.create_random_grid(alive_probability)
        
        # Добавление паттерна Blinker
        self.add_blinker_pattern()
        
        # Сохранение начального состояния
        self.initial_grid = self.grid.copy()
        
        self.generation = 0
        
    def create_random_grid(self, alive_probability):
        """Создание случайной сетки с заданной вероятностью живых клеток"""
        return np.random.choice([0, 1], size=(self.height, self.width), 
                               p=[1-alive_probability, alive_probability])
    
    def add_blinker_pattern(self):
        """
        Добавление паттерна Blinker на сетку в свободной зоне
        Blinker - это осциллирующий паттерн из 3 клеток в ряд
        """
        # Паттерн Blinker (вертикальный)
        blinker = np.array([[0, 1, 0],
                           [0, 1, 0],
                           [0, 1, 0]])
        
        pattern_height, pattern_width = blinker.shape
        
        # Поиск свободной зоны для размещения паттерна
        best_pos = None
        min_conflicts = float('inf')
        
        # Проверяем различные позиции, избегая границ
        for start_row in range(2, self.height - pattern_height - 2):
            for start_col in range(2, self.width - pattern_width - 2):
                # Проверяем область размещения и окрестности
                end_row = start_row + pattern_height
                end_col = start_col + pattern_width
                
                # Расширенная область для проверки (включая границу в 1 клетку)
                check_area = self.grid[start_row-1:end_row+1, start_col-1:end_col+1]
                conflicts = np.sum(check_area)
                
                # Ищем место с минимальным количеством живых клеток
                if conflicts < min_conflicts:
                    min_conflicts = conflicts
                    best_pos = (start_row, start_col)
                    
                    # Если нашли полностью свободную область - используем её
                    if conflicts == 0:
                        break
            
            if min_conflicts == 0:
                break
        
        # Если не нашли идеальное место, используем лучшее из найденных
        if best_pos is None:
            # Fallback к центру если ничего не найдено
            best_pos = (self.height // 2 - 1, self.width // 2 - 1)
        
        start_row, start_col = best_pos
        end_row = start_row + pattern_height
        end_col = start_col + pattern_width
        
        # Размещение паттерна
        self.grid[start_row:end_row, start_col:end_col] = blinker
        
        print(f"Паттерн Blinker добавлен в позицию ({start_row}, {start_col})")
        print(f"Конфликтов с существующими клетками: {min_conflicts}")
    
    def count_neighbors(self, row, col):
        """Подсчет живых соседей для клетки"""
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                
                neighbor_row = (row + i) % self.height
                neighbor_col = (col + j) % self.width
                count += self.grid[neighbor_row, neighbor_col]
        
        return count
    
    def update_grid(self):
        """Обновление сетки согласно правилам игры Конвея"""
        new_grid = np.zeros((self.height, self.width), dtype=int)
        
        for row in range(self.height):
            for col in range(self.width):
                neighbors = self.count_neighbors(row, col)
                current_cell = self.grid[row, col]
                
                # Применение правил игры Жизнь
                if current_cell == 1:  # Живая клетка
                    if neighbors < 2:  # Смерть от одиночества
                        new_grid[row, col] = 0
                    elif neighbors == 2 or neighbors == 3:  # Выживание
                        new_grid[row, col] = 1
                    else:  # neighbors > 3, смерть от перенаселения
                        new_grid[row, col] = 0
                else:  # Мертвая клетка
                    if neighbors == 3:  # Рождение
                        new_grid[row, col] = 1
        
        self.grid = new_grid
        self.generation += 1
    
    def get_stats(self):
        """Получение статистики текущего поколения"""
        alive_cells = np.sum(self.grid)
        total_cells = self.width * self.height
        density = alive_cells / total_cells
        
        return {
            'generation': self.generation,
            'alive_cells': alive_cells,
            'total_cells': total_cells,
            'density': density
        }
    
    def reset(self):
        """Сброс к начальному состоянию"""
        self.grid = self.initial_grid.copy()
        self.generation = 0
    
    def run_simulation(self, steps=100, show_animation=True):
        """
        Запуск симуляции
        
        Args:
            steps: количество шагов симуляции
            show_animation: показывать ли анимацию
        """
        if show_animation:
            self.animate_simulation(steps)
        else:
            # Текстовый режим
            for step in range(steps):
                stats = self.get_stats()
                print(f"Поколение {stats['generation']}: "
                      f"Живых клеток: {stats['alive_cells']}, "
                      f"Плотность: {stats['density']:.3f}")
                
                self.update_grid()
                
                # Остановка при вымирании всех клеток
                if np.sum(self.grid) == 0:
                    print("Все клетки погибли!")
                    break
    
    def animate_simulation(self, steps=100):
        """Анимированная визуализация симуляции"""
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Создание цветовой карты
        colors = ['white', 'black']
        cmap = ListedColormap(colors)
        
        # Начальное отображение с правильной статистикой
        im = ax.imshow(self.grid, cmap=cmap, animated=True)
        
        # Получаем начальную статистику
        initial_stats = self.get_stats()
        ax.set_title(f'Игра "Жизнь" с паттерном Blinker - Поколение: {initial_stats["generation"]}', fontsize=14)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        
        # Добавление сетки
        ax.set_xticks(np.arange(-0.5, self.width, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, self.height, 1), minor=True)
        ax.grid(which="minor", color="gray", linestyle='-', linewidth=0.5, alpha=0.3)
        
        # Текст для отображения статистики с начальными значениями
        initial_stats_str = (f'Поколение: {initial_stats["generation"]}\n'
                           f'Живых клеток: {initial_stats["alive_cells"]}\n'
                           f'Плотность: {initial_stats["density"]:.3f}\n'
                           f'Размер сетки: {self.width}×{self.height}')
        
        stats_text = ax.text(0.02, 0.98, initial_stats_str, transform=ax.transAxes, 
                           verticalalignment='top', fontfamily='monospace', fontsize=10,
                           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9))
        
        def animate(frame):
            # Для первого кадра показываем начальное состояние (поколение 0)
            # Для последующих кадров сначала обновляем, потом отображаем
            if frame > 0:
                self.update_grid()
            
            # Обновляем изображение
            im.set_array(self.grid)
            
            # Получаем актуальную статистику
            stats = self.get_stats()
            
            # Обновляем заголовок
            title = f'Игра "Жизнь" с паттерном Blinker - Поколение: {stats["generation"]}'
            ax.set_title(title, fontsize=14)
            
            # Обновляем текст статистики
            stats_str = (f'Поколение: {stats["generation"]}\n'
                        f'Живых клеток: {stats["alive_cells"]}\n'
                        f'Плотность: {stats["density"]:.3f}\n'
                        f'Размер сетки: {self.width}×{self.height}')
            stats_text.set_text(stats_str)
            
            # Возвращаем только изображение
            return [im]
        
        # Создание анимации (отключаем blit для корректного отображения текста)
        ani = animation.FuncAnimation(fig, animate, frames=steps, 
                                    interval=300, blit=False, repeat=False)
        
        plt.tight_layout()
        plt.show()
        
        return ani

    def save_pattern(self, filename):
        """Сохранение текущего паттерна в файл"""
        np.savetxt(filename, self.grid, fmt='%d')
        print(f"Паттерн сохранен в файл: {filename}")
    
    def load_pattern(self, filename):
        """Загрузка паттерна из файла"""
        self.grid = np.loadtxt(filename, dtype=int)
        self.height, self.width = self.grid.shape
        self.generation = 0
        print(f"Паттерн загружен из файла: {filename}")

# Пример использования
if __name__ == "__main__":
    print("=== Лабораторная работа №4: Игра Жизнь с паттерном Blinker ===\n")
    
    # Создание игры с параметрами из задания
    game = GameOfLife(width=30, height=30, alive_probability=0.35, seed=12345)
    
    print(f"Размер сетки: {game.width}×{game.height}")
    print(f"Начальная статистика:")
    initial_stats = game.get_stats()
    print(f"  Живых клеток: {initial_stats['alive_cells']}")
    print(f"  Плотность: {initial_stats['density']:.3f}")
    print()
    
    # Отображение начального состояния
    print("Начальное состояние (первые 10 строк):")
    for i in range(min(10, game.height)):
        row_str = ''.join(['█' if cell else '·' for cell in game.grid[i]])
        print(f"{i:2d}: {row_str}")
    print()
    
    # Запуск симуляции
    print("Запуск анимированной симуляции...")
    print("Закройте окно с анимацией для продолжения.\n")
    
    try:
        # Анимированная симуляция
        game.run_simulation(steps=200, show_animation=True)
    except Exception as e:
        print(f"Ошибка при показе анимации: {e}")
        print("Запуск в текстовом режиме...\n")
        
        # Сброс и запуск в текстовом режиме
        game.reset()
        game.run_simulation(steps=50, show_animation=False)
    
    print("\n=== Анализ результатов ===")
    print("В данной реализации:")
    print("1. Создана случайная сетка 30×30 с уникальным семенем")
    print("2. Добавлен осциллирующий паттерн Blinker в свободной зоне")
    print("3. Реализованы все правила игры Конвея")
    print("4. Показано взаимодействие структур с случайной динамикой")
    print("5. Визуализирована эволюция системы")
    print("6. Паттерн размещается с минимальным перекрытием случайных клеток")
    
    # Дополнительная информация о паттерне Blinker
    print("\nИнформация о паттерне Blinker:")
    print("- Период осцилляции: 2 поколения")
    print("- Чередует вертикальное и горизонтальное положение")
    print("- Один из простейших осцилляторов в игре Жизнь")