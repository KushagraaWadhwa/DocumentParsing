import json
import ast
import os
import sys
import nbformat
from nbconvert import PythonExporter

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.elements = []

    def visit_FunctionDef(self, node):
        function_info = {
            'type': 'function',
            'name': node.name,
            'args': [arg.arg for arg in node.args.args],
            'defaults': len(node.args.defaults),
            'vararg': node.args.vararg.arg if node.args.vararg else None,
            'kwarg': node.args.kwarg.arg if node.args.kwarg else None,
            'lineno': node.lineno
        }
        self.elements.append(function_info)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        class_info = {
            'type': 'class',
            'name': node.name,
            'bases': [base.id for base in node.bases if isinstance(base, ast.Name)],
            'methods': [],
            'lineno': node.lineno
        }
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = {
                    'name': item.name,
                    'args': [arg.arg for arg in item.args.args],
                    'defaults': len(item.args.defaults),
                    'lineno': item.lineno
                }
                class_info['methods'].append(method_info)
        self.elements.append(class_info)
        self.generic_visit(node)

def convert_ipynb_to_py(ipynb_path):
    with open(ipynb_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
    
    exporter = PythonExporter()
    source, _ = exporter.from_notebook_node(notebook)
    
    py_path = ipynb_path.replace('.ipynb', '.py')
    with open(py_path, 'w', encoding='utf-8') as f:
        f.write(source)
    
    return py_path

def analyze_code(code):
    tree = ast.parse(code)
    analyzer = CodeAnalyzer()
    analyzer.visit(tree)
    return analyzer.elements

def analyze_notebook(ipynb_path):
    py_path = convert_ipynb_to_py(ipynb_path)
    
    with open(py_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    elements = analyze_code(code)
    elements.sort(key=lambda x: x['lineno'])
    
    for element in elements:
        if element['type'] == 'function':
            print(f"Function: {element['name']}")
            print(f"  Arguments: {', '.join(element['args'])}")
            print(f"  Default arguments: {element['defaults']}")
            print(f"  Vararg: {element['vararg']}")
            print(f"  Kwarg: {element['kwarg']}")
        elif element['type'] == 'class':
            print(f"Class: {element['name']}")
            print(f"  Bases: {', '.join(element['bases'])}")
            print(f"  Methods:")
            for method in element['methods']:
                print(f"    Method: {method['name']}")
                print(f"      Arguments: {', '.join(method['args'])}")
                print(f"      Default arguments: {method['defaults']}")
        print()
        print(code)

    # Clean up the temporary .py file
    os.remove(py_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)
    
    ipynb_path = sys.argv[1]
    analyze_notebook(ipynb_path)
