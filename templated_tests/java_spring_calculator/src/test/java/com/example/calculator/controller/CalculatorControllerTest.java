package com.example.calculator.controller;

import com.example.calculator.model.CalculationResult;
import com.example.calculator.service.CalculatorHelper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.when;

class CalculatorControllerTest {
    @InjectMocks
    private CalculatorController calculatorController;

    @Mock
    private CalculatorHelper calculatorHelper;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testAddNumbersSuccessfully() {
        double result = calculatorController.add(10.0, 5.0);

        assertEquals(15.0, result);
    }

    @Test
    void testPowerOperation() {
        double base = 2.0;
        double exponent = 3.0;
        double expectedResult = 8.0;

        when(calculatorHelper.power(base, exponent)).thenReturn(expectedResult);

        double actualResult = calculatorController.power(base, exponent);

        assertEquals(expectedResult, actualResult, "The power calculation result should match the stubbed value.");
    }

    @Test
    void testCalculationResultGetters() {
        // Arrange: Define the input values and the expected result
        double operand1 = 10.0;
        double operand2 = 5.0;
        double result = 15.0;

        // Act: Create an instance of the CalculationResult class
        CalculationResult calculationResult = new CalculationResult(operand1, operand2, result);

        // Assert: Verify that the getter methods return the expected values
        assertEquals(operand1, calculationResult.getOperand1(),
                "The first operand should match the value set in the constructor.");
        assertEquals(operand2, calculationResult.getOperand2(),
                "The second operand should match the value set in the constructor.");
        assertEquals(result, calculationResult.getResult(),
                "The result should match the value set in the constructor.");
    }
}
