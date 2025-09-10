import java.util.Random;

public class MinimaxAlphaBeta {
    static class Result {
        int value;
        long nodesVisited;
        Result(int v, long n) { value = v; nodesVisited = n; }
    }

    // Генерация случайных листовых значений для полного k-арного дерева глубины d
    static int[] generateLeaves(int branching, int depth, int seed) {
        int leaves = (int) Math.pow(branching, depth);
        int[] arr = new int[leaves];
        Random rnd = new Random(seed);
        for (int i = 0; i < leaves; i++) {
            // случайное целое в диапазоне [-50, 50]
            arr[i] = rnd.nextInt(101) - 50;
        }
        return arr;
    }

    // Обычный мини-макс, рекурсивный
    static Result minimax(int depth, int branching, int index, boolean isMax, int[] leaves) {
        if (depth == 0) {
            return new Result(leaves[index], 1);
        }
        long nodes = 1; // текущий узел
        int best = isMax ? Integer.MIN_VALUE : Integer.MAX_VALUE;
        for (int i = 0; i < branching; i++) {
            int childIndex = index * branching + i;
            Result r = minimax(depth - 1, branching, childIndex, !isMax, leaves);
            nodes += r.nodesVisited;
            if (isMax) {
                best = Math.max(best, r.value);
            } else {
                best = Math.min(best, r.value);
            }
        }
        return new Result(best, nodes);
    }

    // Мини-макс с альфа-бета отсечением
    static Result alphabeta(int depth, int branching, int index, int alpha, int beta, boolean isMax, int[] leaves) {
        if (depth == 0) {
            return new Result(leaves[index], 1);
        }
        long nodes = 1;
        int value = isMax ? Integer.MIN_VALUE : Integer.MAX_VALUE;

        for (int i = 0; i < branching; i++) {
            int childIndex = index * branching + i;
            Result r = alphabeta(depth - 1, branching, childIndex, alpha, beta, !isMax, leaves);
            nodes += r.nodesVisited;
            if (isMax) {
                value = Math.max(value, r.value);
                alpha = Math.max(alpha, value);
            } else {
                value = Math.min(value, r.value);
                beta = Math.min(beta, value);
            }
            // отсечение
            if (beta <= alpha) {
                break;
            }
        }
        return new Result(value, nodes);
    }

    public static void main(String[] args) {
        int depth = 5;       // глубина дерева
        int branching = 3;   // ширина (ветвление)
        int seed = 42;       // фиксируем зерно для воспроизводимости

        int[] leaves = generateLeaves(branching, depth, seed);

        // Запуск обычного минимакса
        long t0 = System.nanoTime();
        Result mm = minimax(depth, branching, 0, true, leaves);
        long t1 = System.nanoTime();

        // Запуск альфа-бета
        long t2 = System.nanoTime();
        Result ab = alphabeta(depth, branching, 0, Integer.MIN_VALUE, Integer.MAX_VALUE, true, leaves);
        long t3 = System.nanoTime();

        System.out.println("Depth: " + depth + ", Branching: " + branching);
        System.out.println("Leaves count: " + leaves.length);
        System.out.println();
        System.out.println("Minimax result: value = " + mm.value +
                ", nodes visited = " + mm.nodesVisited +
                ", time ms = " + ((t1 - t0) / 1_000_000.0));
        System.out.println("Alpha-Beta result: value = " + ab.value +
                ", nodes visited = " + ab.nodesVisited +
                ", time ms = " + ((t3 - t2) / 1_000_000.0));
    }
}
