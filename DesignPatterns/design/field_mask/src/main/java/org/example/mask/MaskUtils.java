package org.example.mask;
// Методы:
// 1) combine(m1, m2) — объединяет две маски по принципу "ИЛИ" (||)
//    Поле будет видно, если хотя бы в одной маске оно разрешено
//    Пример: m1 показывает id, m2 показывает name → итоговая маска покажет и id, и name
// 2) combineAnd(m1, m2) — объединяет маски по принципу "И" (&&)
//    Поле будет видно только если оно включено в обеих масках
//    Пример: если только одна из масок разрешает salary, итоговая не покажет salary
// 3) invert(m) — инвертирует маску
//    Поля, которые были видны (true), становятся скрытыми (false), и наоборот

public class MaskUtils {
    public static FieldMask combine(FieldMask m1, FieldMask m2) {
        return new FieldMask(
            m1.showId() || m2.showId(),
            m1.showName() || m2.showName(),
            m1.showSalary() || m2.showSalary(),
            m1.showRole() || m2.showRole(),
            m1.showActive() || m2.showActive()
        );
    }

    public static FieldMask combineAnd(FieldMask m1, FieldMask m2) {
        return new FieldMask(
            m1.showId() && m2.showId(),
            m1.showName() && m2.showName(),
            m1.showSalary() && m2.showSalary(),
            m1.showRole() && m2.showRole(),
            m1.showActive() && m2.showActive()
        );
    }

    public static FieldMask invert(FieldMask m) {
        return new FieldMask(
            !m.showId(),
            !m.showName(),
            !m.showSalary(),
            !m.showRole(),
            !m.showActive()
        );
    }
}
