"""Style guards for readability rules not currently implemented by Ruff."""

import ast
from pathlib import Path

SOURCE_ROOT = Path("src")


def test_source_avoids_nested_conditional_expressions() -> None:
    """Mirror Sonar rule S3358 by requiring explicit nested decisions."""

    violations: list[str] = []
    for path in SOURCE_ROOT.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.IfExp):
                continue
            nested_parts = (node.body, node.orelse)
            if any(
                isinstance(descendant, ast.IfExp)
                for part in nested_parts
                for descendant in ast.walk(part)
            ):
                violations.append(f"{path}:{node.lineno}")

    assert not violations, (
        "extract nested conditional expressions into explicit statements: "
        + ", ".join(violations)
    )
