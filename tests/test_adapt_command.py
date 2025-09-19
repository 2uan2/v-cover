from cover_agent.lsp_logic.utils.utils_adapt_command import adapt_test_command

# og = "coverage run -m pytest --cov=. -- --verbose"
# og = "mvn test -Dtest.parallel=true -DforkCount=4"
# og = "gradle test --parallel --max-workers=4 --continue"
# og = "pytest --maxfail=1 --disable-warnings -q"
# og = "mvn test -DskipIntegrationTests=true"
# og = "jest --runInBand --detectOpenHandles"
# og = "npm test -- --watchAll=false"
# print(og)
# print(adapt_test_command(og, "./lol"))
# test_cases = [
#     ("pytest --cov=src --verbose tests/", "tests/unit/test_auth.py"),
#     ("jest --coverage --watch", "src/components/Button.test.js"),
#     ("go test ./... -v -race", "internal/auth/auth_test.go"),
#     ("mvn test -Dtest=OldTest", "src/test/java/NewTest.java"),
#     ("rspec --format documentation", "spec/models/user_spec.rb"),
# ]
#
# for command, file_path in test_cases:
#     result = adapt_test_command(command, file_path)
#     print(f"Original: {command}")
#     print(f"Adapted:  {result}")
# import pytest
# from unittest.mock import patch, MagicMock
# import os
#
# # Assuming the function is in a module called test_adapter
# # from test_adapter import adapt_test_command
#
# # Mock os.path.exists to avoid file system dependencies
# def mock_exists(path):
#     """Mock os.path.exists to return True for test-like paths"""
#     test_indicators = ['test', 'spec', '.py', '.js', '.java', '.rb', '.php', '.rs']
#     return any(indicator in path.lower() for indicator in test_indicators)
#
#
# class TestAdaptTestCommand:
#     """Test cases for adapt_test_command function"""
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_pytest_basic(self, mock_exists_func):
#         """Test basic pytest command adaptation"""
#         command = "pytest --cov=src --verbose tests/"
#         file_path = "tests/unit/test_auth.py"
#         expected = "pytest --cov=src --verbose tests/unit/test_auth.py"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_pytest_with_existing_file_removal(self, mock_exists_func):
#         """Test pytest removes existing file paths"""
#         command = "pytest --cov=src tests/old_test.py"
#         file_path = "tests/unit/test_auth.py"
#         expected = "pytest --cov=src tests/unit/test_auth.py"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_pytest_with_flags_and_values(self, mock_exists_func):
#         """Test pytest preserves flags with values"""
#         command = "pytest -k test_user --tb=short --cov=src"
#         file_path = "tests/test_auth.py"
#         expected = "pytest -k test_user --tb=short --cov=src tests/test_auth.py"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_jest_basic(self, mock_exists_func):
#         """Test basic Jest command adaptation"""
#         command = "jest --coverage --watch"
#         file_path = "src/components/Button.test.js"
#         expected = "jest --coverage --watch src/components/Button.test.js"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_jest_with_config(self, mock_exists_func):
#         """Test Jest with configuration flags"""
#         command = "jest --config jest.config.js --maxWorkers=4"
#         file_path = "src/utils/helper.test.js"
#         expected = "jest --config jest.config.js --maxWorkers=4 src/utils/helper.test.js"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_go_test_basic(self, mock_exists_func):
#         """Test basic Go test command adaptation"""
#         command = "go test ./... -v -race"
#         file_path = "internal/auth/auth_test.go"
#         expected = "go test -v -race ./internal/auth"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_go_test_current_directory(self, mock_exists_func):
#         """Test Go test with file in current directory"""
#         command = "go test ./... -v"
#         file_path = "main_test.go"
#         expected = "go test -v ./"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_maven_basic(self, mock_exists_func):
#         """Test basic Maven command adaptation"""
#         command = "mvn test"
#         file_path = "src/test/java/UserTest.java"
#         expected = "mvn test -Dtest=UserTest"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_maven_replace_existing_dtest(self, mock_exists_func):
#         """Test Maven replaces existing -Dtest argument"""
#         command = "mvn test -Dtest=OldTest"
#         file_path = "src/test/java/NewTest.java"
#         expected = "mvn test -Dtest=NewTest"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_gradle_basic(self, mock_exists_func):
#         """Test basic Gradle command adaptation"""
#         command = "gradle test"
#         file_path = "src/test/java/UserServiceTest.java"
#         expected = 'gradle test --tests "UserServiceTest"'
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_gradle_replace_existing_tests(self, mock_exists_func):
#         """Test Gradle replaces existing --tests argument"""
#         command = "gradle test --tests OldTest"
#         file_path = "src/test/java/NewTest.java"
#         expected = 'gradle test --tests "NewTest"'
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_rspec_basic(self, mock_exists_func):
#         """Test basic RSpec command adaptation"""
#         command = "rspec --format documentation"
#         file_path = "spec/models/user_spec.rb"
#         expected = "rspec --format documentation spec/models/user_spec.rb"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_rspec_with_existing_spec_path(self, mock_exists_func):
#         """Test RSpec removes existing spec paths"""
#         command = "rspec --format doc spec/"
#         file_path = "spec/models/user_spec.rb"
#         expected = "rspec --format doc spec/models/user_spec.rb"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_npm_test_basic(self, mock_exists_func):
#         """Test npm test command adaptation"""
#         command = "npm test"
#         file_path = "tests/unit/auth.test.js"
#         expected = "npm test -- tests/unit/auth.test.js"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_npm_test_with_existing_separator(self, mock_exists_func):
#         """Test npm test with existing -- separator"""
#         command = "npm test -- --coverage"
#         file_path = "tests/auth.test.js"
#         expected = "npm test -- tests/auth.test.js"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_yarn_test(self, mock_exists_func):
#         """Test yarn test command adaptation"""
#         command = "yarn test"
#         file_path = "src/components/Button.test.tsx"
#         expected = "yarn test -- src/components/Button.test.tsx"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_pnpm_test(self, mock_exists_func):
#         """Test pnpm test command adaptation"""
#         command = "pnpm test"
#         file_path = "tests/utils.test.js"
#         expected = "pnpm test -- tests/utils.test.js"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_dotnet_test_basic(self, mock_exists_func):
#         """Test dotnet test command adaptation"""
#         command = "dotnet test"
#         file_path = "Tests/UserServiceTest.cs"
#         expected = "dotnet test --filter ClassName=UserServiceTest"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_dotnet_test_replace_existing_filter(self, mock_exists_func):
#         """Test dotnet test replaces existing --filter"""
#         command = "dotnet test --filter ClassName=OldTest"
#         file_path = "Tests/NewTest.cs"
#         expected = "dotnet test --filter ClassName=NewTest"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_phpunit_basic(self, mock_exists_func):
#         """Test PHPUnit command adaptation"""
#         command = "phpunit --coverage-html coverage"
#         file_path = "tests/Unit/UserTest.php"
#         expected = "phpunit --coverage-html coverage tests/Unit/UserTest.php"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_mocha_basic(self, mock_exists_func):
#         """Test Mocha command adaptation"""
#         command = "mocha --recursive --reporter spec test/"
#         file_path = "test/unit/auth.test.js"
#         expected = "mocha --reporter spec test/unit/auth.test.js"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_cargo_test_integration(self, mock_exists_func):
#         """Test Cargo test for integration tests"""
#         command = "cargo test --release"
#         file_path = "tests/integration_test.rs"
#         expected = "cargo test --release --test integration_test"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_cargo_test_unit(self, mock_exists_func):
#         """Test Cargo test for unit tests"""
#         command = "cargo test"
#         file_path = "src/lib.rs"
#         expected = "cargo test lib"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_python_unittest(self, mock_exists_func):
#         """Test Python unittest command adaptation"""
#         command = "python -m unittest"
#         file_path = "tests/test_user.py"
#         expected = "python -m unittest tests.test_user"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     def test_unsupported_framework(self):
#         """Test unsupported framework returns None"""
#         command = "custom_test_runner --all"
#         file_path = "tests/test_file.py"
#         
#         result = adapt_test_command(command, file_path)
#         assert result is None
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_gradlew_wrapper(self, mock_exists_func):
#         """Test Gradle wrapper command"""
#         command = "./gradlew test --parallel"
#         file_path = "src/test/java/TestClass.java"
#         expected = './gradlew test --parallel --tests "TestClass"'
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_mvnw_wrapper(self, mock_exists_func):
#         """Test Maven wrapper command"""
#         command = "./mvnw test -q"
#         file_path = "src/test/java/TestClass.java"
#         expected = "./mvnw test -q -Dtest=TestClass"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_complex_pytest_command(self, mock_exists_func):
#         """Test complex pytest command with multiple flags and paths"""
#         command = "pytest -v --cov=src --cov-report=html --tb=short tests/ integration/"
#         file_path = "tests/unit/test_complex.py"
#         expected = "pytest -v --cov=src --cov-report=html --tb=short tests/unit/test_complex.py"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_jest_with_test_pattern(self, mock_exists_func):
#         """Test Jest command with test name pattern"""
#         command = "jest --testNamePattern=user --watch src/"
#         file_path = "src/auth/user.test.js"
#         expected = "jest --testNamePattern=user --watch src/auth/user.test.js"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#
#
# # Additional edge case tests
# class TestEdgeCases:
#     """Test edge cases and error conditions"""
#     
#     def test_empty_command(self):
#         """Test empty command string"""
#         result = adapt_test_command("", "test.py")
#         assert result is None
#     
#     def test_whitespace_command(self):
#         """Test command with only whitespace"""
#         result = adapt_test_command("   ", "test.py")
#         assert result is None
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_command_with_quotes(self, mock_exists_func):
#         """Test command with quoted arguments"""
#         command = 'pytest -k "test_user and not slow"'
#         file_path = "tests/test_auth.py"
#         expected = 'pytest -k "test_user and not slow" tests/test_auth.py'
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#     
#     @patch('os.path.exists', side_effect=mock_exists)
#     def test_file_path_with_spaces(self, mock_exists_func):
#         """Test file path containing spaces"""
#         command = "pytest --verbose"
#         file_path = "tests/unit tests/test auth.py"
#         expected = "pytest --verbose tests/unit tests/test auth.py"
#         
#         result = adapt_test_command(command, file_path)
#         assert result == expected
#
#
# if __name__ == "__main__":
#     # Run the tests
#     pytest.main([__file__, "-v"])
import pytest
from typing import Optional

