from .ast_analyzer import analyze
from .call_graph import graph
from .operator_extractor import extract
from .runtime_profiler import summarize, telemetry
from .source_parser import parse_source


def build_profile(source, filename, history):
    parsed = parse_source(source, filename)
    regions = analyze(parsed)
    return {"language": parsed["language"], "graph": graph(regions),
            "operators": extract(regions), "observed": summarize(history), "instrumented": telemetry(history)}
