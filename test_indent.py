from cover_agent.lsp_logic.utils.utils_indent import *
from cover_agent.lsp_logic.utils.utils_insert_line import *
from argparse import Namespace

test_file = "./templated_tests/java_spring_calculator/src/test/java/com/example/calculator/controller/CalculatorControllerTest.java"

def main():
    args = Namespace()
    args.project_language = "java"

    # result = find_indentation_amount(args, ".", test_file)
    result = find_framework(args, ".", test_file)

    print(result)

if __name__ == "__main__":
    main()

