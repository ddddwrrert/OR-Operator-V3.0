def graph(history):
    nodes = {row["operator"]["name"] for row in history if row.get("operator")}
    edges = [{"from": item["components"][0], "to": item["components"][-1],
              "sequence": item["components"], "interaction": item["interaction"],
              "conflict": item["conflict"]} for item in history if item.get("components")]
    return {"nodes": sorted(nodes), "edges": edges}
