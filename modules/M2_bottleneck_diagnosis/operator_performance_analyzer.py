def rank(profile):
    return sorted(({"name": key, **stats, "gain_per_second": stats["gain"] / max(stats["seconds"], 1e-9)}
                   for key, stats in profile["observed"].items()),
                  key=lambda item: item["gain_per_second"], reverse=True)
