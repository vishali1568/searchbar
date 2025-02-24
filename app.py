from flask import Flask, request, render_template
import tempfile
import os
import autopep8
import subprocess
import ast  # Import AST module to detect syntax errors
import re  # Import re module for regex-based fixes

app = Flask(__name__)

def analyze_code(code):
    """Analyze the submitted Python code for syntax and style issues."""
    try:
        ast.parse(code)  # Check if the code has syntax errors
    except SyntaxError as e:
        return f"Syntax Error: {e}"

    # Save the code to a temp file for flake8 checking
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
        temp_file.write(code.encode('utf-8'))
        temp_file_path = temp_file.name

    try:
        # Run flake8 to find style issues
        result = subprocess.run(
            ["flake8", temp_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        feedback = result.stdout.strip()
        return feedback if feedback else "No issues found!"
    finally:
        os.remove(temp_file_path)

def fix_code_safely(code):
    """Fix common syntax issues before formatting."""
    fixed_code = code
    
    # 1. Fix missing colon after function definition or loop (e.g., def, for, while)
    fixed_code = re.sub(r'(\bdef \w+\(.*\))(\n?)', r'\1:', fixed_code)  # Add colon after function def
    fixed_code = re.sub(r'(\bfor .*in .*\))(\n?)', r'\1:', fixed_code)  # Add colon after for-loop
    fixed_code = re.sub(r'(\bwhile .*\))(\n?)', r'\1:', fixed_code)  # Add colon after while-loop
    
    # 2. Fix missing closing parentheses
    fixed_code = re.sub(r'(\(.*)([^\)])$', r'\1)', fixed_code)  # Add closing parentheses if missing

    try:
        # 3. Run autopep8 for code formatting (e.g., indentation, spacing)
        fixed_code = autopep8.fix_code(fixed_code)
        
        # 4. Validate if the fixed code is now valid
        ast.parse(fixed_code)
        return fixed_code
    except SyntaxError:
        return "❌ Could not auto-fix syntax errors. Please review manually."

@app.route('/', methods=['GET', 'POST'])
def index():
    feedback = ""
    fixed_code = ""
    user_code = ""

    if request.method == 'POST':
        user_code = request.form['code']
        feedback = analyze_code(user_code)  # Analyze for issues
        fixed_code = fix_code_safely(user_code)  # Attempt to fix the code

    return render_template('index.html', feedback=feedback, fixed_code=fixed_code, user_code=user_code)

if __name__ == '__main__':
    app.run(debug=True)
