import org.testng.annotations.Test;
import static org.testng.Assert.assertEquals;

public class CalculatorControllerTestsNG {

    @Test(description = "Tests basic addition functionality")
    public void testAddition() {
        int sum = 2 + 3;
        assertEquals(5, sum);
    }

    @Test
    public void testSubtraction() {
        int difference = 10 - 5;
        assertEquals(5, difference);
    }

    @Test(groups = "smoke")
    public void testMultiplication() {
        int product = 4 * 5;
        assertEquals(20, product);
    }
}
