import ast
import os
from graphviz import Digraph
from ananke.base import BaseObject
class CodeAnalyzer(ast.NodeVisitor,BaseObject):    
    def __init__(self):    
        self.classes = {}    
        self.current_class_name = None    
    
    def visit_ClassDef(self, node):    
        class_name = node.name    
        self.current_class_name = class_name    
        bases = [b.id for b in node.bases if isinstance(b, ast.Name)]    
        self.classes[class_name] = {'methods': [], 'attributes': {}, 'bases': bases}    
    
        for body_item in node.body:    
            if isinstance(body_item, ast.FunctionDef):    
                self.classes[class_name]['methods'].append(body_item.name)    
            elif isinstance(body_item, ast.Assign):    
                for target, value in zip(body_item.targets, body_item.value.elts if isinstance(body_item.value, ast.Tuple) else [body_item.value]):  
                    if isinstance(target, ast.Name):  
                        # 尝试猜测变量类型  
                        attr_type = self.guess_type(value)  
                        self.classes[class_name]['attributes'][target.id] = attr_type  
        self.current_class_name = None    
    
        self.generic_visit(node)   
  
    def guess_type(self, value):  
        """基于AST节点猜测类型。"""  
        if isinstance(value, ast.Str):  
            return 'str'  
        elif isinstance(value, ast.Num):  
            return 'int' if isinstance(value.n, int) else 'float'  
        elif isinstance(value, ast.List):  
            return 'list'  
        elif isinstance(value, ast.Dict):  
            return 'dict'  
        elif isinstance(value, ast.Name):  
            return value.id  
        elif isinstance(value, ast.Attribute):  
            return 'instance'  
        else:  
            return 'unknown'  
  
def generate_uml(classes, output_file='uml_graph'):  
    dot = Digraph(comment='UML Diagram', format='png')  
    for cls_name, cls_details in classes.items():  
        # Create UML-like class diagram with attributes and methods  
        class_label = '{' + cls_name  
        if cls_details['attributes']:  
            class_label += '|'  
            attr_lines = [f'{attr}: {typ}' for attr, typ in cls_details['attributes'].items()]  
            class_label += '\\l'.join(attr_lines) + '\\l'  
        if cls_details['methods']:  
            class_label += '|'  
            class_label += '\\l'.join(cls_details['methods']) + '\\l'  
        class_label += '}'  
        dot.node(cls_name, label=class_label, shape='record') # Use "record" shape for class-like display  
  
        for base in cls_details['bases']:  
            dot.edge(base, cls_name, arrowhead='empty') # Use "empty" arrowhead for inheritance  
  
    dot.render(output_file, view=False)  # Set view to False  
    print(f"UML diagram generated: {output_file}.png") 
  
def analyze_project(project_path):  
    analyzer = CodeAnalyzer()  
    for subdir, dirs, files in os.walk(project_path):  
        for file in files:  
            if file.endswith('.py'):  
                analyzer.visit(ast.parse(open(os.path.join(subdir, file)).read()))  
    return analyzer.classes  
  
def main(project_path):  
    classes = analyze_project(project_path)  
    generate_uml(classes)
    
    
if __name__ == "__main__":
    project_path = '/workspace/ananke/src'
    main(project_path)
