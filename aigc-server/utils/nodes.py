import json, os



def is_real_nodes(item):
    real = True
    nodes = item.get("nodes", [])
    rels = item.get("relationships", [])

    if len(nodes) == 0 and len(rels) == 0:
        return False

    for node in nodes:
        if ("alice" in node or "Alice" in node or "bob" in node or "Bob" in node):
           real = False
           break

    for rel in rels:
        if ("alice" in node or "Alice" in node or "bob" in node or "Bob" in node):
            real = False
            break

    return real


def update_nodes_rels(nodes_dic, rels_dic, item):
    nodes = item.get("nodes")
    for node in nodes:
        if len(node) < 3:
            continue

        node_name, node_label, node_property = node[0], node[1], node[2]
        if type(node_property) != dict:
            continue

        nodes_dic.setdefault(node_label, {})
        nodes_dic[node_label].setdefault(node_name, node_property)
        if node_name in nodes_dic[node_label].keys():
            property = {**node_property, **(nodes_dic[node_label].get(node_name))}
            nodes_dic[node_label][node_name] = property

    rels = item.get("relationships", [])
    for rel in rels:
        if len(rel) < 4:
            continue
        sub, rel, obj, property = rel[0], rel[1], rel[2], rel[3]
        rels_dic.setdefault(sub, {})
        rels_dic[sub].setdefault(rel, [])
        rels_dic[sub][rel].append((obj, property))

