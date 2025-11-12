
import random
import math
import matplotlib.pyplot as plt
from typing import List, Tuple
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

L = 4                # Длина хромосомы (фиксированная)
MAX_INT = 2**L - 1   # Максимальное значение для декодирования (15)




def decode(bits: List[int]) -> float:
    """
    Декодирование хромосомы в x ∈ [0,1]
    Преобразует двоичную строку в десятичное число,
    затем нормализует в диапазон [0, 1]

    """
    binary_string = "".join(str(b) for b in bits)
    decimal_value = int(binary_string, 2)
    x = decimal_value / MAX_INT
    return x


def fitness(bits: List[int]) -> float:
    """
    Функция приспособленности
    Максимум функции находится в точке x = 0.5, где f(0.5) = 1.0
    """
    x = decode(bits)
    return math.exp(-(x - 0.5)**2)


def random_population(N: int) -> List[List[int]]:
    """
    Инициализация популяции.
    Создание N случайных хромосом длиной L битов.
    """
    return [[random.randint(0, 1) for _ in range(L)] for _ in range(N)]


def tournament_selection(pop: List[List[int]], fitnesses: List[float], k: int = 3) -> int:
    """
    Турнирная селекция.
    Выбирает k случайных особей и возвращает индекс лучшей из них.
    Это один из наиболее популярных методов селекции в ГА.
    """
    selected_indices = random.sample(range(len(pop)), k)
    winner_index = max(selected_indices, key=lambda i: fitnesses[i])
    return winner_index


def one_point_crossover(p1: List[int], p2: List[int], pc: float) -> Tuple[List[int], List[int], bool, int]:
    """
    Одноточечный кроссовер (скрещивание).
    С вероятностью pc выполняется обмен генетическим материалом
    между двумя родителями в случайной точке разреза.

    """
    if random.random() <= pc:
        point = random.randint(1, L - 1)
        child1 = p1[:point] + p2[point:]
        child2 = p2[:point] + p1[point:]
        return child1, child2, True, point
    else:
        return p1[:], p2[:], False, None


def mutate(chrom: List[int], pm: float) -> List[int]:
    """
    Побитовая мутация.
    
    Каждый бит хромосомы с вероятностью pm инвертируется (0→1 или 1→0).
    Мутация обеспечивает разнообразие популяции и помогает избежать
    локальных оптимумов.
    """
    mutated_bits = []
    for i in range(len(chrom)):
        if random.random() <= pm:
            chrom[i] = 1 - chrom[i]  # Инверсия бита
            mutated_bits.append(i)
    return mutated_bits


