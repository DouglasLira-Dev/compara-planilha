"""Módulo de configurações do sistema."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()


class Config:
    """Configurações do sistema."""

    # Caminhos
    BASE_DIR: Path = Path(__file__).parent.parent
    LOGS_DIR: Path = Path(os.getenv("LOGS_DIR", str(BASE_DIR / "logs")))
    REPORTS_DIR: Path = Path(os.getenv("REPORTS_DIR", str(BASE_DIR / "relatorios")))

    # Logs
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_RETENTION_DAYS: int = int(os.getenv("LOG_RETENTION_DAYS", "30"))
    MAX_LOG_SIZE_MB: int = int(os.getenv("MAX_LOG_SIZE_MB", "10"))

    # Processamento
    MAX_REGISTROS: int = int(os.getenv("MAX_REGISTROS", "0"))
    MAX_LINHAS_BUSCA_CABECALHO: int = int(os.getenv("MAX_LINHAS_BUSCA_CABECALHO", "10"))

    # Relatório
    RELATORIO_NOME_PADRAO: str = os.getenv("RELATORIO_NOME_PADRAO", "relatorio_comparacao.xlsx")

    @classmethod
    def ensure_directories(cls) -> None:
        """Cria os diretórios necessários se não existirem."""
        cls.LOGS_DIR.mkdir(exist_ok=True, parents=True)
        cls.REPORTS_DIR.mkdir(exist_ok=True, parents=True)

    @classmethod
    def get_log_file(cls) -> Path:
        """Retorna o caminho do arquivo de log."""
        return cls.LOGS_DIR / "comparador.log"


# Garante que os diretórios existem
Config.ensure_directories()