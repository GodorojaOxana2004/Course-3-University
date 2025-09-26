package com.example._1_lab;

import com.example._1_lab.mask.FieldMask;
import com.example._1_lab.mask.MaskUtils;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
// тесты:
// 1) testCombineOr()
//    - проверяяет работу метода combine (логическое ИЛИ)
//    - создаются две маски m1 и m2
//    - итоговая маска должна показывать поля, если они включены хотя бы в одной из масок
//    - через assertTrue / assertFalse проверяются результаты
// 2) testCombineAnd()
//    - проверяет работу метода combineAnd (логическое И)
//    - итоговая маска должна показывать поле только если оно включено в обеих масках
// 3) testInvert()
//    - проверяет работу метода invert (инверсия)
//    - все true должны стать false, а false — true

public class MaskUtilsTest {
    @Test
    void testCombineOr() {
        FieldMask m1 = new FieldMask(true, false, false, true, false);
        FieldMask m2 = new FieldMask(false, true, false, false, true);
        FieldMask result = MaskUtils.combine(m1, m2);
        assertTrue(result.showId());
        assertTrue(result.showName());
        assertFalse(result.showSalary());
        assertTrue(result.showRole());
        assertTrue(result.showActive());
    }

    @Test
    void testCombineAnd() {
        FieldMask m1 = new FieldMask(true, true, false, true, false);
        FieldMask m2 = new FieldMask(true, false, false, true, true);
        FieldMask result = MaskUtils.combineAnd(m1, m2);
        assertTrue(result.showId());
        assertFalse(result.showName());
        assertFalse(result.showSalary());
        assertTrue(result.showRole());
        assertFalse(result.showActive());
    }

    @Test
    void testInvert() {
        FieldMask m = new FieldMask(true, false, true, false, true);
        FieldMask inverted = MaskUtils.invert(m);
        assertFalse(inverted.showId());
        assertTrue(inverted.showName());
        assertFalse(inverted.showSalary());
        assertTrue(inverted.showRole());
        assertFalse(inverted.showActive());
    }
}
