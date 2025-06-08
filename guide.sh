cd /templated_tests/java_spring_calculator
export OPENAI_API_KEY="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"
cover-agent-full-repo \                                                             ✘ INT  cover-agent-py3.11
  --project-language="java" \
  --project-root="." \
  --code-coverage-report-path="target/site/jacoco/jacoco.csv" \
  --test-command="mvn clean verify" \
  --model="openai/gpt-4.1" --api-base="https://openrouter.ai/api/v1"
