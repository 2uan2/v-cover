from cover_agent.lsp_logic.file_map.file_map import FileMap

target_file = "./templated_tests/java_spring_calculator/src/test/java/com/example/calculator/controller/CalculatorControllerTest.java"

def main():
    fname_summary = FileMap(
        target_file,
        parent_context=False,
        child_context=False,
        header_max=0,
        project_base_path=".",
    )
    file_imports = fname_summary.get_unit_tests()
    names = [ file_import['name'] for file_import in file_imports ]
    # print(names)
    print(file_imports)

if __name__ == "__main__":
    main()
