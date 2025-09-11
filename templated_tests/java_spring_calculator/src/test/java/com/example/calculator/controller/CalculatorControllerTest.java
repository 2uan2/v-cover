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
	@Mock
	private CalculatorHelper calculatorHelper;

	@InjectMocks
	private CalculatorController calculatorController;

	@BeforeEach
	void setUp() {
		MockitoAnnotations.openMocks(this);
	}

	@Test
	void testAddNumbersSuccessfully() {
		when(calculatorController.add(10.0, 5.0)).thenReturn(15.0);

		// Call the method on the class under test.
		double result = calculatorController.add(10.0, 5.0);

		// Assert that the returned value is what we expect.
		assertEquals(15.0, result);
	}

	@Test
	void testCreateCalculationResult() {
		// This test shows a dependency on the CalculationResult model class.
		// We're creating an instance of the class directly.
		CalculationResult result = new CalculationResult(10, 5, 50.0);

		// Verify the values are set correctly.
		assertEquals(10, result.getOperand1());
		assertEquals(5, result.getOperand2());
		assertEquals(50.0, result.getResult());
	}
}
