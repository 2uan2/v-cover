from fastmcp import FastMCP
import asyncio
from pathlib import Path
import sys

mcp = FastMCP("vCover")

test = {"counter": 0}
jobs = {}

async def run_and_update_job(job_id, command_list, cwd):
    proc = await asyncio.create_subprocess_exec(
        *command_list,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=cwd
    )
    jobs[job_id]['process'] = proc
    stdout, stderr = await proc.communicate()
    jobs[job_id]['status'] = 'completed' if proc.returncode == 0 else 'failed'
    jobs[job_id]['stdout'] = stdout.decode(errors='ignore')
    jobs[job_id]['stderr'] = stderr.decode(errors='ignore')
    jobs[job_id]['returncode'] = proc.returncode
    del jobs[job_id]['process']

async def run_tool_and_update_job(job_id, seconds):
    try:
        # Execute the tool function (e.g., delayed_message)
        await asyncio.sleep(seconds)
        result = f"[Run {job_id}] Slept for {seconds/3600} hours and now returning this message lol."
        jobs[job_id]['status'] = 'completed'
        jobs[job_id]['result'] = result
    except Exception as e:
        jobs[job_id]['status'] = 'failed'
        jobs[job_id]['error'] = str(e)

@mcp.tool()
async def delayed_message(seconds: int = 5) -> dict:
    """
    Sleeps for a given number of seconds before returning a message.

    Args:
        seconds (int): How long to sleep (default 5 seconds)
    Returns:
        dict: A message confirming the delay
    """
    # test['counter'] += 1
    # await asyncio.sleep(seconds)
    #
    # return f"[Run {test['counter']}] Slept for {seconds/3600} hours and now returning this message lol."
    job_id = str(len(jobs) + 1)
    jobs[job_id] = {
        "status": "running",
        "tool": "delayed_message",
        "params": {"seconds": seconds},
        "result": None
    }

    # Start the delayed_message tool in the background
    asyncio.create_task(run_tool_and_update_job(job_id, seconds))

    return {"job_id": job_id}

