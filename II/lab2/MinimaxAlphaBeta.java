import java.util.Random; // чтобы создавать случайные числа для листьев дерева

public class MinimaxAlphaBeta {

    // Класс, чтобы хранить результат поиска
    // value - лучший найденный результат
    // nodesVisited - сколько всего узлов проверили
    static class Result {
        int value;          // лучшее число в этой ветке
        long nodesVisited;  // количество проверенных узлов
        Result(int v, long n) { value = v; nodesVisited = n; } // конструктор
    }

    // Метод для генерации листьев дерева
    // branching - сколько детей у каждого узла
    // depth - сколько уровней в дереве
    // seed - чтобы случайные числа всегда были одинаковыми
    static int[] generateLeaves(int branching, int depth, int seed) {
        int leaves = (int) Math.pow(branching, depth); // всего листьев = branching^depth
        int[] arr = new int[leaves];                   // создаём массив для листьев
        Random rnd = new Random(seed);                 // создаём генератор случайных чисел
        for (int i = 0; i < leaves; i++) {            // для каждого листа
            arr[i] = rnd.nextInt(101) - 50;           // случайное число от -50 до 50
        }
        return arr;                                    // возвращаем массив чисел
    }

    // Обычный Минимакс
    // depth - текущая глубина
    // branching - сколько детей у каждого узла
    // index - индекс текущего узла
    // isMax - true, если сейчас ход Макса, false - если Мина
    // leaves - массив листьев
    static Result minimax(int depth, int branching, int index, boolean isMax, int[] leaves) {
        if (depth == 0) { // если дошли до конца дерева (лист)
            return new Result(leaves[index], 1); // возвращаем число листа и говорим, что один узел просмотрен
        }

        long nodes = 1; // считаем текущий узел
        int best = isMax ? Integer.MIN_VALUE : Integer.MAX_VALUE; // начальное лучшее число

        for (int i = 0; i < branching; i++) {             // перебираем всех детей
            int childIndex = index * branching + i;       // индекс ребёнка в массиве листьев
            Result r = minimax(depth - 1, branching, childIndex, !isMax, leaves); // рекурсивно проверяем ребёнка
            nodes += r.nodesVisited;                       // добавляем, сколько узлов проверили
            if (isMax) best = Math.max(best, r.value);    // Макс хочет максимум
            else best = Math.min(best, r.value);          // Мин хочет минимум
        }
        return new Result(best, nodes); // возвращаем лучший результат и сколько узлов проверили
    }

    // Минимакс с альфа-бета отсечением
    // alpha - лучший результат для Макса (нижняя граница)
    // beta - лучший результат для Мина (верхняя граница)
    static Result alphabeta(int depth, int branching, int index, int alpha, int beta, boolean isMax, int[] leaves) {
        if (depth == 0) { // если дошли до листа
            return new Result(leaves[index], 1); // возвращаем значение листа
        }

        long nodes = 1; // считаем текущий узел
        int value = isMax ? Integer.MIN_VALUE : Integer.MAX_VALUE; // стартовое лучшее число

        for (int i = 0; i < branching; i++) { // проверяем всех детей
            int childIndex = index * branching + i; // индекс ребёнка
            Result r = alphabeta(depth - 1, branching, childIndex, alpha, beta, !isMax, leaves); // рекурсивно вызываем
            nodes += r.nodesVisited; // добавляем просмотренные узлы

            if (isMax) {                  // если ход Макса
                value = Math.max(value, r.value); // Макс хочет максимум
                alpha = Math.max(alpha, value);   // обновляем альфу
            } else {                        // если ход Мина
                value = Math.min(value, r.value); // Мин хочет минимум
                beta = Math.min(beta, value);     // обновляем бету
            }

            if (beta <= alpha) break; // если стало понятно, что дальше лучше не будет → выходим
        }

        return new Result(value, nodes); // возвращаем лучший результат и сколько узлов проверили
    }

    public static void main(String[] args) {
        int depth = 5;       // дерево с 5 уровнями
        int branching = 3;   // каждый узел имеет 3 ребёнка
        int seed = 42;       // чтобы числа всегда одинаковые при каждом запуске

        int[] leaves = generateLeaves(branching, depth, seed); // создаём листья

        // запускаем обычный Минимакс и измеряем время
        long t0 = System.nanoTime();
        Result mm = minimax(depth, branching, 0, true, leaves); // true = Макс ходит первым
        long t1 = System.nanoTime();

        // запускаем Альфа-Бета и измеряем время
        long t2 = System.nanoTime();
        Result ab = alphabeta(depth, branching, 0, Integer.MIN_VALUE, Integer.MAX_VALUE, true, leaves);
        long t3 = System.nanoTime();

        // выводим общую информацию
        System.out.println("Depth: " + depth + ", Branching: " + branching);
        System.out.println("Leaves count: " + leaves.length);
        System.out.println();

        // выводим результат Минимакса
        System.out.println("Minimax result: value = " + mm.value +
                ", nodes visited = " + mm.nodesVisited +
                ", time ms = " + ((t1 - t0) / 1_000_000.0));

        // выводим результат Альфа-Бета
        System.out.println("Alpha-Beta result: value = " + ab.value +
                ", nodes visited = " + ab.nodesVisited +
                ", time ms = " + ((t3 - t2) / 1_000_000.0));
    }
}
