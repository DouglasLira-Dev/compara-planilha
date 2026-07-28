"""Ponto de entrada para linha de comando (CLI)."""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import __version__


def main() -> None:
    """Função principal da CLI."""
    print(f"🛡️ Comparador de Planilhas v{__version__}")

    if len(sys.argv) < 3:
        print("\n📋 Uso:")
        print("  python src/cli.py planilhaA.xlsx planilhaB.xlsx")
        print("\n📋 Opções:")
        print("  -o, --output    Nome do arquivo de saída")
        print("  --aba-a         Nome da aba na Planilha A")
        print("  --aba-b         Nome da aba na Planilha B")
        print("  -h, --help      Exibe esta ajuda")
        sys.exit(1)

    print(f"📊 Planilha A: {sys.argv[1]}")
    print(f"📊 Planilha B: {sys.argv[2]}")
    print("⏳ Comparação em desenvolvimento...")


if __name__ == "__main__":
    main()