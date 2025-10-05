from cover_agent.lsp_logic.file_map.file_map import FileMap
from argparse import Namespace

# target_file = "./templated_tests/java_spring_calculator/src/test/java/com/example/calculator/controller/CalculatorControllerTest.java"
# target_file = "./templated_tests/python_fastapi/test_app.py"
target_file = "./templated_tests/java_spring_calculator/src/main/java/com/example/calculator/controller/CalculatorController.java"
# target_file = "./templated_tests/python_fastapi/helper.py"
args = Namespace()
args.project_language = "python" if target_file.endswith("py") else "java"
args.project_root = "/home/quan/qodo/q-cover/"

def main():
    fname_summary = FileMap(
        target_file,
        parent_context=False,
        child_context=False,
        header_max=0,
        project_base_path=args.project_root,
    )
    # results = fname_summary.get_query_sub_results()
    # print(results)
    print(fname_summary.get_imports())









if __name__ == '__main__':
    main()