@mcp.tool()
async def improve_coverage_for_entire_repository(
    project_language: str,
    code_coverage_report_path: str,
    test_command: str,
    project_root: str = ".",
    cwd: str = ".",
    max_test_files_allowed_to_analyze: int = None,
    look_for_oldest_unchanged_test_file: bool = None,
    test_folder: str = None,
    test_file: str = None,
    run_each_test_seperately: bool = None,
    test_command_dir: str = None,
    coverage_type: str = None,
    report_filepath: str = None,
    max_iterations: int = None,
    max_run_time_sec: int = None,
    additional_instructions: str = None,
    model: str = None,
    api_base: str = None,
    strict_coverage: bool = None,
    run_tests_multiple_times: int = None,
    log_db_path: str = None,
    test_file_output_path: str = None,
    desired_coverage: int = None,
    branch: str = None,
    record_mode: bool = None,
    suppress_log_files: bool = None,
    use_report_coverage_feature_flag: bool = None,
    diff_coverage: bool = None
):
    """
    Tool: improve_coverage_for_entire_repository
    Description:
        **Primary Function: Automated Test Generation and File Modification for an Entire Repository.**
        This tool scans an *entire repository* to identify testable source files and their
        corresponding test files. It then automatically generates new unit tests to increase
        overall code coverage across the project. The generated tests are **directly appended
        to the respective test files on the file system.**

        **When to Use This Tool:**
        Use this tool when your goal is to improve the overall test coverage of an entire
        codebase, rather than focusing on a single file. This is suitable for initial
        coverage efforts or for maintaining a high level of test coverage across a project.

        **Do NOT generate test code yourself.** Provide the necessary project details and commands,
        and this tool will handle the entire test generation, validation, and file modification process
        across multiple files.

    Workflow:
    1. You provide the absolute path to the project's root directory (e.g., `/path/to/my_project`).
    2. You specify the primary programming language of the project (e.g., "python", "java").
    3. You provide the command to run the existing tests and generate a coverage report.
    4. The tool scans the repository to find all relevant source and test files.
    5. It intelligently generates new tests for uncovered code and **modifies the test files in-place**
       by appending the new, validated tests.
    6. It re-runs tests to validate that overall coverage has increased.

    Parameters:
    -----------
    --- Required ---

        project_language (string):
        The primary programming language of the project (e.g., "python", "java", "typescript").
        This is crucial for the tool to correctly identify and analyze files.

        code_coverage_report_path (string):
        The absolute path to the code coverage report file (e.g., `/path/to/my_project/coverage.xml`).
        The tool uses this report to identify untested code lines across the repository.

        test_command (string):
        The shell command required to run the entire test suite and generate the coverage report.
        Example: `"pytest --cov=/app --cov-report=xml:/app/coverage.xml"`

    --- Optional ---

        project_root (string):
        The absolute path to the root of the repository (e.g., `/path/to/my_project`)
        that you want to scan and improve test coverage for. Read about the cwd below aswell. Should be '.' in most cases.

        cwd (string):
        The absolute path to the current working directory where the `cover-agent` tool itself
        should be executed. 
        The `cwd` is used in the subprocess module as the cwd to execute the command. This should be used instead of the project_root argument, for example, use cwd=templated_tests/java_spring_calculator and project_root=. instead of project_root=templated_tests/java_spring_calculator. 
        DO NOT make the two similar, like cwd=path/to/proj and project_root=path/to/proj. Defaults to the directory where the tool was launched.

        max_test_files_allowed_to_analyze (integer):
        The maximum number of test files the tool will analyze and attempt to improve coverage for.
        This can be used to limit the scope of a run.

        look_for_oldest_unchanged_test_file (boolean):
        If true, the tool will prioritize analyzing the oldest test files that have not been
        modified recently, focusing on areas that might have been neglected.

        test_folder (string):
        A relative path (from `project_root`) to a specific folder containing tests to analyze.
        If provided, the tool will only consider test files within this folder.

        test_file (string):
        A relative path (from `project_root`) to a specific test file to extend.
        If provided, the tool will focus on improving this single test file within the repository.

        run_each_test_seperately (boolean):
        If true, each generated test will be run in a separate process during validation.

        test_command_dir (string):
        The absolute path to the directory where the test command should be executed.
        Defaults to the project root.

        coverage_type (string):
        The type of coverage report being used (e.g., "jacoco", "lcov", "cobertura").
        Defaults to the value in the configuration file.

        report_filepath (string):
        The absolute path to the output report file generated by the tool.

        desired_coverage (integer):
        The target overall coverage percentage (0-100) for the repository. The tool will stop
        generating tests once this coverage level is achieved or exceeded. Defaults to the
        value in the configuration file.

        max_iterations (integer):
        The maximum number of attempts the tool will make to generate new tests across the repository.
        Defaults to the value in the configuration file.

        max_run_time_sec (integer):
        The maximum time in seconds allowed for the test command to run during each validation step.

        additional_instructions (string):
        Any specific instructions or context you wish to provide to the LLM when it generates tests.
        Example: "Ensure new tests integrate well with existing Maven Surefire configurations."

        model (string):
        The name of the LLM model to use for generating tests. Defaults to the
        value in the configuration file.

        api_base (string):
        The base URL for the LLM API (e.g., for Ollama or Hugging Face).

        strict_coverage (boolean):
        If true, the tool will exit with a non-zero status code if the desired
        coverage is not achieved.

        run_tests_multiple_times (integer):
        The number of times to run each newly generated test to ensure its stability and reliability.
        Defaults to the value in the configuration file.

        log_db_path (string):
        The absolute path to an optional SQLite database file for logging detailed test generation
        and validation results.

        branch (string):
        The Git branch to compare against when using `diff_coverage`.

        record_mode (boolean):
        If true, the LLM responses will be recorded for replay or analysis.

        suppress_log_files (boolean):
        If true, all generated log files (HTML, logs, DB files) will be suppressed.

    --- Mutually Exclusive Options ---

        use_report_coverage_feature_flag (boolean):
        If true, the tool will consider the coverage of all files in the
        coverage report when determining if a new test is useful. This means a test is
        considered good if it increases coverage for any file, not just the source file.
        Incompatible with `diff_coverage`.

        diff_coverage (boolean):
        If true, the tool will only generate tests for code changes (diff) between the
        current branch and the branch specified by `branch`. This is useful for
        focusing on new or modified code. Incompatible with `use_report_coverage_feature_flag`.

    Returns:
    --------
        tuple:
            A tuple containing the results and status of the execution. The primary result of this
            tool is the modification of test files across the repository on the file system.
            - stdout (str): The logs from the tool's execution. Review this to see progress.
            - stderr (str): Error messages for debugging.
            - returncode (int): The exit code. 0 means the tool ran successfully and files have been modified.
            - command_list (list): The list of arguments used to execute the command, useful for debugging.

    Example Usage:
    --------------
    To improve overall Python project coverage for a repository at `/home/user/my_python_app`,
    aiming for 85% coverage:
      default_api.improve_coverage_for_entire_repository(
          project_root="/home/user/my_python_app",
          project_language="python",
          code_coverage_report_path="/home/user/my_python_app/coverage.xml",
          test_command="pytest --cov=/home/user/my_python_app --cov-report=xml:/home/user/my_python_app/coverage.xml",
          desired_coverage=85,
          max_iterations=5
      )
    """
    if use_report_coverage_feature_flag and diff_coverage:
       raise ValueError("Cannot use both 'use_report_coverage_feature_flag' and 'diff_coverage' at the same time.")
    python_executable = sys.executable
    if not python_executable:
        raise RuntimeError("Could not determine the python executable path.")

    # --- Build the command as a list ---
    command_list = [
        python_executable,
        "-m",
        "cover_agent.main_full_repo",
        "--project-language", project_language,
        "--project-root", project_root,
        "--code-coverage-report-path", code_coverage_report_path,
        "--test-command", test_command,
    ]

    # --- Append optional arguments ---
    if max_test_files_allowed_to_analyze:
        command_list.extend(["--max-test-files-allowed-to-analyze", str(max_test_files_allowed_to_analyze)])
    if look_for_oldest_unchanged_test_file:
        command_list.append("--look-for-oldest-unchanged-test-file")
    if test_folder:
        command_list.extend(["--test-folder", test_folder])
    if test_file:
        command_list.extend(["--test-file", test_file])
    if run_each_test_seperately:
        command_list.append("--run-each-test-separately")
    if test_command_dir:
        command_list.extend(["--test-command-dir", test_command_dir])
    if coverage_type:
        command_list.extend(["--coverage-type", coverage_type])
    if report_filepath:
        command_list.extend(["--report-filepath", report_filepath])
    if max_iterations:
        command_list.extend(["--max-iterations", str(max_iterations)])
    if max_run_time_sec:
        command_list.extend(["--max-run-time-sec", str(max_run_time_sec)])
    if additional_instructions:
        command_list.extend(["--additional-instructions", additional_instructions])
    if model:
        command_list.extend(["--model", model])
    if api_base:
        command_list.extend(["--api-base", api_base])
    if strict_coverage:
        command_list.append("--strict-coverage")
    if run_tests_multiple_times:
        command_list.extend(["--run-tests-multiple-times", str(run_tests_multiple_times)])
    if log_db_path:
        command_list.extend(["--log-db-path", log_db_path])
    if test_file_output_path:
        command_list.extend(["--test-file-output-path", test_file_output_path])
    if desired_coverage:
        command_list.extend(["--desired-coverage", str(desired_coverage)])
    if branch:
        command_list.extend(["--branch", branch])
    if record_mode:
        command_list.append("--record-mode")
    if suppress_log_files:
        command_list.append("--suppress-log-files")
    if use_report_coverage_feature_flag:
        command_list.append("--use-report-coverage-feature-flag")
    if diff_coverage:
        command_list.append("--diff-coverage")

    # --- Use create_subprocess_exec with the argument list ---
    # proc = await asyncio.create_subprocess_exec(
    #     *command_list,
    #     stdout=asyncio.subprocess.PIPE,
    #     stderr=asyncio.subprocess.PIPE,
    #     cwd=cwd
    # )
    #     job_id: {
    #         # "job_id": job_id,
    #         "status": "running",
    #         "command_list": command_list,
    #         "stdout": "",
    #         "stderr": "",
    #         "returncode": None,
    #         "process": proc
    #     }
    # })
    # job_id = str(uuid.uuid4())
    job_id = str(len(jobs) + 1)
    # jobs.append({
    jobs[job_id] = {
        "status": "running",
        "command": command_list,
        "stdout": "",
        "stderr": "",
        "returncode": None
    }
    asyncio.create_task(run_and_update_job(job_id, command_list, cwd))

    return {"job_id": job_id}
    # stdout, stderr = await proc.communicate()
    # return job_id, proc.returncode, command_list


