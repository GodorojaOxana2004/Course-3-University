package org.example.mask;

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
