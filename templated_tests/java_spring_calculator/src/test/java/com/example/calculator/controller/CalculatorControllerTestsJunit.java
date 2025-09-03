import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

@DisplayName("Test suite for the Calculator class")
class CalculatorControllerTestsJunit {

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

    @Test
    void testMultiplication() {
        Calculator calculator = new Calculator();
        assertEquals(10, calculator.multiply(2, 5));
    }

    @Test
    void testIsPositive() {
        Calculator calculator = new Calculator();
        assertTrue(calculator.isPositive(10));
    }
}
