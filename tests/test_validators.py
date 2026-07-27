"""Testes para o módulo de validadores."""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from src.validators import ValidadorCPF, ValidadorData, ValidadorMatricula


class TestValidadorCPF:
    """Testes para o validador de CPF."""

    def test_validar_cpf_valido(self):
        """Testa validação de CPF válido."""
        assert ValidadorCPF.validar("12345678909") is True

    def test_validar_cpf_com_mascara(self):
        """Testa validação de CPF com máscara."""
        assert ValidadorCPF.validar("123.456.789-09") is True

    def test_validar_cpf_invalido(self):
        """Testa validação de CPF inválido."""
        assert ValidadorCPF.validar("12345678900") is False

    def test_validar_cpf_digitos_iguais(self):
        """Testa validação de CPF com todos dígitos iguais."""
        assert ValidadorCPF.validar("11111111111") is False

    def test_validar_cpf_tamanho_incorreto(self):
        """Testa validação de CPF com tamanho incorreto."""
        assert ValidadorCPF.validar("123456789") is False
        assert ValidadorCPF.validar("123456789012") is False

    def test_validar_cpf_vazio(self):
        """Testa validação de CPF vazio."""
        assert ValidadorCPF.validar("") is False
        assert ValidadorCPF.validar(None) is False

    def test_sanitizar_cpf(self):
        """Testa sanitização do CPF."""
        assert ValidadorCPF.sanitizar("123.456.789-09") == "12345678909"
        assert ValidadorCPF.sanitizar("12345678909") == "12345678909"

    def test_mascarar_cpf(self):
        """Testa mascaramento do CPF."""
        assert ValidadorCPF.mascarar("12345678909") == "***.456.789-**"
        assert ValidadorCPF.mascarar("") == "***.***.***-**"


class TestValidadorData:
    """Testes para o validador de data."""

    def test_validar_formato_dd_mm_yyyy(self):
        """Testa validação do formato DD/MM/YYYY."""
        assert ValidadorData.validar_formato("15/08/2023") is True

    def test_validar_formato_dd_mm_yyyy_alternativo(self):
        """Testa validação do formato DD-MM-YYYY."""
        assert ValidadorData.validar_formato("15-08-2023") is True

    def test_validar_formato_yyyy_mm_dd(self):
        """Testa validação do formato YYYY-MM-DD."""
        assert ValidadorData.validar_formato("2023-08-15") is True

    def test_validar_formato_invalido(self):
        """Testa validação de formato inválido."""
        assert ValidadorData.validar_formato("15/08/23") is False
        assert ValidadorData.validar_formato("2023/08/15") is False

    def test_parse_serial_excel(self):
        """Testa conversão de serial Excel para data."""
        from datetime import datetime

        data = ValidadorData.parse_serial(43831)  # 01/01/2020
        assert data is not None
        if data:
            assert data.year == 2020
            assert data.month == 1
            assert data.day == 1

    def test_parse_serial_invalido(self):
        """Testa conversão de serial inválido."""
        assert ValidadorData.parse_serial(0) is None
        assert ValidadorData.parse_serial(-1) is None


class TestValidadorMatricula:
    """Testes para o validador de matrícula."""

    def test_validar_matricula_valida(self):
        """Testa validação de matrícula válida."""
        assert ValidadorMatricula.validar("12345") is True
        assert ValidadorMatricula.validar("ABC123") is True

    def test_validar_matricula_vazia(self):
        """Testa validação de matrícula vazia."""
        assert ValidadorMatricula.validar("") is False
        assert ValidadorMatricula.validar("   ") is False
        assert ValidadorMatricula.validar(None) is False

    def test_normalizar_matricula(self):
        """Testa normalização da matrícula."""
        assert ValidadorMatricula.normalizar("  12345  ") == "12345"
        assert ValidadorMatricula.normalizar("ABC-123") == "ABC-123"
        assert ValidadorMatricula.normalizar("001234") == "001234"