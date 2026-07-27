"""Testes para o módulo de normalização."""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from datetime import datetime
from src.normalizers import NormalizadorDados


class TestNormalizadorDados:
    """Testes para o normalizador de dados."""

    def test_normalizar_cpf_valido(self):
        """Testa normalização de CPF válido."""
        resultado = NormalizadorDados.normalizar_cpf("12345678909")
        assert resultado == "12345678909"

    def test_normalizar_cpf_com_mascara(self):
        """Testa normalização de CPF com máscara."""
        resultado = NormalizadorDados.normalizar_cpf("123.456.789-09")
        assert resultado == "12345678909"

    def test_normalizar_cpf_com_zeros_faltando(self):
        """Testa normalização de CPF com zeros faltando."""
        # Usando CPF 01234567890 que é válido com zeros
        resultado = NormalizadorDados.normalizar_cpf("1234567890")
        assert resultado == "01234567890"
        assert len(resultado) == 11

    def test_normalizar_cpf_invalido(self):
        """Testa normalização de CPF inválido."""
        with pytest.raises(ValueError, match="CPF inválido"):
            NormalizadorDados.normalizar_cpf("12345678900")

    def test_normalizar_cpf_digitos_iguais(self):
        """Testa normalização de CPF com dígitos iguais."""
        with pytest.raises(ValueError, match="CPF inválido"):
            NormalizadorDados.normalizar_cpf("11111111111")

    def test_normalizar_cpf_vazio(self):
        """Testa normalização de CPF vazio."""
        with pytest.raises(ValueError, match="CPF não pode ser vazio"):
            NormalizadorDados.normalizar_cpf(None)  # type: ignore

    def test_normalizar_matricula_com_numero(self):
        """Testa normalização de matrícula como número."""
        resultado = NormalizadorDados.normalizar_matricula(12345)
        assert resultado == "12345"

    def test_normalizar_matricula_com_texto(self):
        """Testa normalização de matrícula como texto."""
        resultado = NormalizadorDados.normalizar_matricula("ABC-123")
        assert resultado == "ABC-123"

    def test_normalizar_matricula_com_zeros(self):
        """Testa normalização de matrícula com zeros (preservar)."""
        resultado = NormalizadorDados.normalizar_matricula("001234")
        assert resultado == "001234"  # Mantém zeros

    def test_normalizar_matricula_vazia(self):
        """Testa normalização de matrícula vazia."""
        with pytest.raises(ValueError, match="Matrícula vazia após normalização"):
            NormalizadorDados.normalizar_matricula("")

    def test_normalizar_data_dd_mm_yyyy(self):
        """Testa normalização de data DD/MM/YYYY."""
        data = NormalizadorDados.normalizar_data_admissao("15/08/2023")
        assert data.year == 2023
        assert data.month == 8
        assert data.day == 15

    def test_normalizar_data_dd_mm_yyyy_alternativo(self):
        """Testa normalização de data DD-MM-YYYY."""
        data = NormalizadorDados.normalizar_data_admissao("15-08-2023")
        assert data.year == 2023
        assert data.month == 8
        assert data.day == 15

    def test_normalizar_data_iso(self):
        """Testa normalização de data YYYY-MM-DD."""
        data = NormalizadorDados.normalizar_data_admissao("2023-08-15")
        assert data.year == 2023
        assert data.month == 8
        assert data.day == 15

    def test_normalizar_data_serial_excel(self):
        """Testa normalização de serial Excel."""
        data = NormalizadorDados.normalizar_data_admissao(43831)  # 01/01/2020
        assert data.year == 2020
        assert data.month == 1
        assert data.day == 1

    def test_normalizar_data_com_hora(self):
        """Testa normalização de data com hora (ignorar hora)."""
        data = NormalizadorDados.normalizar_data_admissao("15/08/2023 14:30:00")
        assert data.year == 2023
        assert data.month == 8
        assert data.day == 15
        assert data.hour == 0
        assert data.minute == 0
        assert data.second == 0

    def test_normalizar_data_invalida(self):
        """Testa normalização de data inválida."""
        with pytest.raises(ValueError, match="Erro ao normalizar data"):
            NormalizadorDados.normalizar_data_admissao("31/13/2023")

    def test_normalizar_data_vazia(self):
        """Testa normalização de data vazia."""
        with pytest.raises(ValueError, match="Data de admissão não pode ser vazia"):
            NormalizadorDados.normalizar_data_admissao(None)  # type: ignore

    def test_formatar_data_brasil(self):
        """Testa formatação de data no padrão Brasil."""
        data = datetime(2023, 8, 15)
        resultado = NormalizadorDados.formatar_data_brasil(data)
        assert resultado == "15/08/2023"