package com.example.calculator.service;

import org.springframework.stereotype.Service;

/**
 * Helper class for common mathematical operations.
 * This class is typically used by controllers or other services.
 */
@Service
public class CalculatorHelper {
    public double power(double base, double exponent) {
        return Math.pow(base, exponent);
    }   
}
