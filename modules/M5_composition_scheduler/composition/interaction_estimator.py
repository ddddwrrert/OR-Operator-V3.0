def interaction(control, singles, together):
    return together - control - sum(value - control for value in singles)