@mcp.tool()
async def get_job_details(job_id: str) -> dict:
    """
    Retrieves the details of a job.

    Args:
        job_id (str): The ID of the job to retrieve.
    Returns:
        dict: A dictionary containing the job's details.
    """
    job = jobs.get(job_id)
    if not job:
        return {"error": "Job not found"}

    # Don't return the process object, it's not JSON serializable
    return {k: v for k, v in job.items() if k != 'process'} 

@mcp.tool()
async def improve_coverage_for_single_file(
    source_file_path: str,
    test_file_path: str,
    code_coverage_report_path: str,
    test_command: str,
    project_root: str = None,
    test_command_dir: str = None,
    coverage_type: str = None,
    report_filepath: str = None,
    max_iterations: int = None,
    max_run_time_sec: int = None,
    additional_instructions: str = None,
    model: str = None,
    api_base: str = None,
    strict_coverage: bool = None,
    run_tests_multiple_times: int = None,
    log_db_path: str = None,
    test_file_output_path: str = None,
    desired_coverage: int = None,
    branch: str = None,
    record_mode: bool = None,
    suppress_log_files: bool = None,
    run_each_test_separately: bool = None,
    use_report_coverage_feature_flag: bool = None,
    diff_coverage: bool = None,
    included_files: list[str] = None
):
    """
    Tool: improve_coverage_for_single_file
    Description:
        **Primary Function: Automated Test Generation and File Modification for a Single File.**
        This tool automatically generates new unit tests for a *single specified source code file*
        to increase its code coverage. It analyzes the source code, identifies lines not covered
        by existing tests, and then intelligently writes new test cases. The generated tests are
        **directly appended to the specified test file on the file system.**

        **When to Use This Tool:**
        Use this tool when you have a specific source file (e.g., `my_module.py`) and its
        corresponding test file (e.g., `test_my_module.py`) and your goal is to improve
        the test coverage for that particular source file.

        **Do NOT generate test code yourself.** Provide the necessary file paths and arguments,
        and this tool will handle the entire test generation, validation, and file modification process.

    Workflow:
    1. You provide the absolute path to the source code file you want to test (e.g., `/path/to/project/src/my_module.py`).
    2. You provide the absolute path to the associated test file where new tests should be added (e.g., `/path/to/project/tests/test_my_module.py`).
    3. You provide the command to run the existing tests and generate a coverage report.
    4. The tool runs the existing tests to analyze the current code coverage.
    5. It then intelligently generates new tests and **modifies the test file in-place** by appending the new, validated tests.
    6. It re-runs tests to validate that coverage has increased.

    Parameters:
    -----------
    --- Required ---

        source_file_path (string):
        The absolute path to the single source file (e.g., `/path/to/project/src/my_module.py`)
        that you want to improve test coverage for.

        test_file_path (string):
        The absolute path to the existing test file (e.g., `/path/to/project/tests/test_my_module.py`)
        that this tool will **read from and directly append new tests to.**

        code_coverage_report_path (string):
        The absolute path to the code coverage report file (e.g., `/path/to/project/coverage.xml`).
        The tool uses this report to identify untested code lines.

        test_command (string):
        The shell command required to run the entire test suite and generate the coverage report.
        Example: `"pytest --cov=./ --cov-report=xml:/app/coverage.xml"`

    --- Optional ---

        cwd (string):
        The absolute path to the current working directory where the `cover-agent` tool itself
        should be executed. This should be the root of the project, like for Maven project, it should be the directory which contains the pom.xml and the src/ directory. Defaults to the directory where the tool was launched.

        project_root (string):
        The absolute path to the root of the project. If not provided, the current working
        directory where the tool is executed will be used as the project root.

        test_file_output_path (string):
        The absolute path to a new file where the modified test file should be written.
        If provided, the tool will **write the complete, modified test file to this new path**
        instead of overwriting the original file specified by `test_file_path`.

        test_command_dir (string):
        The absolute path to the directory where the test command should be executed.
        Defaults to the project root.

        included_files (list of strings):
        A list of absolute file paths to include in the coverage analysis. This is useful when
        the coverage report contains information about files that are not directly related to
        the source file, but whose coverage is relevant to the overall goal.
        Example: `["/path/to/project/src/helper.py", "/path/to/project/src/utils.py"]`

        coverage_type (string):
        The type of coverage report being used (e.g., "jacoco", "lcov", "cobertura").
        Defaults to the value in the configuration file.

        report_filepath (string):
        The absolute path to the output report file generated by the tool.

        desired_coverage (integer):
        The target coverage percentage (0-100). The tool will stop generating tests
        once this coverage level is achieved or exceeded. Defaults to the value in the
        configuration file.

        max_iterations (integer):
        The maximum number of attempts the tool will make to generate new tests.
        Defaults to the value in the configuration file.

        max_run_time_sec (integer):
        The maximum time in seconds allowed for the test command to run during each validation step.

        additional_instructions (string):
        Any specific instructions or context you wish to provide to the LLM when it generates tests.
        Example: "Focus on edge cases for negative numbers and zero."

        model (string):
        The name of the LLM model to use for generating tests. Defaults to the
        value in the configuration file.

        api_base (string):
        The base URL for the LLM API (e.g., for Ollama or Hugging Face).

        strict_coverage (boolean):
        If true, the tool will exit with a non-zero status code if the desired
        coverage is not achieved.

        run_tests_multiple_times (integer):
        The number of times to run each newly generated test to ensure its stability and reliability.
        Defaults to the value in the configuration file.

        log_db_path (string):
        The absolute path to an optional SQLite database file for logging detailed test generation
        and validation results.

        branch (string):
        The Git branch to compare against when using `diff_coverage`.

        run_each_test_separately (boolean):
        If true, each generated test will be run in a separate process during validation.

        record_mode (boolean):
        If true, the LLM responses will be recorded for replay or analysis.

        suppress_log_files (boolean):
        If true, all generated log files (HTML, logs, DB files) will be suppressed.

    --- Mutually Exclusive Options ---

        use_report_coverage_feature_flag (boolean):
        If true, the tool will consider the coverage of all files in the
        coverage report when determining if a new test is useful. This means a test is
        considered good if it increases coverage for any file, not just the source file.
        Incompatible with `diff_coverage`.

        diff_coverage (boolean):
        If true, the tool will only generate tests for code changes (diff) between the
        current branch and the branch specified by `branch`. This is useful for
        focusing on new or modified code. Incompatible with `use_report_coverage_feature_flag`.

    Returns:
    --------
        tuple:
            A tuple containing the results and status of the execution. The primary result of this
            tool is the modification of the test file on the file system.
            - stdout (str): The logs from the tool's execution. Review this to see progress.
            - stderr (str): Error messages for debugging.
            - returncode (int): The exit code. 0 means the tool ran successfully and the file has been modified.
            - command_list (list): The list of arguments used to execute the command, useful for debugging.

    Example Usage:
    --------------
    To improve coverage for `src/calculator.py` by adding tests to `tests/test_calculator.py`
    within a project located at `/app`, aiming for 90% coverage:
     default_api.improve_coverage_for_single_file(
         source_file_path="/app/src/calculator.py",
         test_file_path="/app/tests/test_calculator.py",
         code_coverage_report_path="/app/coverage.xml",
         test_command="pytest --cov=/app --cov-report=xml:/app/coverage.xml",
         project_root="/app",
         desired_coverage=90,
         additional_instructions="Focus on edge cases for addition and subtraction, especially with zero and negative numbers."
     )
    """
    if use_report_coverage_feature_flag and diff_coverage:
        raise ValueError("Cannot use both 'use_report_coverage_feature_flag' and 'diff_coverage' at the same time.")

    python_executable = sys.executable
    if not python_executable:
        raise RuntimeError("Could not determine the python executable path.")

    command_list = [
        python_executable,
        "-m",
        "cover_agent.main",
        "--source-file-path", source_file_path,
        "--test-file-path", test_file_path,
        "--code-coverage-report-path", code_coverage_report_path,
        "--test-command", test_command,
    ]

    if project_root:
        command_list.extend(["--project-root", project_root])
    if test_file_output_path:
        command_list.extend(["--test-file-output-path", test_file_output_path])
    if test_command_dir:
        command_list.extend(["--test-command-dir", test_command_dir])
    if included_files:
        command_list.append("--included-files")
        command_list.extend(included_files)
    if coverage_type:
        command_list.extend(["--coverage-type", coverage_type])
    if report_filepath:
        command_list.extend(["--report-filepath", report_filepath])
    if desired_coverage:
        command_list.extend(["--desired-coverage", str(desired_coverage)])
    if max_iterations:
        command_list.extend(["--max-iterations", str(max_iterations)])
    if max_run_time_sec:
        command_list.extend(["--max-run-time-sec", str(max_run_time_sec)])
    if additional_instructions:
        command_list.extend(["--additional-instructions", additional_instructions])
    if model:
        command_list.extend(["--model", model])
    if api_base:
        command_list.extend(["--api-base", api_base])
    if strict_coverage:
        command_list.append("--strict-coverage")
    if run_tests_multiple_times:
        command_list.extend(["--run-tests-multiple-times", str(run_tests_multiple_times)])
    if log_db_path:
        command_list.extend(["--log-db-path", log_db_path])
    if branch:
        command_list.extend(["--branch", branch])
    if run_each_test_separately:
        command_list.append("--run-each-test-separately")
    if record_mode:
        command_list.append("--record-mode")
    if suppress_log_files:
        command_list.append("--suppress-log-files")
    if use_report_coverage_feature_flag:
        command_list.append("--use-report-coverage-feature-flag")
    if diff_coverage:
        command_list.append("--diff-coverage")

    proc = await asyncio.create_subprocess_exec(
        *command_list,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=cwd
    )
    stdout, stderr = await proc.communicate()

    return stdout, stderr, proc.returncode, command_list
