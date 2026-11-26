from pathlib import Path
from setuptools import find_namespace_packages, setup

root = Path(__file__).parent
setup(
    name="or-operator-v30",
    version="3.0.0",
    python_requires=">=3.11",
    packages=find_namespace_packages(include=[
        "adapters*", "budget*", "config*", "core*", "evaluation*", "execution*",
        "interfaces*", "memory*", "meta*", "modules*", "prompts*",
    ]),
    py_modules=["main", "run"],
    package_data={"config": ["*.yaml"], "prompts": ["*.md"]},
    install_requires=(root / "requirements.txt").read_text().splitlines(),
    entry_points={"console_scripts": ["or-operator-v30=main:cli"]},
)
