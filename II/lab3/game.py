import pygame
import numpy as np
import random
import math
from typing import List, Tuple, Optional

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 60

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)

class Wall:
    """Класс для представления стен"""
    def __init__(self, start: Tuple[float, float], end: Tuple[float, float]):
        self.start = np.array(start, dtype=float)
        self.end = np.array(end, dtype=float)
        self.normal = self._calculate_normal()
    
    def _calculate_normal(self) -> np.ndarray:
        """Вычисляет нормаль к стене"""
        direction = self.end - self.start
        # Поворачиваем направление на 90 градусов для получения нормали
        normal = np.array([-direction[1], direction[0]])
        length = np.linalg.norm(normal)
        return normal / length if length > 0 else np.array([0.0, 0.0])
    
    def distance_to_point(self, point: np.ndarray) -> Tuple[float, np.ndarray]:
        """Вычисляет расстояние от точки до стены и ближайшую точку"""
        # Вектор от начала стены к точке
        to_point = point - self.start
        # Вектор стены
        wall_vec = self.end - self.start
        wall_length_sq = np.dot(wall_vec, wall_vec)
        
        if wall_length_sq == 0:
            return np.linalg.norm(to_point), self.start
        
        # Проекция точки на линию стены
        t = max(0, min(1, np.dot(to_point, wall_vec) / wall_length_sq))
        projection = self.start + t * wall_vec
        
        return np.linalg.norm(point - projection), projection
    
    def get_repulsion_force(self, point: np.ndarray, radius: float) -> np.ndarray:
        """Вычисляет силу отталкивания от стены"""
        distance, closest_point = self.distance_to_point(point)
        if distance > radius:
            return np.array([0.0, 0.0])
        
        # Направление от стены к точке
        direction = point - closest_point
        length = np.linalg.norm(direction)
        
        if length == 0:
            # Если точка прямо на стене, используем нормаль
            return self.normal * radius
        
        # Сила обратно пропорциональна расстоянию
        force_magnitude = (radius - distance) / radius * 100  # увеличиваем силу
        return (direction / length) * force_magnitude
    
    def check_collision(self, point: np.ndarray, radius: float) -> Tuple[bool, np.ndarray]:
        """Проверяет столкновение с стеной и возвращает корректирующий вектор"""
        distance, closest_point = self.distance_to_point(point)
        
        if distance < radius:
            # Есть пересечение, нужно корректировать позицию
            direction = point - closest_point
            length = np.linalg.norm(direction)
            
            if length == 0:
                # Используем нормаль стены
                correction = self.normal * (radius - distance)
            else:
                correction = (direction / length) * (radius - distance)
            
            return True, correction
        
        return False, np.array([0.0, 0.0])

class Exit:
    """Класс для представления выхода"""
    def __init__(self, position: Tuple[float, float], width: float = 40):
        self.position = np.array(position, dtype=float)
        self.width = width
        self.reached_count = 0

