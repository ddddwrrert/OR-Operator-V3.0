def ideas(model, context):
    response = model.request("operator_discovery", context)
    return response.get("ideas", []) if "ideas" in response else [response]
