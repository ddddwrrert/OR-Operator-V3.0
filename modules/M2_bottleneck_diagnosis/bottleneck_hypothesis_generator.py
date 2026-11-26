def generate(model, evidence, source, directive=""):
    return model.request("bottleneck_diagnosis", {"evidence": evidence, "source": source, "directive": directive})
