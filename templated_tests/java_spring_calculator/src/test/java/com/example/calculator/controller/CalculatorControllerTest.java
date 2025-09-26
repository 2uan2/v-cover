package com.example.calculator.controller;

import com.example.calculator.controller.CalculatorController;
import com.example.calculator.service.CalculatorService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;

@WebMvcTest(CalculatorController.class)
public class CalculatorControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private CalculatorService calculatorService;

    @BeforeEach
    public void setUp() {
        when(calculatorService.add(2, 3)).thenReturn(5.0);
        when(calculatorService.subtract(5, 4)).thenReturn(1.0);
        when(calculatorService.multiply(2, 3)).thenReturn(6.0);
        when(calculatorService.divide(6, 3)).thenReturn(2.0);
    }

    @Test
    public void testAdd() throws Exception {
        mockMvc.perform(get("/add?a=2&b=3"))
                .andExpect(status().isOk())
                .andExpect(content().string("5.0"));
    }

    @Test
    public void testSubtract() throws Exception {
        mockMvc.perform(get("/subtract?a=5&b=4"))
                .andExpect(status().isOk())
                .andExpect(content().string("1.0"));
    }

    @Test
    public void testServiceDivideByZero() {
        CalculatorService service = new CalculatorService();
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            service.divide(10, 0);
        });
        assertEquals("Cannot divide by zero", exception.getMessage());
    }


    @Test
    public void testServiceDivideHappyPath() {
        CalculatorService service = new CalculatorService();
        assertEquals(2.0, service.divide(10, 5));
        assertEquals(0.0, service.divide(0, 5));
    }


    @Test
    public void testServiceBasicOperations() {
        CalculatorService service = new CalculatorService();
        assertEquals(8.0, service.add(5, 3));
        assertEquals(2.0, service.subtract(5, 3));
        assertEquals(15.0, service.multiply(5, 3));
    }


}
