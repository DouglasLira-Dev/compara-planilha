"""Testes para o módulo de leitor."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import pytest

from src.leitor import LeitorPlanilhas


class TestLeitorPlanilhas:
    """Testes para o leitor de planilhas."""

    def test_criar_leitor(self):
        """Testa criação do leitor."""
        leitor = LeitorPlanilhas()
        assert leitor.abas == []
        assert leitor.dados == []
        assert leitor.erros == []

    def test_keywords_definidas(self):
        """Testa se as keywords estão definidas."""
        assert len(LeitorPlanilhas.KEYWORDS_CPF) > 0
        assert len(LeitorPlanilhas.KEYWORDS_MATRICULA) > 0
        assert len(LeitorPlanilhas.KEYWORDS_DATA) > 0

    def test_carregar_arquivo_inexistente(self):
        """Testa carregamento de arquivo inexistente."""
        leitor = LeitorPlanilhas()
        with pytest.raises(ValueError, match="Arquivo não encontrado"):
            leitor.carregar_arquivo("arquivo_inexistente.xlsx")

    def test_criar_arquivo_excel_temporario(self, tmp_path):
        """Testa criação e leitura de arquivo Excel."""
        # Cria arquivo Excel temporário
        caminho = tmp_path / "teste.xlsx"
        df = pd.DataFrame({
            "CPF": ["12345678909", "98765432100"],
            "Matrícula": ["001234", "005678"],
            "Data de Admissão": ["15/08/2023", "20/01/2021"],
            "Nome": ["João", "Maria"],
        })
        df.to_excel(caminho, index=False)

        leitor = LeitorPlanilhas()
        leitor.carregar_arquivo(str(caminho))

        assert len(leitor.abas) == 1
        assert leitor.abas[0] == "Sheet1"

        # Seleciona a aba
        leitor.selecionar_aba("Sheet1")

        # Identifica cabeçalhos
        sucesso, cabecalhos = leitor.identificar_cabecalhos()
        assert sucesso is True
        assert "cpf" in cabecalhos
        assert "matricula" in cabecalhos
        assert "data_admissao" in cabecalhos

        # Processa dados
        dados, erros = leitor.processar_dados("A")
        assert len(dados) == 2
        assert len(erros) == 0

        # Verifica dados
        assert dados[0]["cpf"] == "12345678909"
        assert dados[0]["matricula"] == "001234"
        assert dados[1]["cpf"] == "98765432100"

    def test_carregar_com_cpf_invalido(self, tmp_path):
        """Testa carregamento com CPF inválido."""
        caminho = tmp_path / "teste_invalido.xlsx"
        df = pd.DataFrame({
            "CPF": ["12345678900", "98765432100"],  # CPF inválido
            "Matrícula": ["001234", "005678"],
            "Data de Admissão": ["15/08/2023", "20/01/2021"],
        })
        df.to_excel(caminho, index=False)

        leitor = LeitorPlanilhas()
        leitor.carregar_arquivo(str(caminho))
        leitor.selecionar_aba("Sheet1")
        leitor.identificar_cabecalhos()

        dados, erros = leitor.processar_dados("A")
        assert len(dados) == 1  # Apenas o CPF válido
        assert len(erros) == 1  # O CPF inválido gerou erro

    def test_carregar_com_linhas_em_branco(self, tmp_path):
        """Testa carregamento com linhas em branco."""
        caminho = tmp_path / "teste_branco.xlsx"
        df = pd.DataFrame({
            "CPF": ["12345678909", "", "98765432100"],
            "Matrícula": ["001234", "", "005678"],
            "Data de Admissão": ["15/08/2023", "", "20/01/2021"],
        })
        df.to_excel(caminho, index=False)

        leitor = LeitorPlanilhas()
        leitor.carregar_arquivo(str(caminho))
        leitor.selecionar_aba("Sheet1")
        leitor.identificar_cabecalhos()

        dados, erros = leitor.processar_dados("A")
        # Linha em branco deve ser ignorada
        assert len(dados) == 2
        assert len(erros) == 0