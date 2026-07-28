"""Módulo de validação de dados."""

import re
from datetime import datetime


class ValidadorCPF:
    """Validador de CPF com dígitos verificadores."""

    @staticmethod
    def validar(cpf: str | None) -> bool:
        """
        Valida CPF com dígitos verificadores.

        Args:
            cpf: String contendo o CPF (com ou sem máscara)

        Returns:
            True se o CPF for válido, False caso contrário
        """
        # Verifica se o valor é None ou vazio
        if cpf is None or cpf == "":
            return False

        # Remove caracteres não numéricos
        cpf_limpo = re.sub(r"[^0-9]", "", str(cpf))

        # Verifica se tem 11 dígitos
        if len(cpf_limpo) != 11:
            return False

        # Verifica se todos os dígitos são iguais (CPF inválido conhecido)
        if len(set(cpf_limpo)) == 1:
            return False

        # Cálculo do primeiro dígito verificador
        soma = sum(int(cpf_limpo[i]) * (10 - i) for i in range(9))
        digito1 = (soma * 10) % 11
        if digito1 == 10:
            digito1 = 0

        # Cálculo do segundo dígito verificador
        soma = sum(int(cpf_limpo[i]) * (11 - i) for i in range(10))
        digito2 = (soma * 10) % 11
        if digito2 == 10:
            digito2 = 0

        return int(cpf_limpo[9]) == digito1 and int(cpf_limpo[10]) == digito2

    @staticmethod
    def sanitizar(cpf: str) -> str:
        """Remove máscara do CPF, mantendo apenas números."""
        if cpf is None:
            return ""
        return re.sub(r"[^0-9]", "", str(cpf))

    @staticmethod
    def mascarar(cpf: str) -> str:
        """
        Aplica máscara de segurança ao CPF.

        Args:
            cpf: CPF com 11 dígitos

        Returns:
            CPF mascarado no formato ***.123.456-**
        """
        cpf_limpo = ValidadorCPF.sanitizar(cpf)
        if len(cpf_limpo) == 11:
            return f"***.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-**"
        return "***.***.***-**"


class ValidadorData:
    """Validador de datas com suporte a múltiplos formatos."""

    FORMATOS = [  # noqa: RUF012
        r"\d{2}/\d{2}/\d{4}",  # DD/MM/YYYY
        r"\d{2}-\d{2}-\d{4}",  # DD-MM-YYYY
        r"\d{2}\.\d{2}\.\d{4}",  # DD.MM.YYYY
        r"\d{4}-\d{2}-\d{2}",  # YYYY-MM-DD
    ]

    @staticmethod
    def validar_formato(valor: str) -> bool:
        """Verifica se a data está em um formato reconhecido."""
        if not valor:
            return False
        for formato in ValidadorData.FORMATOS:
            if re.match(formato, valor.strip()):
                return True
        return False

    @staticmethod
    def parse_serial(serial: float) -> datetime | None:
        """
        Converte número serial do Excel para datetime.

        Args:
            serial: Número serial do Excel (dias desde 1899-12-30)

        Returns:
            Objeto datetime ou None se inválido
        """
        try:
            if serial < 1:
                return None
            from datetime import timedelta

            # Excel serial: 1 = 1900-01-01
            # Ajuste: 1899-12-30 + serial dias
            base = datetime(1899, 12, 30)  # noqa: DTZ001
            return base + timedelta(days=float(serial))
        except (ValueError, TypeError, OverflowError):
            return None


class ValidadorMatricula:
    """Validador de matrícula."""

    @staticmethod
    def validar(valor: str | None) -> bool:
        """
        Valida se a matrícula não está vazia após normalização.

        Args:
            valor: Matrícula a ser validada

        Returns:
            True se válida, False caso contrário
        """
        if valor is None:
            return False
        return str(valor).strip()

    @staticmethod
    def normalizar(valor: str | float | None) -> str:
        """
        Normaliza a matrícula removendo espaços.

        Args:
            valor: Matrícula a ser normalizada

        Returns:
            Matrícula normalizada
        """
        if valor is None:
            return ""
        valor_str = str(valor).strip()
        # Remove espaços internos extras
        return " ".join(valor_str.split())