def run_ga(N: int = 4, pc: float = 0.8, pm: float = 0.05, G: int = 30, 
           verbose: bool = True, seed: int = None) -> dict:
    """
    Запуск генетического алгоритма.
        N: размер популяции
        pc: вероятность кроссовера
        pm: вероятность мутации
        G: количество поколений
        verbose: выводить ли подробные логи
        seed: seed для воспроизводимости результатов
    """
    if seed is not None:
        random.seed(seed)
    
    # Инициализация популяции
    population = random_population(N)
    history = []
    
    print(f"\n{'='*80}")
    print(f"ЗАПУСК ГЕНЕТИЧЕСКОГО АЛГОРИТМА")
    print(f"{'='*80}")
    print(f"Параметры:")
    print(f"  - Размер популяции (N): {N}")
    print(f"  - Вероятность кроссовера (pc): {pc}")
    print(f"  - Вероятность мутации (pm): {pm}")
    print(f"  - Количество поколений (G): {G}")
    print(f"  - Длина хромосомы (L): {L}")
    print(f"  - Функция: f(x) = e^(-(x - 0.5)^2), x ∈ [0,1]")
    print(f"  - Теоретический оптимум: x = 0.5, f(x) = 1.0")
    print(f"{'='*80}\n")
    
    for generation in range(1, G + 1):
        fitnesses = [fitness(individual) for individual in population]
        max_fitness = max(fitnesses)
        min_fitness = min(fitnesses)
        avg_fitness = sum(fitnesses) / len(fitnesses)
        
        best_idx = fitnesses.index(max_fitness)
        best_individual = population[best_idx]
        best_x = decode(best_individual)
        
        history.append({
            'generation': generation,
            'best_x': best_x,
            'best_fitness': max_fitness,
            'max_fitness': max_fitness,
            'min_fitness': min_fitness,
            'avg_fitness': avg_fitness,
            'population': [ind[:] for ind in population],
            'fitnesses': fitnesses[:]
        })

        if verbose:
            print(f"\n{'─'*80}")
            print(f"ПОКОЛЕНИЕ {generation}")
            print(f"{'─'*80}")
            print(f"{'№':<4} {'Хромосома':<12} {'x':<10} {'f(x)':<12} {'Приспособленность'}")
            print(f"{'─'*80}")
            
            for i, ind in enumerate(population):
                binary_str = ''.join(str(b) for b in ind)
                x_val = decode(ind)
                f_val = fitnesses[i]
                marker = " ← ЛУЧШАЯ" if i == best_idx else ""
                print(f"{i+1:<4} {binary_str:<12} {x_val:<10.6f} {f_val:<12.6f}{marker}")
            
            print(f"{'─'*80}")
            print(f"Статистика поколения:")
            print(f"  Максимальный fitness: {max_fitness:.6f} (особь #{best_idx+1}, x={best_x:.6f})")
            print(f"  Минимальный fitness:  {min_fitness:.6f}")
            print(f"  Средний fitness:      {avg_fitness:.6f}")
            print(f"  Разнообразие:         {max_fitness - min_fitness:.6f}")
        
    
        new_population = []
        generation_logs = []
        
        while len(new_population) < N:
            # Селекция родителей
            parent1_idx = tournament_selection(population, fitnesses)
            parent2_idx = tournament_selection(population, fitnesses)
            
            parent1 = population[parent1_idx][:]
            parent2 = population[parent2_idx][:]
            
            # Кроссовер
            child1, child2, crossover_occurred, crossover_point = one_point_crossover(
                parent1, parent2, pc
            )
            
            if crossover_occurred and verbose:
                p1_str = ''.join(str(b) for b in parent1)
                p2_str = ''.join(str(b) for b in parent2)
                c1_str = ''.join(str(b) for b in child1)
                c2_str = ''.join(str(b) for b in child2)
                
                log = (f"\n  КРОССОВЕР между особями #{parent1_idx+1} и #{parent2_idx+1} "
                       f"в точке {crossover_point}:\n"
                       f"    Родитель 1: {p1_str} → Потомок 1: {c1_str}\n"
                       f"    Родитель 2: {p2_str} → Потомок 2: {c2_str}")
                generation_logs.append(log)
            
            # Мутация потомка 1
            mutated_bits1 = mutate(child1, pm)
            if mutated_bits1 and verbose:
                c1_str = ''.join(str(b) for b in child1)
                log = (f"\n  МУТАЦИЯ в потомке 1: биты {mutated_bits1} изменены. "
                       f"Результат: {c1_str}")
                generation_logs.append(log)
            
            # Мутация потомка 2
            mutated_bits2 = mutate(child2, pm)
            if mutated_bits2 and verbose:
                c2_str = ''.join(str(b) for b in child2)
                log = (f"\n  МУТАЦИЯ в потомке 2: биты {mutated_bits2} изменены. "
                       f"Результат: {c2_str}")
                generation_logs.append(log)
            
            # Добавление потомков в новую популяцию
            new_population.append(child1)
            if len(new_population) < N:
                new_population.append(child2)
        
        # Вывод логов генетических операторов
        if verbose and generation_logs:
            print(f"\nПрименённые генетические операторы:")
            for log in generation_logs:
                print(log)
        
        # Замена популяции
        population = new_population
    
    # Финальная оценка
    final_fitnesses = [fitness(ind) for ind in population]
    final_best_idx = final_fitnesses.index(max(final_fitnesses))
    final_best = population[final_best_idx]
    final_x = decode(final_best)
    final_fitness = final_fitnesses[final_best_idx]
    
    print(f"\n{'='*80}")
    print(f"ИТОГОВЫЕ РЕЗУЛЬТАТЫ")
    print(f"{'='*80}")
    print(f"Найденное решение:")
    print(f"  x* = {final_x:.6f}")
    print(f"  f(x*) = {final_fitness:.6f}")
    print(f"  Хромосома: {''.join(str(b) for b in final_best)}")
    print(f"\nТеоретический оптимум:")
    print(f"  x = 0.5000")
    print(f"  f(x) = 1.0000")
    print(f"\nОтклонение от оптимума:")
    print(f"  Δx = {abs(final_x - 0.5):.6f}")
    print(f"  Δf = {abs(final_fitness - 1.0):.6f}")
    print(f"  Точность: {final_fitness * 100:.2f}%")
    print(f"{'='*80}\n")
    
    return {
        'history': history,
        'final_x': final_x,
        'final_fitness': final_fitness,
        'final_individual': final_best,
        'parameters': {'N': N, 'pc': pc, 'pm': pm, 'G': G}
    }



