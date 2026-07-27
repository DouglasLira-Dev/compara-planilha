"""Ponto de entrada principal da aplicação."""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para importações
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import __version__
from src.config import Config


def main() -> None:
    """Função principal da aplicação (GUI)."""
    print(f"🛡️ Comparador de Planilhas v{__version__}")
    print(f"📁 Diretório de logs: {Config.LOGS_DIR}")
    print(f"📁 Diretório de relatórios: {Config.REPORTS_DIR}")
    print("\n📋 Versão GUI em desenvolvimento...")
    print("💡 Em breve: Interface gráfica com PyQt6")
    print("\n✅ Configurações carregadas com sucesso!")


def cli_main() -> None:
    """Ponto de entrada para linha de comando."""
    if len(sys.argv) < 3:
        print(f"🛡️ Comparador de Planilhas v{__version__}")
        print("\n📋 Uso:")
        print("  python src/main.py planilhaA.xlsx planilhaB.xlsx")
        print("\n📋 Opções:")
        print("  -o, --output    Nome do arquivo de saída")
        print("  --aba-a         Nome da aba na Planilha A")
        print("  --aba-b         Nome da aba na Planilha B")
        print("  -h, --help      Exibe esta ajuda")
        sys.exit(1)

    print(f"📊 Planilha A: {sys.argv[1]}")
    print(f"📊 Planilha B: {sys.argv[2]}")
    print("⏳ Comparação em desenvolvimento...")
    print("📄 Relatório será gerado em breve...")


if __name__ == "__main__":
    # Se houver argumentos, executa CLI
    if len(sys.argv) > 1:
        cli_main()
    else:
        main()