package com.example.calculator.model;

/**
 * A simple data class to represent the result of a calculation.
 * This is a Plain Old Java Object (POJO) often used for data transfer.
 */
public class CalculationResult {
    private final double operand1;
    private final double operand2;
    private final double result;

    public CalculationResult(double operand1, double operand2, double result) {
        this.operand1 = operand1;
        this.operand2 = operand2;
        this.result = result;
    }

    public double getOperand1() {
        return operand1;
    }

    public double getOperand2() {
        return operand2;
    }

    public double getResult() {
        return result;
    }
}
