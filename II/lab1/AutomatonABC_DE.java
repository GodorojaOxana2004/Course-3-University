import java.util.Scanner;

public class AutomatonABC_DE {
    public static boolean accepts(String s) {
        if (s == null) return false;
        if (s.length() == 0) return false;
        if (s.charAt(0) != 'a') return false;

        int n = 0; 
        int m = 0; 
        boolean deStarted = false;
        int abcPos = 0;
        int dePos = 0;

        int i = 1; 
        while (i < s.length()) {
            char ch = s.charAt(i);

            if (!deStarted) {
               
                if (abcPos == 0) {
                    if (ch == 'a') {
                        abcPos = 1;
                        i++;
                    } else if (ch == 'd') {
                        deStarted = true;
                        dePos = 1; 
                        i++;
                    } else {
                        return false; 
                    }
                } else if (abcPos == 1) {
                    if (ch == 'b') {
                        abcPos = 2;
                        i++;
                    } else {
                        return false;
                    }
                } else { // abcPos == 2
                    if (ch == 'c') {
                        n++;
                        abcPos = 0;
                        i++;
                    } else {
                        return false;
                    }
                }
            } else {
                //режим de-блоков — допускаются только 'd' и 'e' в корректном порядке
                if (dePos == 0) {
                    if (ch == 'd') {
                        dePos = 1; 
                        i++;
                    } else {
                        return false;
                    }
                } else { 
                    if (ch == 'e') {
                        m++;
                        dePos = 0; 
                        i++;
                    } else {
                        return false;
                    }
                }
            }
        }

        
        if (!deStarted) {
            if (abcPos == 1 || abcPos == 2) return false;
        } else {
            if (dePos == 1) return false;
        }

        
        if (n + m < 1) return false;

        return true;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter lines. Format: a(abc)^n(de)^m, n+m>=1");
        while (true) {
            System.out.print("> ");
            String line = sc.nextLine();
            if (line == null || line.isEmpty()) break;
            if (accepts(line)) {
                System.out.println("ACCEPTED");
            } else {
                System.out.println("REJECTED");
            }
        }
        sc.close();
    }
}
