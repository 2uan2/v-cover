cd /templated_tests/java_spring_calculator
export OPENAI_API_KEY="<API_KEY>"
cover-agent-full-repo \                                                             ✘ INT  cover-agent-py3.11
  --project-language="java" \
  --project-root="." \
  --code-coverage-report-path="target/site/jacoco/jacoco.csv" \
  --test-command="mvn clean verify" \
  --model="openai/gpt-4.1" --api-base="https://openrouter.ai/api/v1"
