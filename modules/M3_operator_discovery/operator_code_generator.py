def code_for(model, idea, context):
    response = idea if "body" in idea else model.request("code_generation", {**context, "idea": idea})
    code = response.get("body")
    if not isinstance(code, str) or not code.strip():
        raise ValueError("Missing implementation body")
    return code
