from pathlib import Path
from execution.code_integrator import executable, split


def parse_source(source, filename):
    return {"language": "python" if Path(filename).suffix == ".py" else "cpp",
            "body": split(source)[1], "executable": executable(source)}