# Function signature we're testing:
# def adapt_test_command_for_single_file(test_command: str, test_file_path: str) -> str

class TestAdaptTestCommandForSingleFile:
    """Test suite for rule-based test command adaptation function."""

    # Python/pytest test cases
    def test_pytest_basic(self):
        """Test basic pytest command."""
        result = adapt_test_command("pytest", "tests/test_utils.py")
        assert result == "pytest tests/test_utils.py"

    def test_pytest_with_flags(self):
        """Test pytest with various flags."""
        result = adapt_test_command(
            "pytest -v --tb=short", 
            "tests/test_api.py"
        )
        assert result == "pytest -v --tb=short tests/test_api.py"

    def test_pytest_with_coverage(self):
        """Test pytest with coverage options."""
        result = adapt_test_command(
            "pytest --cov=src --cov-report=html --cov-report=term-missing",
            "tests/integration/test_database.py"
        )
        assert result == "pytest --cov=src --cov-report=html --cov-report=term-missing tests/integration/test_database.py"

    def test_pytest_with_existing_file_arg(self):
        """Test pytest that already has a file argument - should replace it."""
        result = adapt_test_command(
            "pytest tests/", 
            "tests/test_specific.py"
        )
        assert result == "pytest tests/test_specific.py"

    def test_pytest_with_multiple_paths(self):
        """Test pytest with multiple existing paths - should replace them."""
        result = adapt_test_command(
            "pytest tests/ src/", 
            "tests/test_one.py"
        )
        assert result == "pytest tests/test_one.py"

    def test_python_m_pytest(self):
        """Test python -m pytest format."""
        result = adapt_test_command(
            "python -m pytest -v", 
            "tests/test_module.py"
        )
        assert result == "python -m pytest -v tests/test_module.py"

    # Node.js/Jest test cases
    def test_npm_test_basic(self):
        """Test basic npm test command."""
        result = adapt_test_command(
            "npm test", 
            "src/components/__tests__/Button.test.js"
        )
        assert result == "npm test -- src/components/__tests__/Button.test.js"

    def test_npm_run_test(self):
        """Test npm run test command."""
        result = adapt_test_command(
            "npm run test", 
            "tests/utils.test.js"
        )
        assert result == "npm run test -- tests/utils.test.js"

    def test_yarn_test(self):
        """Test yarn test command."""
        result = adapt_test_command(
            "yarn test", 
            "src/__tests__/App.test.tsx"
        )
        assert result == "yarn test -- src/__tests__/App.test.tsx"

    def test_jest_direct(self):
        """Test direct Jest command."""
        result = adapt_test_command(
            "jest --coverage", 
            "tests/api.test.js"
        )
        assert result == "jest --coverage tests/api.test.js"

    def test_npx_jest(self):
        """Test npx jest command."""
        result = adapt_test_command(
            "npx jest --watchAll=false", 
            "src/utils.test.ts"
        )
        assert result == "npx jest --watchAll=false src/utils.test.ts"

    # Java/Maven test cases
    def test_mvn_test_basic(self):
        """Test basic Maven test command."""
        result = adapt_test_command(
            "mvn test", 
            "src/test/java/com/example/UserServiceTest.java"
        )
        assert result == "mvn test -Dtest=UserServiceTest"

    def test_mvn_test_with_profile(self):
        """Test Maven test with profile."""
        result = adapt_test_command(
            "mvn test -Pintegration", 
            "src/test/java/com/example/integration/DatabaseTest.java"
        )
        assert result == "mvn test -Pintegration -Dtest=DatabaseTest"

    def test_mvn_test_nested_class(self):
        """Test Maven test with nested test class path."""
        result = adapt_test_command(
            "mvn test", 
            "src/test/java/com/company/module/service/UserServiceTest.java"
        )
        assert result == "mvn test -Dtest=UserServiceTest"

    # Java/Gradle test cases
    def test_gradle_test_basic(self):
        """Test basic Gradle test command."""
        result = adapt_test_command(
            "./gradlew test", 
            "src/test/java/com/example/CalculatorTest.java"
        )
        assert result == './gradlew test --tests "CalculatorTest"'

    def test_gradle_test_with_flags(self):
        """Test Gradle test with additional flags."""
        result = adapt_test_command(
            "./gradlew test --info", 
            "src/test/kotlin/com/example/ServiceTest.kt"
        )
        assert result == './gradlew test --info --tests "ServiceTest"'

    # Go test cases
    def test_go_test_all(self):
        """Test go test ./... command."""
        result = adapt_test_command(
            "go test ./...", 
            "internal/handlers/user_test.go"
        )
        assert result == "go test ./internal/handlers"

    def test_go_test_with_verbose(self):
        """Test go test with verbose flag."""
        result = adapt_test_command(
            "go test -v ./...", 
            "pkg/utils/math_test.go"
        )
        assert result == "go test -v ./pkg/utils"

    def test_go_test_with_coverage(self):
        """Test go test with coverage."""
        result = adapt_test_command(
            "go test -cover -race ./...", 
            "cmd/server/main_test.go"
        )
        assert result == "go test -cover -race ./cmd/server"

    def test_go_test_single_package(self):
        """Test go test on single package."""
        result = adapt_test_command(
            "go test ./internal/...", 
            "internal/auth/token_test.go"
        )
        assert result == "go test ./internal/auth"

    # Ruby/RSpec test cases
    def test_rspec_basic(self):
        """Test basic RSpec command."""
        result = adapt_test_command(
            "rspec", 
            "spec/models/user_spec.rb"
        )
        assert result == "rspec spec/models/user_spec.rb"

    def test_bundle_exec_rspec(self):
        """Test bundle exec rspec command."""
        result = adapt_test_command(
            "bundle exec rspec", 
            "spec/controllers/users_controller_spec.rb"
        )
        assert result == "bundle exec rspec spec/controllers/users_controller_spec.rb"

    def test_rspec_with_format(self):
        """Test RSpec with format options."""
        result = adapt_test_command(
            "rspec --format documentation", 
            "spec/services/auth_service_spec.rb"
        )
        assert result == "rspec --format documentation spec/services/auth_service_spec.rb"

    # C#/.NET test cases
    def test_dotnet_test_basic(self):
        """Test basic dotnet test command."""
        result = adapt_test_command(
            "dotnet test", 
            "tests/UserServiceTests.cs"
        )
        assert result == "dotnet test --filter FullyQualifiedName~UserServiceTests"

    def test_dotnet_test_with_project(self):
        """Test dotnet test with specific project."""
        result = adapt_test_command(
            "dotnet test MyProject.Tests.csproj", 
            "tests/Integration/DatabaseTests.cs"
        )
        assert result == "dotnet test MyProject.Tests.csproj --filter FullyQualifiedName~DatabaseTests"

    # Edge cases and complex scenarios
    def test_command_with_environment_variables(self):
        """Test command with environment variables."""
        result = adapt_test_command(
            "ENV=test pytest --tb=short", 
            "tests/test_env.py"
        )
        assert result == "ENV=test pytest --tb=short tests/test_env.py"

    def test_deeply_nested_test_file(self):
        """Test with deeply nested test file path."""
        result = adapt_test_command(
            "pytest", 
            "tests/unit/services/auth/providers/oauth/test_google.py"
        )
        assert result == "pytest tests/unit/services/auth/providers/oauth/test_google.py"

    def test_windows_path_separators(self):
        """Test with Windows-style path separators."""
        result = adapt_test_command(
            "pytest", 
            "tests\\unit\\test_utils.py"
        )
        # Should normalize to forward slashes or handle appropriately
        assert "test_utils.py" in result

    def test_test_file_without_extension(self):
        """Test with test file path without extension (edge case)."""
        result = adapt_test_command(
            "go test ./...", 
            "internal/handlers/user_test"
        )
        # Should still work for Go tests
        assert result == "go test ./internal/handlers"

    def test_relative_vs_absolute_paths(self):
        """Test handling of relative vs absolute paths."""
        result = adapt_test_command(
            "pytest", 
            "./tests/test_relative.py"
        )
        assert result == "pytest ./tests/test_relative.py"

    def test_command_already_targeting_specific_file(self):
        """Test command that already targets the same specific file."""
        result = adapt_test_command(
            "pytest tests/test_specific.py", 
            "tests/test_specific.py"
        )
        # Should return the same command since it's already correct
        assert result == "pytest tests/test_specific.py"

    def test_command_with_test_name_pattern(self):
        """Test command with existing test name patterns."""
        result = adapt_test_command(
            "pytest -k test_login", 
            "tests/test_auth.py"
        )
        # Should preserve the pattern but target the specific file
        assert result == "pytest -k test_login tests/test_auth.py"

    # Performance and boundary tests
    def test_very_long_command(self):
        """Test with very long command line."""
        long_flags = " ".join([f"--flag{i}=value{i}" for i in range(50)])
        command = f"pytest {long_flags}"
        result = adapt_test_command(command, "tests/test_long.py")
        assert result.endswith("tests/test_long.py")
        assert len(result) > len(command)

    def test_very_long_file_path(self):
        """Test with very long file path."""
        long_path = "/".join([f"level{i}" for i in range(20)]) + "/test_deep.py"
        result = adapt_test_command("pytest", long_path)
        assert result == f"pytest {long_path}"
