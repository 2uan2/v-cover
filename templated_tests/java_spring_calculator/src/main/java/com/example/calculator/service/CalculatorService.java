package com.example.calculator.service;

import org.springframework.stereotype.Service;

import com.example.calculator.controller.CalculatorController;

@Service
public class CalculatorService {
    private CalculatorController calculatorController;

    public double add(double a, double b) {
        calculatorController.add(1, 2);
        return a + b;
    }

    public double subtract(double a, double b) {
        return a - b;
    }

    public double multiply(double a, double b) {
        return a * b;
    }

    public double divide(double a, double b) {
        if (b == 0) {
            throw new IllegalArgumentException("Cannot divide by zero");
        }
        return a / b;
    }
}
