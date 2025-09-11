package com.example.calculator.controller;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

class CalculatorControllerTest {

    private CalculatorController calculatorController;

    @BeforeEach
    void setUp() {
        calculatorController = new CalculatorController();
    }

    @Test
    void testAddition() {
        assertEquals(2, calculatorController.add(1, 1), "1 + 1 should equal 2");
        assertEquals(10, calculatorController.add(4, 6), "4 + 6 should equal 10");
        assertEquals(0, calculatorController.add(-5, 5), "-5 + 5 should equal 0");
    }

    @Test
    @DisplayName("tests subtraction with positive numbers")
    void testSubtraction() {
        assertEquals(0, calculatorController.subtract(5, 5), "5 - 5 should equal 0");
        assertEquals(3, calculatorController.subtract(7, 4), "7 - 4 should equal 3");
    }

    @Test
    @DisplayName("tests multiplication with positive and negative numbers")
    void testMultiplication() {
        assertEquals(12, calculatorController.multiply(3, 4), "3 * 4 should equal 12");
        assertEquals(-15, calculatorController.multiply(5, -3), "5 * -3 should equal -15");
        assertEquals(0, calculatorController.multiply(100, 0), "Any number multiplied by 0 should equal 0");
    }

    @Nested
    @DisplayName("Division Tests")
    class DivisionTests {

        @Test
        @DisplayName("dividing positive numbers")
        void testDivisionPositive() {
            assertEquals(2.0, calculatorController.divide(10, 5), "10 / 5 should equal 2.0");
        }

        @Test
        @DisplayName("dividing negative numbers")
        void testDivisionNegative() {
            assertEquals(-3.0, calculatorController.divide(9, -3), "9 / -3 should equal -3.0");
        }

        @Test
        @DisplayName("should throw ArithmeticException for division by zero")
        void testDivisionByZero() {
            assertThrows(ArithmeticException.class, () -> calculatorController.divide(10, 0));
        }
    }
}