def plot_results(experiments: dict):
    fig, axes = plt.subplots(2, 2, figsize=(16, 11))
    
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E']
    markers = ['o', 's', '^', 'D', 'v']
    
    # График 1: Максимальный fitness
    ax1 = axes[0, 0]
    for idx, (name, result) in enumerate(experiments.items()):
        history = result['history']
        gens = [h['generation'] for h in history]
        max_f = [h['max_fitness'] for h in history]
        
        ax1.plot(gens, max_f, label=name, marker=markers[idx % len(markers)], 
                markersize=4, linewidth=2.5, color=colors[idx % len(colors)], 
                alpha=0.85, markevery=max(1, len(gens)//20))
    
    ax1.axhline(y=1.0, color='red', linestyle='--', linewidth=2, 
               label='Theoretical optimum', alpha=0.7)
    ax1.set_title("Evolution of Maximum Fitness", fontsize=14, fontweight='bold', pad=15)
    ax1.set_xlabel("Generation", fontsize=12)
    ax1.set_ylabel("Max fitness", fontsize=12)
    ax1.legend(fontsize=9, loc='lower right', framealpha=0.9)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_ylim([0.75, 1.05])
    
    # График 2: Средний fitness
    ax2 = axes[0, 1]
    for idx, (name, result) in enumerate(experiments.items()):
        history = result['history']
        gens = [h['generation'] for h in history]
        avg_f = [h['avg_fitness'] for h in history]
        
        ax2.plot(gens, avg_f, label=name, marker=markers[idx % len(markers)], 
                markersize=4, linewidth=2.5, color=colors[idx % len(colors)], 
                alpha=0.85, markevery=max(1, len(gens)//20))
    
    ax2.set_title("Evolution of Average Fitness", fontsize=14, fontweight='bold', pad=15)
    ax2.set_xlabel("Generation", fontsize=12)
    ax2.set_ylabel("Avg fitness", fontsize=12)
    ax2.legend(fontsize=9, loc='lower right', framealpha=0.9)
    ax2.grid(True, alpha=0.3, linestyle='--')
    
    # График 3: Лучшее значение x
    ax3 = axes[1, 0]
    for idx, (name, result) in enumerate(experiments.items()):
        history = result['history']
        gens = [h['generation'] for h in history]
        best_x = [h['best_x'] for h in history]
        
        ax3.plot(gens, best_x, label=name, marker=markers[idx % len(markers)], 
                markersize=4, linewidth=2.5, color=colors[idx % len(colors)], 
                alpha=0.85, markevery=max(1, len(gens)//20))
    
    ax3.axhline(y=0.5, color='red', linestyle='--', linewidth=2, 
               label='Optimum (x=0.5)', alpha=0.7)
    ax3.set_title("Convergence to Optimal x", fontsize=14, fontweight='bold', pad=15)
    ax3.set_xlabel("Generation", fontsize=12)
    ax3.set_ylabel("Best x", fontsize=12)
    ax3.legend(fontsize=9, loc='best', framealpha=0.9)
    ax3.grid(True, alpha=0.3, linestyle='--')
    ax3.set_ylim([0, 1])
    
    # График 4: Разнообразие популяции
    ax4 = axes[1, 1]
    for idx, (name, result) in enumerate(experiments.items()):
        history = result['history']
        gens = [h['generation'] for h in history]
        diversity = [h['max_fitness'] - h['min_fitness'] for h in history]
        
        ax4.plot(gens, diversity, label=name, marker=markers[idx % len(markers)], 
                markersize=4, linewidth=2.5, color=colors[idx % len(colors)], 
                alpha=0.85, markevery=max(1, len(gens)//20))
    
    ax4.set_title("Population Diversity (max - min fitness)", 
                 fontsize=14, fontweight='bold', pad=15)
    ax4.set_xlabel("Generation", fontsize=12)
    ax4.set_ylabel("Fitness range", fontsize=12)
    ax4.legend(fontsize=9, loc='best', framealpha=0.9)
    ax4.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout(pad=2.5)
    plt.savefig('genetic_algorithm_results.png', dpi=300, bbox_inches='tight')
    print("\nГрафики сохранены в файл 'genetic_algorithm_results.png'")
    plt.show()

if __name__ == "__main__":
    print("\n" + "="*80)
    print(" "*20 + "ЛАБОРАТОРНАЯ РАБОТА №6")
    print(" "*10 + "Генетический алгоритм для функции f(x) = e^(-(x-0.5)^2)")
    print("="*80)
    

    experiments_config = [
        ("Exp1: Base (pc=0.8, pm=0.05)", 0.8, 0.05, 4),
        ("Exp2: High crossover (pc=0.95, pm=0.02)", 0.95, 0.02, 4),
        ("Exp3: High mutation (pc=0.6, pm=0.15)", 0.6, 0.15, 4),
    ]
    
    experiments_results = {}

    for name, pc, pm, N in experiments_config:
        print(f"\n\n{'#'*80}")
        print(f"# {name}")
        print(f"{'#'*80}")
        
        result = run_ga(N=N, pc=pc, pm=pm, G=50, verbose=True, seed=42)
        experiments_results[name] = result
        
        input("\nНажмите Enter для продолжения...")
    
    # Сравнительный анализ
    print(f"\n\n{'='*80}")
    print(" "*25 + "СРАВНИТЕЛЬНЫЙ АНАЛИЗ")
    print(f"{'='*80}\n")
    
    print(f"{'Эксперимент':<40} {'x*':<12} {'f(x*)':<12} {'Δx':<12} {'Δf':<12}")
    print(f"{'─'*80}")
    
    for name, result in experiments_results.items():
        x_star = result['final_x']
        f_star = result['final_fitness']
        delta_x = abs(x_star - 0.5)
        delta_f = abs(f_star - 1.0)
        
        print(f"{name:<40} {x_star:<12.6f} {f_star:<12.6f} {delta_x:<12.6f} {delta_f:<12.6f}")
    
    print(f"{'─'*80}\n")
    
    plot_results(experiments_results)
    
    # Выводы
    print(f"\n{'='*80}")
    print(" "*30 + "ВЫВОДЫ")
    print(f"{'='*80}")
    print("""
1. ВЛИЯНИЕ ВЕРОЯТНОСТИ КРОССОВЕРА (pc):
   - Высокий pc (0.95) способствует быстрому обмену генетической информацией
   - Низкий pc (0.6) замедляет конвергенцию, но может помочь избежать
     преждевременной сходимости к локальному оптимуму

2. ВЛИЯНИЕ ВЕРОЯТНОСТИ МУТАЦИИ (pm):
   - Высокий pm (0.15) увеличивает разнообразие популяции и помогает
     исследовать пространство поиска, но может нарушать хорошие решения
   - Низкий pm (0.02) обеспечивает стабильную конвергенцию, но может
     привести к застреванию в локальных оптимумах

3. ОПТИМАЛЬНЫЙ БАЛАНС:
   - Для данной задачи базовые параметры (pc=0.8, pm=0.05) показали
     хорошую сходимость к глобальному оптимуму
   - Важно поддерживать баланс между эксплуатацией (кроссовер) и
     исследованием (мутация) пространства поиска

4. РАЗМЕР ПОПУЛЯЦИИ:
   - При малом N (4) алгоритм может работать быстро, но с риском потери
     разнообразия и застревания в локальных оптимумах
    """)
    print(f"{'='*80}\n")
