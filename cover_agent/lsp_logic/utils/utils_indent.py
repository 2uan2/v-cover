import os
from collections import Counter

from cover_agent.lsp_logic.file_map.file_map import FileMap


def find_indentation_amount(args, project_root, test_file) -> int:
    try:
        target_file = test_file
        rel_file = os.path.relpath(target_file, project_root)

        fname_summary = FileMap(
            target_file,
            parent_context=False,
            child_context=False,
            header_max=0,
            project_base_path=project_root,
        )
        # query_results, captures =
        results = fname_summary.get_unit_tests()

        number_of_tests = len(results)
        indentation_counter = Counter([result["column"] for result in results])
        test_headers_indentation = indentation_counter.most_common(1)[0][0]
        # print(f"test_headers_indentation = {test_headers_indentation}")
        # print(f"number_of_tests = {number_of_tests}")
        return test_headers_indentation

        # print("results from treesitter: ", results)
    except Exception as e:
        print(
            f"Error while getting indentation, falling back to using LLM maybe??: {e}"
        )
        # TODO: fallback to LLM here

    return 4  # defaults


def find_framework(args, project_root, test_file) -> str:
    try:
        target_file = test_file
        language = args.project_language
        rel_file = os.path.relpath(target_file, project_root)

        fname_summary = FileMap(
            target_file,
            parent_context=False,
            child_context=False,
            header_max=0,
            project_base_path=project_root,
        )
        imports = fname_summary.get_imports()

    except Exception as e:
        print(f"Error while getting framework, falling back to using LLM maybe??: {e}")
        # TODO: fallback to LLM here

    return "Unknown"


# ```yaml
# language: {{ language }}
# testing_framework: ...
# number_of_tests: ...
# test_headers_indentation: ...
# ```
