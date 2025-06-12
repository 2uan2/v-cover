import asyncio
import copy
import logging
import datetime

from cover_agent.ai_caller import AICaller
from cover_agent.cover_agent_ import CoverAgent
from cover_agent.lsp_logic.ContextHelper import ContextHelper
from cover_agent.settings.config_loader import get_settings
from cover_agent.settings.config_schema import CoverAgentConfig
from cover_agent.utils import find_test_files, parse_args_full_repo


async def process_test_file(test_file, context_helper, ai_caller, args, logger, task_id):
    """Process a single test file asynchronously."""
    try:
        print(f"\n[Task {task_id}] Processing test file: {test_file} at {datetime.datetime.now()}")
        # Find the context files for the test file
        context_files = await context_helper.find_test_file_context(test_file)
        print("[Task {}] Context files for test file '{}':\n{}".format(task_id, test_file, "".join(f"{f}\n" for f in context_files)))

        # Analyze the test file against the context files
        print(f"\n[Task {task_id}] Analyzing test file against context files...")
        source_file, context_files_include = await context_helper.analyze_context(
            test_file, context_files, ai_caller
        )

        if source_file:
            try:
                # Run the CoverAgent for the test file
                args_copy = copy.deepcopy(args)
                args_copy.source_file_path = source_file
                args_copy.test_command_dir = args.project_root
                args_copy.test_file_path = test_file
                args_copy.included_files = context_files_include

                config = CoverAgentConfig.from_cli_args_with_defaults(args_copy)
                agent = CoverAgent(config)
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

    # scan the project directory for test files
    test_files = find_test_files(args)
    print("============\nTest files to be extended:\n" + "".join(f"{f}\n============\n" for f in test_files))

    # start the language server
    async with context_helper.start_server():
        print("LSP server initialized.")

        generate_log_files = not args.suppress_log_files
        api_base = getattr(args, "api_base", "")
        ai_caller = AICaller(model=args.model, api_base=api_base, generate_log_files=generate_log_files)

        # Process all test files concurrently
        tasks = [process_test_file(test_file, context_helper, ai_caller, args, logger, task_id) 
                 for task_id, test_file in enumerate(test_files, 1)]
        results = await asyncio.gather(*tasks)
        
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

