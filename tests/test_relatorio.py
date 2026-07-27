"""Testes para o módulo de relatório."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime

import pandas as pd
import pytest

from src.models import (
    RegistroDivergente,
    RegistroErro,
    RegistroPlanilha,
    ResultadoComparacao,
)
from src.relatorio import GeradorRelatorio


class TestGeradorRelatorio:
    """Testes para o gerador de relatório."""

    def test_criar_gerador(self):
        """Testa criação do gerador."""
        gerador = GeradorRelatorio()
        assert gerador.resultado is None
        assert gerador.nome_arquivo == "relatorio_comparacao.xlsx"

    def test_definir_nome_arquivo(self):
        """Testa definição do nome do arquivo."""
        gerador = GeradorRelatorio()
        gerador.definir_nome_arquivo("teste.xlsx")
        assert gerador.nome_arquivo == "teste.xlsx"

    def test_definir_nome_arquivo_sem_extensao(self):
        """Testa definição do nome sem extensão."""
        gerador = GeradorRelatorio()
        gerador.definir_nome_arquivo("teste")
        assert gerador.nome_arquivo == "teste.xlsx"

    def test_definir_pasta_destino(self):
        """Testa definição da pasta de destino."""
        gerador = GeradorRelatorio()
        gerador.definir_pasta_destino("./temp")
        assert gerador.pasta_destino.name == "temp"

    def test_carregar_resultado(self):
        """Testa carregamento do resultado."""
        gerador = GeradorRelatorio()
        resultado = ResultadoComparacao(
            total_registros_a=10,
            total_registros_b=10,
        )
        gerador.carregar_resultado(resultado)
        assert gerador.resultado is not None
        assert gerador.resultado.total_registros_a == 10

    def test_gerar_relatorio_sem_resultado(self):
        """Testa geração sem resultado carregado."""
        gerador = GeradorRelatorio()
        with pytest.raises(ValueError, match="Nenhum resultado carregado"):
            gerador.gerar()

    def test_gerar_relatorio_vazio(self, tmp_path):
        """Testa geração de relatório vazio."""
        gerador = GeradorRelatorio()
        gerador.definir_pasta_destino(str(tmp_path))

        resultado = ResultadoComparacao()
        gerador.carregar_resultado(resultado)

        caminho = gerador.gerar()
        assert caminho.exists()
        assert caminho.suffix == ".xlsx"

        # Verifica se o arquivo foi criado
        df = pd.read_excel(caminho, sheet_name="Resumo")
        assert not df.empty

    def test_gerar_relatorio_com_dados(self, tmp_path):
        """Testa geração de relatório com dados."""
        gerador = GeradorRelatorio()
        gerador.definir_pasta_destino(str(tmp_path))

        # Cria resultado com dados
        resultado = ResultadoComparacao()

        # Adiciona registro na A
        registro = RegistroPlanilha(
            cpf="12345678909",
            matricula="001234",
            data_admissao="15/08/2023",
        )
        resultado.apenas_a.append(registro)

        # Adiciona divergência
        divergente = RegistroDivergente(
            cpf="98765432100",
            matricula="005678",
            data_a=datetime(2023, 8, 15),  # noqa: DTZ001
            data_b=datetime(2023, 8, 20),  # noqa: DTZ001
            diferenca_dias=5,
        )
        resultado.divergencias.append(divergente)

        # Adiciona erro
        erro = RegistroErro(
            linha=10,
            planilha="A",
            cpf="11122233344",
            erro="CPF inválido",
        )
        resultado.erros.append(erro)

        resultado.calcular_totais()
        gerador.carregar_resultado(resultado)

        caminho = gerador.gerar()
        assert caminho.exists()

        # Verifica abas
        xls = pd.ExcelFile(caminho)
        abas = xls.sheet_names
        assert "Divergências" in abas
        assert "Apenas na A" in abas
        assert "Apenas na B" in abas
        assert "Iguais" in abas
        assert "Erros" in abas
        assert "Resumo" in abas

        # Verifica dados da aba Divergências
        df = pd.read_excel(caminho, sheet_name="Divergências")
        assert len(df) == 1
        assert df.iloc[0]["Diferença (dias)"] == 5

        # Verifica dados da aba Erros
        df = pd.read_excel(caminho, sheet_name="Erros")
        assert len(df) == 1
        assert df.iloc[0]["Erro"] == "CPF inválido"