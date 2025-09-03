import ast

with open('CalculatorApplication.java') as f:
    code = f.read()

node = ast.parse(code)
print(node)
