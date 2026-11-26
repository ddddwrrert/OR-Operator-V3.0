from execution.code_integrator import integrate


def adapt(parent, operator):
    return integrate(parent, operator.body)
