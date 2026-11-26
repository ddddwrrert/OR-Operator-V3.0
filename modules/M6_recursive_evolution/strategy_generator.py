def generate(model, policy, history, weaknesses):
    return model.request("strategy_generation", {"policy": policy, "history": history[-4:], "weaknesses": weaknesses})
