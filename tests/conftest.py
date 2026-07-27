"""Configurações compartilhadas para os testes."""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para importações
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest


@pytest.fixture
def cpf_valido():
    """Retorna um CPF válido para testes."""
    return "12345678909"


@pytest.fixture
def cpf_invalido():
    """Retorna um CPF inválido para testes."""
    return "12345678900"


@pytest.fixture
def cpf_com_mascara():
    """Retorna um CPF com máscara para testes."""
    return "123.456.789-09"


@pytest.fixture
def data_valida():
    """Retorna uma data válida para testes."""
    return "15/08/2023"


@pytest.fixture
def matricula_com_zeros():
    """Retorna uma matrícula com zeros à esquerda."""
    return "001234"