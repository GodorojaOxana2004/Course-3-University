package org.example;

import org.example.mask.FieldMask;
import org.example.mask.MaskUtils;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

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
