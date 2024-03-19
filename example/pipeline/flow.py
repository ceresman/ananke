# Copyright 2023 undefined
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import networkx as nx
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# 创建一个有向图
graph = nx.DiGraph()

# 定义五个函数
def function1(data, count):
    count[0] += 1
    timestamp = time.time()
    data["a"] += 1
    time.sleep(1)  # 模拟耗时操作
    print(f"Function 1 - Run {count[0]} at {timestamp}")
    return data

def function2(data, count):
    count[1] += 1
    timestamp = time.time()
    data["b"] *= 2
    time.sleep(2)  # 模拟耗时操作
    print(f"Function 2 - Run {count[1]} at {timestamp}")
    return data

def function3(data, count):
    count[2] += 1
    timestamp = time.time()
    data["c"] -= 1
    time.sleep(3)  # 模拟耗时操作
    print(f"Function 3 - Run {count[2]} at {timestamp}")
    return data

def function4(data, count):
    count[3] += 1
    timestamp = time.time()
    data["d"] = data["a"] * data["b"]
    time.sleep(1)  # 模拟耗时操作
    print(f"Function 4 - Run {count[3]} at {timestamp}")
    return data

def function5(data, count):
    count[4] += 1
    timestamp = time.time()
    data["e"] = data["a"] + data["b"] + data["c"] + data["d"]
    time.sleep(1)  # 模拟耗时操作
    print(f"Function 5 - Run {count[4]} at {timestamp}")
    return data

# 添加节点和边
graph.add_node(function1)
graph.add_node(function2)
graph.add_node(function3)
graph.add_node(function4)
graph.add_node(function5)
graph.add_edge(function1, function4)
graph.add_edge(function2, function5)
graph.add_edge(function3, function4)
graph.add_edge(function4, function5)

# 执行顺序
execution_order = list(nx.topological_sort(graph))

# 执行函数
data = {
    "a": 1,
    "b": 2,
    "c": 3
}
count = [0, 0, 0, 0, 0]

# def execute_functions(execution_order, data, count, max_workers=3):
#     def execute_function(func, data, count):
#         return func(data, count)

#     with ThreadPoolExecutor(max_workers=max_workers) as executor:
#         futures = {executor.submit(execute_function, node, data, count): node for node in execution_order}
#         for future in as_completed(futures):
#             node = futures[future]
#             try:
#                 data = future.result()
#             except Exception as e:
#                 print(f"Function {node.__name__} failed to execute: {e}")
    
#     return data




def execute_functions(execution_order, data, count, max_workers=3):
    def execute_function(func, data, count):
        return func(data, count)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(execute_function, node, data, count): node for node in execution_order}
        for future in as_completed(futures):
            node = futures[future]
            try:
                data = future.result()
            except Exception as e:
                print(f"Function {node.__name__} failed to execute: {e}")
    
    # 检查所有依赖函数是否已经完成
    for node in execution_order:
        if not all([data[node] == 1 for node in list(nx.out_edges(node, graph))]):
            print(f"Function {node.__name__} has uncompleted dependencies")
            return None

    return data

execution_order = list(nx.topological_sort(graph))

data = execute_functions(execution_order, data, count, max_workers=8)
data = execute_functions(execution_order, data, count, max_workers=8)
data = execute_functions(execution_order, data, count, max_workers=8)

print("Final Data:", data)
