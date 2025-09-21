package org.example.mask;

import org.example.model.Person;

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
