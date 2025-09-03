package com.example.calculator.controller;

import static org.junit.jupiter.api.Assertions.*;
class CalculatorControllerTest {
    @Test
    void testAddition() {
        Calculator calculator = new Calculator();
        assertEquals(2, calculator.add(1, 1), "1 + 1 should equal 2");
    }

    @Test
    @DisplayName("Tests subtraction with positive numbers")
    void testSubtraction() {
        Calculator calculator = new Calculator();
        assertEquals(0, calculator.subtract(5, 5), "5 - 5 should equal 0");
    }
}
