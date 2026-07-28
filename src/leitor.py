"""Módulo para leitura de planilhas Excel."""

import re
from pathlib import Path
from typing import Any

import pandas as pd

from src.config import Config
from src.validators import ValidadorCPF


class LeitorPlanilhas:
    """Classe para leitura e validação de planilhas Excel."""

    # Palavras-chave para identificar cabeçalhos (case insensitive)
    KEYWORDS_CPF = ["cpf", "cpf/cnpj", "documento", "doc"]  # noqa: RUF012
    KEYWORDS_MATRICULA = ["matrícula", "matricula", "registro", "id", "código", "codigo", "número", "numero", "MATRIC", "matric"]  # noqa: RUF012
    KEYWORDS_DATA = [  # noqa: RUF012
        "data de admissão",
        "data admissão",
        "data adm",
        "admissão",
        "admissao",
        "ADMISSÃO",
        "ADMISSAO",
        "data de entrada",
        "data entrada",
    ]

    def __init__(self):
        self.arquivo: Path | None = None
        self.abas: list[str] = []
        self.aba_selecionada: str | None = None
        self.cabecalhos: dict[str, Any] = {}
        self.dados: list[dict] = []
        self.erros: list[dict] = []
        self.linha_cabecalho: int | None = None
        self.df_raw = None

    def carregar_arquivo(self, caminho: str, aba: str | None = None) -> bool:
        """
        Carrega um arquivo Excel.

        Args:
            caminho: Caminho do arquivo
            aba: Nome da aba a ser carregada (opcional)

        Returns:
            True se carregou com sucesso, False caso contrário
        """
        try:
            self.arquivo = Path(caminho)
            if not self.arquivo.exists():
                raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

            # Verifica extensão para usar o engine correto
            extensao = self.arquivo.suffix.lower()

            # Lista todas as abas
            try:
                if extensao in ['.xlsx', '.xlsm']:
                    xls = pd.ExcelFile(self.arquivo, engine='openpyxl')
                elif extensao == '.xls':
                    try:
                        xls = pd.ExcelFile(self.arquivo, engine='xlrd')
                    except ImportError:
                        xls = pd.ExcelFile(self.arquivo, engine='openpyxl')
                else:
                    xls = pd.ExcelFile(self.arquivo, engine='openpyxl')

            except Exception:  # noqa: BLE001
                try:
                    xls = pd.ExcelFile(self.arquivo)
                except Exception as e:  # noqa: BLE001
                    raise ValueError(f"Erro ao ler arquivo: {e!s}")

            self.abas = xls.sheet_names

            if not self.abas:
                raise ValueError("Arquivo não contém nenhuma aba")

            # Seleciona a aba
            if aba:
                if aba not in self.abas:
                    raise ValueError(f"Aba '{aba}' não encontrada. Abas disponíveis: {self.abas}")
                self.aba_selecionada = aba
            else:
                if len(self.abas) == 1:
                    self.aba_selecionada = self.abas[0]
                else:
                    self.aba_selecionada = None

            return True

        except Exception as e:  # noqa: BLE001
            raise ValueError(f"Erro ao carregar arquivo: {e!s}")

    def listar_abas(self) -> list[str]:
        """Retorna a lista de abas disponíveis."""
        return self.abas

    def selecionar_aba(self, nome_aba: str) -> bool:
        """
        Seleciona uma aba para processamento.

        Args:
            nome_aba: Nome da aba

        Returns:
            True se selecionou com sucesso
        """
        if nome_aba not in self.abas:
            raise ValueError(f"Aba '{nome_aba}' não encontrada. Abas disponíveis: {self.abas}")
        self.aba_selecionada = nome_aba
        return True

    def identificar_cabecalhos(self) -> tuple[bool, dict[str, Any]]:
        """
        Identifica a linha de cabeçalho e mapeia as colunas.

        Returns:
            Tuple com (sucesso, dict com mapeamento)
        """
        if not self.arquivo or not self.aba_selecionada:
            raise ValueError("Arquivo ou aba não selecionada")

        # Lê o arquivo sem cabeçalho para buscar a linha correta
        self.df_raw = pd.read_excel(
            self.arquivo,
            sheet_name=self.aba_selecionada,
            header=None,
            dtype=str,
        )

        # Procura pela linha de cabeçalho (até o limite configurado)
        limite = Config.MAX_LINHAS_BUSCA_CABECALHO
        self.linha_cabecalho = None

        # Converte todas as células para string minúscula para comparação
        for idx in range(min(limite, len(self.df_raw))):
            # Pega a linha e converte para string, tratando NaN
            linha = self.df_raw.iloc[idx]
            # Converte cada célula para string, substituindo NaN por string vazia
            linha_str = []
            for cell in linha:
                if pd.isna(cell):
                    linha_str.append("")
                else:
                    linha_str.append(str(cell).lower().strip())
            
            # Concatena todas as células da linha para procurar as palavras-chave
            linha_texto = " ".join(linha_str)

            # Verifica se contém as palavras-chave
            tem_cpf = any(k in linha_texto for k in self.KEYWORDS_CPF)
            tem_matricula = any(k in linha_texto for k in self.KEYWORDS_MATRICULA)
            tem_data = any(k in linha_texto for k in self.KEYWORDS_DATA)

            if tem_cpf and tem_matricula and tem_data:
                self.linha_cabecalho = idx
                break

        if self.linha_cabecalho is None:
            return False, {}

        # Mapeia as colunas
        cabecalho = self.df_raw.iloc[self.linha_cabecalho].astype(str).str.lower().str.strip()
        self.cabecalhos = {}

        for idx, col in enumerate(cabecalho):
            col_str = str(col).lower().strip()
            # Verifica se é CPF
            if any(k in col_str for k in self.KEYWORDS_CPF):
                self.cabecalhos["cpf"] = idx
            # Verifica se é Matrícula
            elif any(k in col_str for k in self.KEYWORDS_MATRICULA):
                self.cabecalhos["matricula"] = idx
            # Verifica se é Data de Admissão
            elif any(k in col_str for k in self.KEYWORDS_DATA):
                self.cabecalhos["data_admissao"] = idx
            # Colunas extras
            else:
                if "extras" not in self.cabecalhos:
                    self.cabecalhos["extras"] = []
                self.cabecalhos["extras"].append(idx)

        # Verifica se encontrou todas as colunas obrigatórias
        obrigatorias = ["cpf", "matricula", "data_admissao"]
        for col in obrigatorias:
            if col not in self.cabecalhos:
                return False, self.cabecalhos

        return True, self.cabecalhos

    def processar_dados(self, origem: str = "A") -> tuple[list[dict], list[dict]]:
        """
        Processa os dados da planilha, criando registros válidos.

        Args:
            origem: Identificador da origem ("A" ou "B")

        Returns:
            Tuple com (lista de registros válidos, lista de erros)
        """
        if not self.arquivo or not self.aba_selecionada:
            raise ValueError("Arquivo ou aba não selecionada")

        if self.linha_cabecalho is None:
            self.identificar_cabecalhos()

        if self.linha_cabecalho is None:
            raise ValueError("Cabeçalhos não identificados")

        # Lê os dados a partir da linha após o cabeçalho
        df = pd.read_excel(
            self.arquivo,
            sheet_name=self.aba_selecionada,
            header=self.linha_cabecalho,
            dtype=str,
        )

        self.dados = []
        self.erros = []

        for idx, row in df.iterrows():
            try:
                # Extrai os dados
                cpf = row.iloc[self.cabecalhos["cpf"]] if self.cabecalhos["cpf"] < len(row) else ""
                matricula = row.iloc[self.cabecalhos["matricula"]] if self.cabecalhos["matricula"] < len(row) else ""
                data = row.iloc[self.cabecalhos["data_admissao"]] if self.cabecalhos["data_admissao"] < len(row) else ""

                # Converte para string e trata NaN
                cpf_str = str(cpf) if not pd.isna(cpf) else ""
                matricula_str = str(matricula) if not pd.isna(matricula) else ""
                data_str = str(data) if not pd.isna(data) else ""

                # Remove espaços
                cpf_limpo = cpf_str.strip()
                matricula_limpa = matricula_str.strip()
                data_limpa = data_str.strip()

                # VERIFICAÇÃO: Se todos os campos obrigatórios estiverem vazios ou forem "nan", pula
                if (not cpf_limpo or cpf_limpo.lower() == "nan") and \
                   (not matricula_limpa or matricula_limpa.lower() == "nan") and \
                   (not data_limpa or data_limpa.lower() == "nan"):
                    continue  # Pula linhas em branco

                # Se CPF está vazio
                if not cpf_limpo or cpf_limpo.lower() == "nan":
                    self.erros.append({
                        "linha": idx + 2,
                        "cpf": None,
                        "matricula": matricula_limpa if matricula_limpa.lower() != "nan" else "",
                        "data": data_limpa if data_limpa.lower() != "nan" else "",
                        "erro": "CPF vazio",
                    })
                    continue

                # Coleta dados extras
                dados_extras = {}
                if "extras" in self.cabecalhos:
                    for col_idx in self.cabecalhos["extras"]:
                        if col_idx < len(row):
                            col_name = df.columns[col_idx] if col_idx < len(df.columns) else f"col_{col_idx}"
                            valor = row.iloc[col_idx]
                            if not pd.isna(valor):
                                valor_str = str(valor).strip()
                                if valor_str and valor_str.lower() != "nan":
                                    dados_extras[str(col_name)] = valor_str

                # Valida CPF
                cpf_limpo_num = re.sub(r"[^0-9]", "", cpf_limpo)
                cpf_valido = ValidadorCPF.validar(cpf_limpo_num) if cpf_limpo_num else False

                if not cpf_limpo_num:
                    self.erros.append({
                        "linha": idx + 2,
                        "cpf": cpf_limpo,
                        "matricula": matricula_limpa if matricula_limpa.lower() != "nan" else "",
                        "data": data_limpa if data_limpa.lower() != "nan" else "",
                        "erro": "CPF vazio após sanitização",
                    })
                    continue

                if not cpf_valido:
                    self.erros.append({
                        "linha": idx + 2,
                        "cpf": cpf_limpo,
                        "matricula": matricula_limpa if matricula_limpa.lower() != "nan" else "",
                        "data": data_limpa if data_limpa.lower() != "nan" else "",
                        "erro": f"CPF inválido (dígitos verificadores não conferem): {cpf_limpo}",
                    })
                    continue

                # Registro válido
                registro = {
                    "cpf": cpf_limpo_num,
                    "matricula": matricula_limpa if matricula_limpa.lower() != "nan" else "",
                    "data_admissao": data_limpa if data_limpa.lower() != "nan" else "",
                    "linha_original": idx + 2,
                    "origem": origem,
                    "dados_extras": dados_extras,
                    "valido": True,
                }

                self.dados.append(registro)

            except Exception as e:  # noqa: BLE001
                # Registra o erro mas continua
                cpf_val = row.iloc[self.cabecalhos["cpf"]] if self.cabecalhos["cpf"] < len(row) else ""
                mat_val = row.iloc[self.cabecalhos["matricula"]] if self.cabecalhos["matricula"] < len(row) else ""
                data_val = row.iloc[self.cabecalhos["data_admissao"]] if self.cabecalhos["data_admissao"] < len(row) else ""

                cpf_str = str(cpf_val) if not pd.isna(cpf_val) else ""
                mat_str = str(mat_val) if not pd.isna(mat_val) else ""
                data_str = str(data_val) if not pd.isna(data_val) else ""

                self.erros.append({
                    "linha": idx + 2,
                    "cpf": cpf_str.strip() if cpf_str.strip() and cpf_str.strip().lower() != "nan" else None,
                    "matricula": mat_str.strip() if mat_str.strip() and mat_str.strip().lower() != "nan" else None,
                    "data": data_str.strip() if data_str.strip() and data_str.strip().lower() != "nan" else None,
                    "erro": str(e),
                })

        return self.dados, self.erros

    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas do processamento."""
        return {
            "total_registros": len(self.dados),
            "total_erros": len(self.erros),
            "aba": self.aba_selecionada,
            "cabecalho_linha": self.linha_cabecalho,
        }