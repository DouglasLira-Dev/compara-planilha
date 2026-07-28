"""Módulo de normalização de dados."""

import re
from datetime import datetime

import pandas as pd
from dateutil import parser

from src.validators import ValidadorCPF, ValidadorData


class NormalizadorDados:
    """Classe para normalização de dados de planilhas."""

    @staticmethod
    def normalizar_cpf(valor: str | int | None) -> str:
        """
        Normaliza CPF com validação e completação de zeros à esquerda.

        Regras:
        - Remove máscara (., -, /)
        - Adiciona zeros à esquerda se faltar
        - Valida dígitos verificadores

        Args:
            valor: CPF em qualquer formato

        Returns:
            CPF normalizado com 11 dígitos

        Raises:
            ValueError: Se o CPF for inválido ou vazio
        """
        if pd.isna(valor) or valor is None:
            raise ValueError("CPF não pode ser vazio")

        # Converte para string
        if isinstance(valor, (int, float)):
            cpf_str = str(int(valor))
        else:
            cpf_str = str(valor)

        # Remove caracteres não numéricos
        cpf_limpo = re.sub(r"[^0-9]", "", cpf_str)

        if len(cpf_limpo) == 0:
            raise ValueError("CPF não contém números")

        # Completa com zeros à esquerda se necessário
        if len(cpf_limpo) < 11:
            cpf_limpo = cpf_limpo.zfill(11)

        # Trunca se tiver mais de 11 dígitos
        if len(cpf_limpo) > 11:
            cpf_limpo = cpf_limpo[:11]

        # Valida CPF
        if not ValidadorCPF.validar(cpf_limpo):
            raise ValueError("CPF inválido (dígitos verificadores não conferem)")

        return cpf_limpo

    @staticmethod
    def normalizar_matricula(valor: str | float | None) -> str:
        """
        Normaliza matrícula.

        Regras:
        - Converte para string
        - Remove espaços
        - NÃO adiciona zeros à esquerda
        - Preserva zeros à esquerda existentes

        Args:
            valor: Matrícula em qualquer formato

        Returns:
            Matrícula normalizada

        Raises:
            ValueError: Se a matrícula for vazia
        """
        if pd.isna(valor) or valor is None:
            raise ValueError("Matrícula não pode ser vazia")

        # Converte para string
        if isinstance(valor, (int, float)):
            valor_str = str(int(valor)) if isinstance(valor, float) else str(valor)
        else:
            valor_str = str(valor)

        # Remove espaços extras
        valor_normalizado = valor_str.strip()

        if len(valor_normalizado) == 0:
            raise ValueError("Matrícula vazia após normalização")

        return valor_normalizado

    @staticmethod
    def normalizar_data_admissao(valor: str | float | datetime | None) -> datetime:
        """
        Normaliza data de admissão com prioridade DD/MM/YYYY.

        Regras:
        - Prioridade: DD/MM/YYYY (formato Brasil)
        - Aceita DD-MM-YYYY, DD.MM.YYYY, YYYY-MM-DD
        - Aceita número serial do Excel
        - Extrai apenas a parte da data (ignora hora)

        Args:
            valor: Data em qualquer formato

        Returns:
            Datetime normalizado (sem hora)

        Raises:
            ValueError: Se a data for inválida ou vazia
        """
        if pd.isna(valor) or valor is None:
            raise ValueError("Data de admissão não pode ser vazia")

        try:
            # Caso 1: Já é datetime
            if isinstance(valor, datetime):
                return valor.replace(hour=0, minute=0, second=0, microsecond=0)

            # Caso 2: Número serial do Excel
            if isinstance(valor, (int, float)):
                if valor < 1:
                    raise ValueError(f"Data serial inválida: {valor}")
                data = ValidadorData.parse_serial(valor)
                if data is None:
                    raise ValueError(f"Erro ao converter serial: {valor}")
                return data.replace(hour=0, minute=0, second=0, microsecond=0)

            # Caso 3: String
            if isinstance(valor, str):
                valor_limpo = valor.strip()

                # Extrai apenas a parte da data (antes do espaço ou T)
                if " " in valor_limpo:
                    valor_limpo = valor_limpo.split(" ")[0]
                if "T" in valor_limpo:
                    valor_limpo = valor_limpo.split("T")[0]

                # Prioridade 1: DD/MM/YYYY
                if re.match(r"\d{2}/\d{2}/\d{4}", valor_limpo):
                    return datetime.strptime(valor_limpo, "%d/%m/%Y")  # noqa: DTZ007

                # Prioridade 2: DD-MM-YYYY
                if re.match(r"\d{2}-\d{2}-\d{4}", valor_limpo):
                    return datetime.strptime(valor_limpo, "%d-%m-%Y")  # noqa: DTZ007

                # Prioridade 3: DD.MM.YYYY
                if re.match(r"\d{2}\.\d{2}\.\d{4}", valor_limpo):
                    return datetime.strptime(valor_limpo, "%d.%m.%Y")  # noqa: DTZ007

                # Prioridade 4: YYYY-MM-DD (ISO)
                if re.match(r"\d{4}-\d{2}-\d{2}", valor_limpo):
                    return datetime.strptime(valor_limpo, "%Y-%m-%d")  # noqa: DTZ007

                # Fallback: parser automático
                try:
                    data = parser.parse(valor_limpo, fuzzy=False)
                    return data.replace(hour=0, minute=0, second=0, microsecond=0)
                except (ValueError, TypeError):
                    raise ValueError(f"Data em formato não reconhecido: '{valor_limpo}'")

            # Caso 4: Qualquer outra coisa
            raise ValueError(f"Tipo de dado não suportado para data: {type(valor)}")

        except ValueError as e:
            raise ValueError(f"Erro ao normalizar data: {e!s}")

    @staticmethod
    def formatar_data_brasil(data: datetime) -> str:
        """
        Formata data no padrão DD/MM/YYYY (Brasil).

        Args:
            data: Objeto datetime

        Returns:
            String no formato DD/MM/YYYY
        """
        return data.strftime("%d/%m/%Y")