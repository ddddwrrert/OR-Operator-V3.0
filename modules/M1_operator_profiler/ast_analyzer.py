import ast
import re


def analyze(parsed):
    if parsed["language"] == "python":
        body = parsed["executable"]
        root = ast.parse(body)
        regions = [{"name": "<inline>", "nodes": root.body}]
        regions.extend({"name": node.name, "nodes": node.body}
                       for node in ast.walk(root) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)))
        records = []
        for region in regions:
            nodes = []
            pending = list(region["nodes"])
            while pending:
                node = pending.pop(0)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    continue
                nodes.append(node)
                pending.extend(ast.iter_child_nodes(node))
            records.append({
                "name": region["name"],
                "calls": [ast.unparse(n.func) for n in nodes if isinstance(n, ast.Call)],
                "writes": [ast.unparse(n) for n in nodes if isinstance(n, (ast.Name, ast.Subscript, ast.Attribute))
                           and isinstance(n.ctx, ast.Store)],
                "branches": [type(n).__name__.lower() for n in nodes if isinstance(n, (ast.For, ast.While, ast.If, ast.Assert))],
            })
        return records

    records = [{"name": "<inline>", "calls": [], "writes": [], "branches": []}]
    for line in parsed["body"].splitlines():
        line = line.split("//", 1)[0]
        decl = re.match(r"\s*(?:[\w:*<>]+\s+)+(\w+)\s*\([^;]*\)\s*\{", line)
        if decl and decl[1] not in {"if", "for", "while", "switch"}:
            records.append({"name": decl[1], "calls": [], "writes": [], "branches": []})
        current = records[-1]
        current["calls"].extend(word for word in re.findall(r"\b(\w+)\s*\(", line)
                                if word not in {"if", "for", "while", "switch", current["name"]})
        current["writes"].extend(re.findall(r"(\w+(?:\[[^\]]+\])?)\s*(?:[+*/-]?=(?!=)|\+\+|--)", line))
        current["branches"].extend(re.findall(r"\b(?:if|for|while|switch)\b", line))
    return records