# --- Validate Mutually Exclusive Options ---
    # if use_report_coverage_feature_flag and diff_coverage:
    #     raise ValueError("Cannot use both 'use_report_coverage_feature_flag' and 'diff_coverage' at the same time.")
    #
    # command = f"""/home/quan/.cache/pypoetry/virtualenvs/cover-agent-_7Ijlvta-py3.10/bin/python3 -m cover_agent.main_full_repo \\
    #     --source-file-path "{source_file_path}" \\
    #     --test-file-path "{test_file_path}" \\
    #     --code-coverage-report-path "{code_coverage_report_path}" \\
    #     --test-command "{test_command}"
    # """
    # if project_root:
    #     command += f' \\\n    --project-root "{project_root}"'
    # if test_file_output_path:
    #     command += f' \\\n    --test-file-output-path "{test_file_output_path}"'
    # if test_command_dir:
    #     command += f' \\\n    --test-command-dir "{test_command_dir}"'
    # if included_files:
    #     files_str = " ".join(f'"{f}"' for f in included_files)
    #     command += f' \\\n    --included-files "{files_str}"'
    # if coverage_type:
    #     command += f' \\\n    --coverage-type "{coverage_type}"'
    # if report_filepath:
    #     command += f' \\\n    --report-filepath "{report_filepath}"'
    # if desired_coverage:
    #     command += f' \\\n    --desired-coverage "{desired_coverage}"'
    # if max_iterations:
    #     command += f' \\\n    --max-iterations "{max_iterations}"'
    # if max_run_time_sec:
    #     command += f' \\\n    --max-run-time-sec "{max_run_time_sec}"'
    # if additional_instructions:
    #     command += f' \\\n    --additional-instructions "{additional_instructions}"'
    # if model:
    #     command += f' \\\n    --model "{model}"'
    # if api_base:
    #     command += f' \\\n    --api-base "{api_base}"'
    # if strict_coverage:
    #     command += ' \\\n    --strict-coverage'
    # if run_tests_multiple_times:
    #     command += f' \\\n    --run-tests-multiple-times "{run_tests_multiple_times}"'
    # if log_db_path:
    #     command += f' \\\n    --log-db-path "{log_db_path}"'
    # if branch:
    #     command += f' \\\n    --branch "{branch}"'
    # if run_each_test_separately:
    #     command += ' \\\n    --run-each-test-separately'
    # if record_mode:
    #     command += ' \\\n    --record-mode'
    # if suppress_log_files:
    #     command += ' \\\n    --suppress-log-files'
    # if use_report_coverage_feature_flag:
    #     command += ' \\\n    --use-report-coverage-feature-flag'
    # if diff_coverage:
    #     command += ' \\\n    --diff-coverage'
    #
    # proc = await asyncio.create_subprocess_shell(
    #     command,
    #     stdout=asyncio.subprocess.PIPE,
    #     stderr=asyncio.subprocess.PIPE
    # )
    # stdout, stderr = await proc.communicate()
    #
    # # return stdout.decode(errors='ignore'), stderr.decode(errors='ignore'), proc.returncode
    # return stdout, stderr, proc.returncode

def main():
    # asyncio.run(improve_coverage_for_entire_repository(
    #     'java', 
    #     'target/site/jacoco/jacoco.xml', 
    #     'mvn verify -DfailIfNoTest=false',
    #     api_base="https://netmind.viettel.vn/dgx-qwq/v1/", 
    #     model='openai/openai/gpt-oss-20b',
    #     cwd='/home/quan/qodo/q-cover/templated_tests/java_spring_calculator/'
    #
    # ))
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
