# from cover_agent.lsp_logic.utils.utils_context import find_test_file_context
from argparse import Namespace
from cover_agent.utils import get_included_files_content_in_ranges
import asyncio

file = "./templated_tests/java_spring_calculator/src/test/java/com/example/calculator/controller/CalculatorControllerTest.java"
# file = "./templated_tests/python_fastapi/test_app.py"
included_files = [('/home/quan/qodo/q-cover/templated_tests/java_spring_calculator/src/main/java/com/example/calculator/model/CalculationResult.java', 'getOperand1', 17, 19), ('/home/quan/qodo/q-cover/templated_tests/java_spring_calculator/src/main/java/com/example/calculator/controller/CalculatorController.java', 'add', 22, 25), ('/home/quan/qodo/q-cover/templated_tests/java_spring_calculator/src/main/java/com/example/calculator/service/CalculatorService.java', 'add', 10, 13), ('/home/quan/qodo/q-cover/templated_tests/java_spring_calculator/src/main/java/com/example/calculator/model/CalculationResult.java', 'getOperand2', 21, 23), ('/home/quan/qodo/q-cover/templated_tests/java_spring_calculator/src/main/java/com/example/calculator/service/CalculatorHelper.java', 'power', 10, 12), ('/home/quan/qodo/q-cover/templated_tests/java_spring_calculator/src/main/java/com/example/calculator/model/CalculationResult.java', 'CalculationResult', 6, 28), ('/home/quan/qodo/q-cover/templated_tests/java_spring_calculator/src/main/java/com/example/calculator/model/CalculationResult.java', 'getResult', 25, 27)]

async def run():
    content = get_included_files_content_in_ranges(included_files, ".")
    print(content)










def main():
    asyncio.run(run())

if __name__ == "__main__":
    main()

