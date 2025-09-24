import asyncio
import copy
import logging
import datetime
import os
import argparse

from cover_agent.ai_caller import AICaller
from cover_agent.cover_agent_ import CoverAgent
from cover_agent.lsp_logic.ContextHelper import ContextHelper
from cover_agent.settings.config_loader import get_settings
from cover_agent.settings.config_schema import CoverAgentConfig
from cover_agent.utils import find_test_files, parse_args_full_repo
from cover_agent.testable_file_finder import TestableFileFinder
from cover_agent.test_file_generator import TestFileGenerator
from cover_agent.build_tool_adapter import MavenAdapter


async def process_test_file(test_file: str, adapter: MavenAdapter, context_helper: ContextHelper, ai_caller: AICaller, args: argparse.Namespace, logger, task_id: int):
    """Process a single test file asynchronously."""
    try:
        print(f"\n[Task {task_id}] Processing test file: {test_file} at {datetime.datetime.now()}")
        # Find the context files for the test file
        context_files = await context_helper.find_test_file_context(test_file)
        print("[Task {}] Context files for test file '{}':\n{}".format(task_id, test_file, "".join(f"{f}\n" for f in context_files)))

        # Analyze the test file against the context files
        print(f"\n[Task {task_id}] Analyzing test file against context files...")
        source_file, context_files_include = context_files[0], context_files[1:]
        # source_file, context_files_include = await context_helper.analyze_context(
        #     test_file, context_files, ai_caller
        # )

        if source_file:
            try:
                # Run the CoverAgent for the test file
                args_copy = copy.deepcopy(args)
                args_copy.source_file_path = source_file
                args_copy.test_command_dir = args.project_root
                args_copy.test_file_path = test_file
                args_copy.included_files = context_files_include
                # args_copy.test_command = adapter.adapt_test_command(test_file)
                args_copy.code_coverage_report_path = adapter.get_coverage_path(test_file)

                config = CoverAgentConfig.from_cli_args_with_defaults(args_copy)
                agent = CoverAgent(config=config, built_tool_adapter=adapter)
                agent.run()
                return (test_file, True, None)
            except Exception as e:
                print(f"[Task {task_id}] Error running CoverAgent for test file '{test_file}': {e}")
                return (test_file, False, f"CoverAgent error: {str(e)}")
        else:
            return (test_file, False, "No source file found")
    except Exception as e:
        print(f"[Task {task_id}] Error processing test file '{test_file}': {e}")
        return (test_file, False, f"Processing error: {str(e)}")


async def generate_test_file(source_file, test_file_path, test_content, context_helper, task_id):
    """Generate an empty test file for a source file using LSP for context."""
    try:
        print(f"\n[Task {task_id}] Generating test file for: {source_file}")
        
        # Create test file directory if it doesn't exist
        test_dir = os.path.dirname(test_file_path)
        os.makedirs(test_dir, exist_ok=True)
        
        # Write the test file
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        print(f"[Task {task_id}] Created test file: {test_file_path}")
        return (source_file, test_file_path, True, None)
        
    except Exception as e:
        print(f"[Task {task_id}] Error generating test file for '{source_file}': {e}")
        return (source_file, test_file_path, False, str(e))


async def run():
    # Setup logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    settings = get_settings().get("default")
    args = parse_args_full_repo(settings)

    if args.project_language == "python" or args.project_language == "java":
        context_helper = ContextHelper(args)
    else:
        raise NotImplementedError("Unsupported language: {}".format(args.project_language))

    # Find files which need unit tests to be generated
    testable_finder = TestableFileFinder(args.project_root, args.project_language)
    all_testable_files = testable_finder.find_testable_files()
    
    # scan the project directory for test files
    test_files = find_test_files(args)

    print("\n============\nTest files to be extended:\n" + "".join(f"{f}\n============\n" for f in test_files))

    # Generate test files for all testable files (exclude files that already have existed test files)
    test_generator = TestFileGenerator(args.project_root, args.project_language)
    files_needing_tests = []
    
    for source_file in all_testable_files:
        existing_test = test_generator.find_existing_test_file(source_file, test_files)
        if not existing_test:
            test_file_path, test_content = test_generator.generate_test_file(source_file)
            if test_file_path is None:
                continue
            files_needing_tests.append((source_file, test_file_path, test_content))
    
    print(f"\n============\nFiles needing test generation: {len(files_needing_tests)}")
    if files_needing_tests:
        print("First 10 files without tests:" if len(files_needing_tests) > 10 else "Files without tests:")
        for source_file, test_path, _ in files_needing_tests[:10]:
            print(f"  - {source_file}")
            print(f"    -> {test_path}")
        if len(files_needing_tests) > 10:
            print(f"  ... and {len(files_needing_tests) - 10} more files")

    # start the language server
    async with context_helper.start_server():
        print("LSP server initialized.")

        generate_log_files = not args.suppress_log_files
        api_base = getattr(args, "api_base", "")
        ai_caller = AICaller(model=args.model, api_base=api_base, generate_log_files=generate_log_files)

        # First, generate empty test files for files without tests
        if files_needing_tests:
            print(f"\n============\nGenerating {len(files_needing_tests)} empty test files...")
            generation_tasks = [
                generate_test_file(source_file, test_file_path, test_content, context_helper, task_id)
                for task_id, (source_file, test_file_path, test_content) in enumerate(files_needing_tests, 1)
            ]
            generation_results = await asyncio.gather(*generation_tasks)
            
            # Add newly created test files to the test_files list
            for source_file, test_file_path, success, error in generation_results:
                if success and test_file_path not in test_files:
                    test_files.append(test_file_path)
            
            # Print generation summary
            successful_generations = [r for r in generation_results if r[2]]
            failed_generations = [r for r in generation_results if not r[2]]
            
            print(f"\nTest file generation complete:")
            print(f"✅ Successfully created: {len(successful_generations)} test files")
            print(f"❌ Failed: {len(failed_generations)} test files")

        adapter = MavenAdapter(args.test_command ,args.project_root)

        try:
            if adapter: 
                adapter.prepare_environment()
            # Process all test files concurrently
            tasks = [process_test_file(test_file, adapter, context_helper, ai_caller, args, logger, task_id) 
                     for task_id, test_file in enumerate(test_files, 1)]
            results = await asyncio.gather(*tasks)
        finally:
            if adapter:
                adapter.cleanup_environment()
        
        # Generate statistics
        print("\n" + "="*80)
        print("EXECUTION SUMMARY")
        print("="*80)
        
        successful_files = [(f, r, e) for f, r, e in results if r]
        failed_files = [(f, r, e) for f, r, e in results if not r]
        
        print(f"\nTotal test files processed: {len(results)}")
        print(f"✅ Successful: {len(successful_files)}")
        print(f"❌ Failed: {len(failed_files)}")
        
        if successful_files:
            print("\n✅ Successfully processed files:")
            for file, _, _ in successful_files:
                print(f"   - {file}")
        
        if failed_files:
            print("\n❌ Failed files:")
            for file, _, error in failed_files:
                print(f"   - {file}")
                if error:
                    print(f"     Error: {error}")
        
        print("\n" + "="*80)


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()

