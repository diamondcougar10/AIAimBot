import sys

with open('AI-Aimbot/gui.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_code = '''            # Get the virtual environment python path
            venv_python = Path(".venv/Scripts/python.exe")
            if venv_python.exists():
                python_cmd = str(venv_python)
            else:
                python_cmd = sys.executable'''

new_code = '''            # Get the virtual environment python path
            venv_python = Path("../.venv/Scripts/python.exe")
            if not venv_python.exists():
                venv_python = Path(".venv/Scripts/python.exe")
            if venv_python.exists():
                python_cmd = str(venv_python)
            else:
                python_cmd = sys.executable'''

content = content.replace(old_code, new_code)

with open('AI-Aimbot/gui.py', 'w', encoding='utf-8') as f:
    f.write(content)
    
print('GUI fixed! The venv path has been updated.')
