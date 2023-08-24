import subprocess
import os
import tempfile
import ast
import time
import astor
import re
import base64
def is_show_node(node: ast.Call) -> bool:
    if not hasattr(node, "value"):
        return False

    value = node.value
    return (
        isinstance(value, ast.Call)
        and value.func
        and (
            isinstance(value.func, ast.Attribute)
            and value.func.attr == "show"
            and value.func.value.id == "plt"
        )
    )


class CodeExecutor():

    def __init__(self, mix_code):
        #self.interpreter = os.path.join(self.path, "bin/python3")
        #self.temp = NamedTemporaryFile(delete=False)
        #with self.temp as f:
        #    f.write(source_code);
        #    f.close()
        self._mix_code = mix_code        

    def run_plot_code(self, df):
        html = ''
        python_code = ''
        lines = self._mix_code.split('\n')
        i  = 0
        while i < len(lines):
            if lines[i] == "```python":
                i +=1
                while lines[i] != "```":
                    python_code += lines[i] +'\n'
                    i += 1
                i += 1
                temp_files = []
                tree = ast.parse(python_code)
                show_count = sum(1 for node in ast.walk(tree) if is_show_node(node))
                # if there are no plt.show() calls, return the original code
                new_body = []
                if show_count: 
                    for node in tree.body:
                        if is_show_node(node):
                            image_id = f"{str(round(time.time() * 1000))}.png"
                            image_path = os.path.join('/tmp',image_id)
                            new_body.append(ast.parse(f"plt.savefig('{image_path}')"))
                            temp_files.append(image_path)
                        new_body.append(node)
                new_tree = ast.Module(body=new_body)
                python_code = astor.to_source(new_tree, pretty_source=lambda x: "".join(x)).strip()
                environment = {'df': df.dropna(axis=0, how='all')}
                exec(python_code, environment)
                for image_path in temp_files:
                    with open(image_path,'rb') as f:
                        content = f.read()
                        base64Str = base64.b64encode(content).decode('utf-8')
                        html += f'<img src="data:image/png;base64,{base64Str}">'
            else:
                html +=f"<p>{lines[i]}</p>"
                i += 1
        return html
    
    def run_flowchart_code(self):
        html = ''
        flowchart_code = ''
        lines = self._mix_code.split('\n')
        i  = 0
        while i < len(lines):
            if lines[i] == "```mermaid":
                flowchart_code += lines[i] +'\n'
                i += 1
                while True:
                    flowchart_code += lines[i] +'\n'
                    if lines[i] == "```":
                        break
                    i += 1
                input_image_id = f"{str(round(time.time() * 1000))}.mrk"
                input_image_path = os.path.join('/tmp',input_image_id)
                output_image_id = f"{str(round(time.time() * 1000))}.png"
                output_image_path = os.path.join('/tmp',output_image_id)
                os.system(f"python -m echo Hello from the other side!")
                #for image_path in temp_files:
                #    with open(image_path,'rb') as f:
                #        content = f.read()
                #        base64Str = base64.b64encode(content).decode('utf-8')
                #        html += f'<img src="data:image/png;base64,{base64Str}">'
            else:
                html +=f"<p>{lines[i]}</p>"
                i += 1
        return html