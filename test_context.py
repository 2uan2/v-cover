# from cover_agent.lsp_logic.utils.utils_context import find_test_file_context
from argparse import Namespace
from cover_agent.lsp_logic.ContextHelper import ContextHelper
from cover_agent.lsp_logic.utils.utils import remove_duplicate_included_files
import asyncio

file = "./templated_tests/java_spring_calculator/src/main/java/com/example/calculator/controller/CalculatorController.java"
# file = "./src/main/java/org/example/schemaextractor/controllers/ReportEditorController.java"
# file = "./templated_tests/python_fastapi/test_app.py"

async def run():
    args = Namespace()
    args.project_language = "python" if file.endswith("py") else "java"
    # args.project_root = "/home/quan/viettel/metadata-extractor-be/"
    args.project_root = "/home/quan/qodo/q-cover/"
    context_helper = ContextHelper(args)
    async with context_helper.start_server():
        # context_files = await context_helper.find_test_file_context(file)
        # print("The return value from context_helper.find_test_file_context: ", context_files)
        all_context_files = await context_helper.find_all_context(file)
        deduped = remove_duplicate_included_files(all_context_files)
        
        # context_files = [context_file for context_file, _, _, _ in all_context_files]
        print("all_context_files are: ", deduped)



def main():
    asyncio.run(run())

if __name__ == "__main__":
    main()
