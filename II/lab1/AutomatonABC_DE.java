import java.util.Scanner;

public class AutomatonABC_DE {

    /**
     * Проверяем, подходит ли строка под шаблон:
     * a(abc)^n(de)^m, где n+m >= 1
     */
    public static boolean accepts(String s) {
        // отбрасываем всякий мусор
        if (s == null) return false;         // null точно не подойдёт
        if (s.length() == 0) return false;   // пустая строка тоже
        if (s.charAt(0) != 'a') return false; // строка обязана начинаться с 'a'

        int n = 0; // сколько раз встретили полный блок "abc"
        int m = 0; // сколько раз встретили полный блок "de"

        boolean deStarted = false; // переключатель: перешли ли мы к "de"-части?

        int abcPos = 0; // где мы находимся внутри блока "abc"
        // 0 - ждём 'a' (или переход в 'd')
        // 1 - ждём 'b'
        // 2 - ждём 'c'
        int dePos = 0;  // где мы находимся внутри блока "de"
        // 0 - ждём 'd'
        // 1 - ждём 'e'

        int i = 1; // начинаем проверку со второго символа (первый уже 'a')

        // крутимся по строке
        while (i < s.length()) {
            char ch = s.charAt(i);

            if (!deStarted) {
                // пока ещё в зоне "abc"-блоков
                if (abcPos == 0) {
                    if (ch == 'a') {
                        abcPos = 1; // нашли начало "abc"
                        i++;
                    } else if (ch == 'd') {
                        // встречаем 'd' — пора переключиться на "de"-блоки
                        deStarted = true;
                        dePos = 1; // уже прочитали 'd', теперь ждём 'e'
                        i++;
                    } else {
                        return false; // что-то чужое прилетело
                    }
                } else if (abcPos == 1) {
                    if (ch == 'b') {
                        abcPos = 2; // ок, ждём 'c'
                        i++;
                    } else {
                        return false; // вместо 'b' что-то другое
                    }
                } else { // abcPos == 2
                    if (ch == 'c') {
                        n++;        // блок "abc" завершён
                        abcPos = 0; // можно начинать следующий
                        i++;
                    } else {
                        return false; // ждали 'c', а пришло не то
                    }
                }
            } else {
                // теперь в зоне "de"-блоков
                if (dePos == 0) {
                    if (ch == 'd') {
                        dePos = 1; // ок, ждём 'e'
                        i++;
                    } else {
                        return false; // ожидали 'd', а пришло не то
                    }
                } else { // dePos == 1
                    if (ch == 'e') {
                        m++;        // получили полный "de"
                        dePos = 0; // ждём снова 'd'
                        i++;
                    } else {
                        return false; // ждали 'e', а пришло что-то другое
                    }
                }
            }
        }

        // проверка на неполные блоки
        if (!deStarted) {
            if (abcPos == 1 || abcPos == 2) return false; // застряли внутри "abc"
        } else {
            if (dePos == 1) return false; // застряли внутри "de" (нашёлся 'd' без 'e')
        }

        // нужно хотя бы одно вхождение "abc" или "de"
        if (n + m < 1) return false;

        return true; // если дошли сюда — строка подходит
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Введите строку в формате: a(abc)^n(de)^m, где n+m>=1");
        while (true) {
            System.out.print("> ");
            String line = sc.nextLine();
            if (line == null || line.isEmpty()) break; // пустая строка = выход
            if (accepts(line)) {
                System.out.println("ACCEPTED"); // строка подошла
            } else {
                System.out.println("REJECTED"); // не подошла
            }
        }
        sc.close();
    }
}