class Pedestrian:
    """Класс пешехода с алгоритмом Boids и целевым движением"""
    
    def __init__(self, x: float, y: float, goal: Exit):
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.array([
            random.uniform(-1, 1), 
            random.uniform(-1, 1)
        ], dtype=float)
        self.goal = goal
        
        # Параметры движения
        self.max_speed = random.uniform(30, 50)  # пикселей в секунду
        self.max_force = 2.0
        self.radius = 8
        self.perception_radius = 40
        
        # Веса для различных сил
        self.separation_weight = 2.5
        self.alignment_weight = 1.0
        self.cohesion_weight = 1.0
        self.goal_weight = 3.0
        self.wall_avoidance_weight = 8.0  # Увеличиваем вес избегания стен
        
        # Визуальные параметры
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.reached_goal = False
    
    def update(self, neighbors: List['Pedestrian'], walls: List[Wall], dt: float):
        """Обновление состояния пешехода"""
        if self.reached_goal:
            return
        
        # Сохраняем предыдущую позицию для проверки столкновений
        old_position = self.position.copy()
        
        # Получаем соседей в радиусе восприятия
        nearby_neighbors = self.get_nearby_neighbors(neighbors)
        
        # Применяем правила Boids
        separation = self.separate(nearby_neighbors) * self.separation_weight
        alignment = self.align(nearby_neighbors) * self.alignment_weight
        cohesion = self.cohesion(nearby_neighbors) * self.cohesion_weight
        
        # Движение к цели
        goal_seeking = self.seek_goal() * self.goal_weight
        
        # Избегание стен
        wall_avoidance = self.avoid_walls(walls) * self.wall_avoidance_weight
        
        # Суммируем все силы
        total_force = separation + alignment + cohesion + goal_seeking + wall_avoidance
        
        # Ограничиваем силу
        if np.linalg.norm(total_force) > self.max_force:
            total_force = total_force / np.linalg.norm(total_force) * self.max_force
        
        # Обновляем скорость и позицию
        self.velocity += total_force * dt
        
        # Ограничиваем скорость
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed
        
        # Обновляем позицию
        self.position += self.velocity * dt
        
        # Проверяем и исправляем столкновения со стенами
        self.resolve_wall_collisions(walls)
        
        # Ограничиваем движение границами экрана
        margin = self.radius
        self.position[0] = max(margin, min(SCREEN_WIDTH - margin, self.position[0]))
        self.position[1] = max(margin, min(SCREEN_HEIGHT - margin, self.position[1]))
        
        # Проверяем достижение цели
        if np.linalg.norm(self.position - self.goal.position) < self.goal.width:
            self.reached_goal = True
            self.goal.reached_count += 1
    
    def resolve_wall_collisions(self, walls: List[Wall]):
        """Разрешение столкновений со стенами"""
        for wall in walls:
            collision, correction = wall.check_collision(self.position, self.radius)
            if collision:
                self.position += correction
                # Отражаем скорость от стены для более реалистичного поведения
                normal = correction / np.linalg.norm(correction) if np.linalg.norm(correction) > 0 else np.array([0.0, 0.0])
                self.velocity -= 2 * np.dot(self.velocity, normal) * normal * 0.3  # частичное отражение
    
    def get_nearby_neighbors(self, neighbors: List['Pedestrian']) -> List['Pedestrian']:
        """Получение соседей в радиусе восприятия"""
        nearby = []
        for neighbor in neighbors:
            if neighbor != self and not neighbor.reached_goal:
                distance = np.linalg.norm(self.position - neighbor.position)
                if distance < self.perception_radius:
                    nearby.append(neighbor)
        return nearby
    
    def separate(self, neighbors: List['Pedestrian']) -> np.ndarray:
        """Правило разделения - избегание столкновений"""
        if not neighbors:
            return np.array([0.0, 0.0])
        
        steer = np.array([0.0, 0.0])
        count = 0
        
        for neighbor in neighbors:
            distance = np.linalg.norm(self.position - neighbor.position)
            if distance > 0 and distance < self.radius * 3:
                # Направление от соседа
                diff = self.position - neighbor.position
                diff = diff / distance  # нормализуем
                diff = diff / distance  # взвешиваем по обратному расстоянию
                steer += diff
                count += 1
        
        if count > 0:
            steer = steer / count
            # Нормализуем и масштабируем
            if np.linalg.norm(steer) > 0:
                steer = steer / np.linalg.norm(steer) * self.max_speed
                steer = steer - self.velocity
        
        return steer
    
    def align(self, neighbors: List['Pedestrian']) -> np.ndarray:
        """Правило выравнивания - синхронизация скорости и направления"""
        if not neighbors:
            return np.array([0.0, 0.0])
        
        average_velocity = np.array([0.0, 0.0])
        count = 0
        
        for neighbor in neighbors:
            average_velocity += neighbor.velocity
            count += 1
        
        if count > 0:
            average_velocity = average_velocity / count
            # Нормализуем до максимальной скорости
            if np.linalg.norm(average_velocity) > 0:
                average_velocity = average_velocity / np.linalg.norm(average_velocity) * self.max_speed
            steer = average_velocity - self.velocity
            return steer
        
        return np.array([0.0, 0.0])
    
    def cohesion(self, neighbors: List['Pedestrian']) -> np.ndarray:
        """Правило сплочения - движение к центру группы"""
        if not neighbors:
            return np.array([0.0, 0.0])
        
        center = np.array([0.0, 0.0])
        count = 0
        
        for neighbor in neighbors:
            center += neighbor.position
            count += 1
        
        if count > 0:
            center = center / count
            return self.seek(center)
        
        return np.array([0.0, 0.0])
    
    def seek_goal(self) -> np.ndarray:
        """Движение к цели (выходу)"""
        return self.seek(self.goal.position)
    
    def seek(self, target: np.ndarray) -> np.ndarray:
        """Базовое поведение поиска цели"""
        desired = target - self.position
        distance = np.linalg.norm(desired)
        
        if distance == 0:
            return np.array([0.0, 0.0])
        
        # Нормализуем и масштабируем до максимальной скорости
        desired = desired / distance * self.max_speed
        
        # Управляющая сила
        steer = desired - self.velocity
        return steer
    
    def avoid_walls(self, walls: List[Wall]) -> np.ndarray:
        """Избегание стен"""
        avoidance = np.array([0.0, 0.0])
        
        for wall in walls:
            repulsion = wall.get_repulsion_force(self.position, self.perception_radius)
            avoidance += repulsion
        
        return avoidance
    
    def draw(self, screen):
        """Отрисовка пешехода"""
        if self.reached_goal:
            return
        
        # Рисуем круг пешехода
        pygame.draw.circle(screen, self.color, 
                         (int(self.position[0]), int(self.position[1])), 
                         self.radius)
        
        # Рисуем направление движения
        if np.linalg.norm(self.velocity) > 0:
            direction = self.velocity / np.linalg.norm(self.velocity) * 15
            end_pos = self.position + direction
            pygame.draw.line(screen, BLACK, 
                           (int(self.position[0]), int(self.position[1])),
                           (int(end_pos[0]), int(end_pos[1])), 2)

