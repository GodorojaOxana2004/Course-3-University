package org.example.mask;

import org.example.model.Person;
// Его задача — напечатать объект Person в консоль,
// но только с теми полями, которые разрешены "маской" (FieldMask).
//
// Метод print(Person p, FieldMask mask):
// - создаёт строку с фигурными скобками { ... }
// - проверяет у маски, какие поля разрешено показывать (showId, showName и т.д.)
// - если флаг = true, то добавляет соответствующее поле из Person в строку
// - в конце выводит получившийся текст через System.out.println()

public class MaskPrinter {
    public static void print(Person p, FieldMask mask) {
        StringBuilder sb = new StringBuilder("{ ");
        if (mask.showId()) sb.append("id=").append(p.getId()).append(" ");
        if (mask.showName()) sb.append("name=").append(p.getName()).append(" ");
        if (mask.showSalary()) sb.append("salary=").append(p.getSalary()).append(" ");
        if (mask.showRole()) sb.append("role=").append(p.getRole()).append(" ");
        if (mask.showActive()) sb.append("active=").append(p.isActive()).append(" ");
        sb.append("}");
        System.out.println(sb);
    }
}
