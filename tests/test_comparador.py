"""Testes para o módulo de comparação."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


from src.comparador import ComparadorPlanilhas


class TestComparadorPlanilhas:
    """Testes para o comparador de planilhas."""

    def test_criar_comparador(self):
        """Testa criação do comparador."""
        comparador = ComparadorPlanilhas()
        assert comparador.dados_a == {}
        assert comparador.dados_b == {}
        assert comparador.resultado is None

    def test_carregar_dados(self):
        """Testa carregamento de dados."""
        comparador = ComparadorPlanilhas()

        dados_a = [
            {
                "cpf": "12345678909",
                "matricula": "001234",
                "data_admissao": "15/08/2023",
                "linha_original": 2,
                "origem": "A",
            }
        ]

        dados_b = [
            {
                "cpf": "12345678909",
                "matricula": "001234",
                "data_admissao": "15/08/2023",
                "linha_original": 2,
                "origem": "B",
            }
        ]

        comparador.carregar_dados(dados_a, dados_b, [], [])

        assert len(comparador.dados_a) == 1
        assert len(comparador.dados_b) == 1
        assert comparador.resultado is not None
        assert comparador.resultado.total_registros_a == 1
        assert comparador.resultado.total_registros_b == 1

    def test_comparar_dados_iguais(self):
        """Testa comparação de dados idênticos."""
        comparador = ComparadorPlanilhas()

        dados_a = [
            {
                "cpf": "12345678909",
                "matricula": "001234",
                "data_admissao": "15/08/2023",
                "linha_original": 2,
                "origem": "A",
            }
        ]

        dados_b = [
            {
                "cpf": "12345678909",
                "matricula": "001234",
                "data_admissao": "15/08/2023",
                "linha_original": 2,
                "origem": "B",
            }
        ]

        comparador.carregar_dados(dados_a, dados_b, [], [])
        resultado = comparador.comparar()

        assert resultado.total_iguais == 1
        assert resultado.total_apenas_a == 0
        assert resultado.total_apenas_b == 0
        assert resultado.total_divergencias == 0
        assert resultado.total_erros == 0

    def test_comparar_dados_divergentes(self):
        """Testa comparação com divergência de data."""
        comparador = ComparadorPlanilhas()

        dados_a = [
            {
                "cpf": "12345678909",
                "matricula": "001234",
                "data_admissao": "15/08/2023",
                "linha_original": 2,
                "origem": "A",
            }
        ]

        dados_b = [
            {
                "cpf": "12345678909",
                "matricula": "001234",
                "data_admissao": "20/08/2023",
                "linha_original": 2,
                "origem": "B",
            }
        ]

        comparador.carregar_dados(dados_a, dados_b, [], [])
        resultado = comparador.comparar()

        assert resultado.total_iguais == 0
        assert resultado.total_apenas_a == 0
        assert resultado.total_apenas_b == 0
        assert resultado.total_divergencias == 1
        assert resultado.total_erros == 0

        # Verifica a diferença em dias
        divergencia = resultado.divergencias[0]
        assert divergencia.diferenca_dias == 5

    def test_comparar_dados_apenas_a(self):
        """Testa comparação com dados apenas na A."""
        comparador = ComparadorPlanilhas()

        dados_a = [
            {
                "cpf": "12345678909",
                "matricula": "001234",
                "data_admissao": "15/08/2023",
                "linha_original": 2,
                "origem": "A",
            }
        ]

        dados_b = []

        comparador.carregar_dados(dados_a, dados_b, [], [])
        resultado = comparador.comparar()

        assert resultado.total_iguais == 0
        assert resultado.total_apenas_a == 1
        assert resultado.total_apenas_b == 0
        assert resultado.total_divergencias == 0

    def test_comparar_dados_apenas_b(self):
        """Testa comparação com dados apenas na B."""
        comparador = ComparadorPlanilhas()

        dados_a = []

        dados_b = [
            {
                "cpf": "12345678909",
                "matricula": "001234",
                "data_admissao": "15/08/2023",
                "linha_original": 2,
                "origem": "B",
            }
        ]

        comparador.carregar_dados(dados_a, dados_b, [], [])
        resultado = comparador.comparar()

        assert resultado.total_iguais == 0
        assert resultado.total_apenas_a == 0
        assert resultado.total_apenas_b == 1
        assert resultado.total_divergencias == 0

    def test_comparar_com_erros(self):
        """Testa comparação com erros."""
        comparador = ComparadorPlanilhas()

        dados_a = []
        dados_b = []

        erros_a = [
            {
                "linha": 2,
                "cpf": "12345678900",
                "matricula": "001234",
                "data": "15/08/2023",  # Mantém string, será tratado pelo modelo
                "erro": "CPF inválido",
            }
        ]

        comparador.carregar_dados(dados_a, dados_b, erros_a, [])
        resultado = comparador.comparar()

        assert resultado.total_erros == 1
        assert resultado.erros[0].erro == "CPF inválido"

    def test_obter_resumo(self):
        """Testa obtenção do resumo."""
        comparador = ComparadorPlanilhas()

        dados_a = [
            {
                "cpf": "12345678909",
                "matricula": "001234",
                "data_admissao": "15/08/2023",
                "linha_original": 2,
                "origem": "A",
            },
            {
                "cpf": "98765432100",
                "matricula": "005678",
                "data_admissao": "20/01/2021",
                "linha_original": 3,
                "origem": "A",
            },
        ]

        dados_b = [
            {
                "cpf": "12345678909",
                "matricula": "001234",
                "data_admissao": "15/08/2023",
                "linha_original": 2,
                "origem": "B",
            }
        ]

        comparador.carregar_dados(dados_a, dados_b, [], [])
        comparador.comparar()
        resumo = comparador.obter_resumo()

        assert resumo["total_registros_a"] == 2
        assert resumo["total_registros_b"] == 1
        assert resumo["total_apenas_a"] == 1
        assert resumo["total_apenas_b"] == 0
        assert resumo["total_divergencias"] == 0
        assert resumo["total_iguais"] == 1