class Environment:
    """Класс среды с коридорами и препятствиями"""
    
    def __init__(self):
        self.walls = []
        self.exits = []
        self.create_environment()
    
    def create_environment(self):
        """Создание среды с коридорами и выходами"""
        # Внешние стены
        self.walls.extend([
            Wall((30, 30), (SCREEN_WIDTH - 30, 30)),      # верх
            Wall((SCREEN_WIDTH - 30, 30), (SCREEN_WIDTH - 30, SCREEN_HEIGHT - 30)),  # право
            Wall((SCREEN_WIDTH - 30, SCREEN_HEIGHT - 30), (30, SCREEN_HEIGHT - 30)), # низ
            Wall((30, SCREEN_HEIGHT - 30), (30, 30))       # лево
        ])
        
        # Внутренние препятствия - создаем коридоры
        # Горизонтальная стена с проходами
        self.walls.extend([
            Wall((150, 200), (300, 200)),
            Wall((400, 200), (550, 200)),
            Wall((650, 200), (800, 200))
        ])
        
        # Вертикальные препятствия
        self.walls.extend([
            Wall((300, 100), (300, 170)),
            Wall((550, 230), (550, 450)),
            Wall((700, 80), (700, 170))
        ])
        
        # Создаем выходы
        self.exits = [
            Exit((SCREEN_WIDTH - 30, SCREEN_HEIGHT // 2), 50),  # правый выход
            Exit((SCREEN_WIDTH // 2, 30), 50),                  # верхний выход
        ]
    
    def draw(self, screen):
        """Отрисовка среды"""
        # Рисуем стены
        for wall in self.walls:
            pygame.draw.line(screen, DARK_GRAY, wall.start, wall.end, 8)
        
        # Рисуем выходы
        for exit in self.exits:
            pygame.draw.circle(screen, GREEN, 
                             (int(exit.position[0]), int(exit.position[1])), 
                             int(exit.width), 3)
            pygame.draw.circle(screen, LIGHT_GRAY, 
                             (int(exit.position[0]), int(exit.position[1])), 
                             int(exit.width))

class Simulation:
    """Основной класс симуляции"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Симуляция движения пешеходов (Boids + Goal Seeking)")
        self.clock = pygame.time.Clock()
        
        self.environment = Environment()
        self.pedestrians = []
        self.font = pygame.font.Font(None, 24)
        
        # Параметры эксперимента
        self.pedestrian_count = 60  # уменьшаем количество для меньшего окна
        self.density_multiplier = 1.0
        self.paused = False  # Добавляем флаг паузы
        
        self.create_pedestrians()
        
        # Статистика
        self.total_created = 0
        self.start_time = pygame.time.get_ticks()
    
    def create_pedestrians(self):
        """Создание пешеходов"""
        self.pedestrians = []
        count = int(self.pedestrian_count * self.density_multiplier)
        
        for _ in range(count):
            # Случайное начальное положение в левой части экрана
            x = random.uniform(60, 200)
            y = random.uniform(80, SCREEN_HEIGHT - 80)
            
            # Случайный выбор цели
            goal = random.choice(self.environment.exits)
            
            pedestrian = Pedestrian(x, y, goal)
            self.pedestrians.append(pedestrian)
        
        self.total_created = len(self.pedestrians)
    
    def update(self, dt: float):
        """Обновление симуляции"""
        if not self.paused:  # Обновляем только если не на паузе
            for pedestrian in self.pedestrians:
                pedestrian.update(self.pedestrians, self.environment.walls, dt)
    
    def draw_statistics(self):
        """Отрисовка статистики"""
        active_count = sum(1 for p in self.pedestrians if not p.reached_goal)
        reached_count = sum(exit.reached_count for exit in self.environment.exits)
        
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000.0
        
        stats = [
            f"Активных пешеходов: {active_count}",
            f"Достигли цели: {reached_count}",
            f"Общее количество: {self.total_created}",
            f"Плотность: {self.density_multiplier:.1f}x",
            f"Время: {elapsed_time:.1f}с",
            f"Пауза: {'ВКЛ' if self.paused else 'ВЫКЛ'}",
            "",
            "Управление:",
            "R - перезапуск",
            "1,2,3 - изменить плотность",
            "Пробел - пауза/продолжить"
        ]
        
        y_offset = 10
        for stat in stats:
            if stat:  # не пустая строка
                text = self.font.render(stat, True, BLACK)
                self.screen.blit(text, (10, y_offset))
            y_offset += 25
    
    def draw_density_visualization(self):
        """Визуализация плотности скопления"""
        # Создаем сетку для подсчета плотности
        grid_size = 40
        grid_width = SCREEN_WIDTH // grid_size
        grid_height = SCREEN_HEIGHT // grid_size
        density_grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
        
        # Подсчитываем пешеходов в каждой клетке
        for pedestrian in self.pedestrians:
            if not pedestrian.reached_goal:
                grid_x = int(pedestrian.position[0] // grid_size)
                grid_y = int(pedestrian.position[1] // grid_size)
                if 0 <= grid_x < grid_width and 0 <= grid_y < grid_height:
                    density_grid[grid_y][grid_x] += 1
        
        # Отрисовываем области высокой плотности
        for y in range(grid_height):
            for x in range(grid_width):
                if density_grid[y][x] > 4:  # порог высокой плотности
                    # Используем простой способ без альфа-канала
                    intensity = min(255, density_grid[y][x] * 40)
                    red_value = min(255, 100 + intensity)
                    color = (red_value, 100, 100)  # красноватый оттенок
                    
                    rect = pygame.Rect(x * grid_size, y * grid_size, grid_size, grid_size)
                    pygame.draw.rect(self.screen, color, rect)
    
    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Перезапуск симуляции
                    self.start_time = pygame.time.get_ticks()
                    for exit in self.environment.exits:
                        exit.reached_count = 0
                    self.create_pedestrians()
                
                elif event.key == pygame.K_1:
                    self.density_multiplier = 0.5
                    self.create_pedestrians()
                
                elif event.key == pygame.K_2:
                    self.density_multiplier = 1.0
                    self.create_pedestrians()
                
                elif event.key == pygame.K_3:
                    self.density_multiplier = 2.0
                    self.create_pedestrians()
                
                elif event.key == pygame.K_SPACE:
                    # Переключаем паузу
                    self.paused = not self.paused
        
        return True
    
    def run(self):
        """Главный цикл симуляции"""
        running = True
        
        while running:
            dt = self.clock.tick(FPS) / 1000.0  # время в секундах
            
            running = self.handle_events()
            
            # Обновление
            self.update(dt)
            
            # Отрисовка с индикацией паузы
            self.screen.fill(WHITE)
            
            # Если на паузе, добавляем полупрозрачный оверлей
            if self.paused:
                pause_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                pause_surface.set_alpha(50)
                pause_surface.fill(BLUE)
                self.screen.blit(pause_surface, (0, 0))
            
            # Визуализация плотности
            self.draw_density_visualization()
            
            # Отрисовка среды
            self.environment.draw(self.screen)
            
            # Отрисовка пешеходов
            for pedestrian in self.pedestrians:
                pedestrian.draw(self.screen)
            
            # Статистика
            self.draw_statistics()
            
            # Если на паузе, показываем большой текст
            if self.paused:
                pause_font = pygame.font.Font(None, 72)
                pause_text = pause_font.render("ПАУЗА", True, RED)
                text_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                self.screen.blit(pause_text, text_rect)
            
            pygame.display.flip()
        
        pygame.quit()

if __name__ == "__main__":
    simulation = Simulation()
    simulation.run()