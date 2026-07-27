"""Script para gerenciar a versão do projeto."""

import re
import sys
from pathlib import Path


def get_version() -> str:
    """Lê a versão do arquivo __init__.py."""
    init_file = Path("src/__init__.py")
    content = init_file.read_text()
    match = re.search(r'__version__\s*=\s*"([^"]+)"', content)
    if match:
        return match.group(1)
    return "0.0.0"


def bump_version(part: str = "patch") -> str:
    """
    Incrementa a versão.

    Args:
        part: "major", "minor" ou "patch"

    Returns:
        Nova versão
    """
    current = get_version()
    major, minor, patch = map(int, current.split("."))

    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    else:  # patch
        patch += 1

    new_version = f"{major}.{minor}.{patch}"

    # Atualiza o arquivo __init__.py
    init_file = Path("src/__init__.py")
    content = init_file.read_text()
    content = re.sub(
        r'__version__\s*=\s*"[^"]+"',
        f'__version__ = "{new_version}"',
        content
    )
    init_file.write_text(content)

    return new_version


if __name__ == "__main__":
    if len(sys.argv) > 1:
        part = sys.argv[1]
        if part in ["major", "minor", "patch"]:
            new_version = bump_version(part)
            print(f"✅ Versão atualizada para: {new_version}")
        else:
            print("❌ Uso: python scripts/version.py [major|minor|patch]")
            sys.exit(1)
    else:
        print(f"📌 Versão atual: {get_version()}")