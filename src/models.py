"""Modelos de dados com validação automática."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.normalizers import NormalizadorDados


class RegistroPlanilha(BaseModel):
    """Modelo de um registro da planilha com normalização automática."""

    model_config = ConfigDict(extra="forbid")

    cpf: str = Field(..., description="CPF com 11 dígitos")
    matricula: str = Field(..., description="Matrícula normalizada")
    data_admissao: datetime = Field(..., description="Data de admissão normalizada")
    nome: str | None = Field(None, description="Nome do servidor")
    linha_original: int | None = Field(None, description="Número da linha na planilha")
    origem: str | None = Field(None, description="Origem do registro (A ou B)")
    dados_extras: dict[str, Any] | None = Field(
        default_factory=dict,
        description="Colunas extras da planilha"
    )

    @field_validator("cpf", mode="before")
    @classmethod
    def normalizar_cpf(cls, v):
        """Normaliza e valida CPF automaticamente."""
        return NormalizadorDados.normalizar_cpf(v)

    @field_validator("matricula", mode="before")
    @classmethod
    def normalizar_matricula(cls, v):
        """Normaliza matrícula automaticamente."""
        return NormalizadorDados.normalizar_matricula(v)

    @field_validator("data_admissao", mode="before")
    @classmethod
    def normalizar_data(cls, v):
        """Normaliza data automaticamente com prioridade DD/MM/YYYY."""
        return NormalizadorDados.normalizar_data_admissao(v)

    def data_admissao_brasil(self) -> str:
        """Retorna data no formato DD/MM/YYYY."""
        return NormalizadorDados.formatar_data_brasil(self.data_admissao)

    def cpf_mascarado(self) -> str:
        """Retorna CPF mascarado."""
        from src.validators import ValidadorCPF
        return ValidadorCPF.mascarar(self.cpf)

    def chave_comparacao(self) -> str:
        """Gera chave única para comparação (CPF + Matrícula + Nome)."""
        return f"{self.cpf}|{self.matricula}|{self.nome or ''}"

    def to_dict(self, mascarar_cpf: bool = False) -> dict[str, Any]:
        """Converte para dicionário."""
        dados = {
            "cpf": self.cpf_mascarado() if mascarar_cpf else self.cpf,
            "matricula": self.matricula,
            "data_admissao": self.data_admissao_brasil(),
        }
        if self.dados_extras:
            dados.update(self.dados_extras)
        return dados


class RegistroDivergente(BaseModel):
    """Modelo para registro com divergência de data ou nome."""

    model_config = ConfigDict(extra="forbid")

    cpf: str
    matricula: str
    nome_a: str
    nome_b: str
    data_a: datetime
    data_b: datetime
    diferenca_dias: int
    dados_extras_a: dict[str, Any] | None = None
    dados_extras_b: dict[str, Any] | None = None

    def data_a_brasil(self) -> str:
        return NormalizadorDados.formatar_data_brasil(self.data_a)

    def data_b_brasil(self) -> str:
        return NormalizadorDados.formatar_data_brasil(self.data_b)

    def cpf_mascarado(self) -> str:
        from src.validators import ValidadorCPF
        return ValidadorCPF.mascarar(self.cpf)

    def to_dict(self, mascarar_cpf: bool = False) -> dict[str, Any]:
        dados = {
            "cpf": self.cpf_mascarado() if mascarar_cpf else self.cpf,
            "matricula": self.matricula,
            "nome_a": self.nome_a or "",
            "nome_b": self.nome_b or "",
            "data_a": self.data_a_brasil(),
            "data_b": self.data_b_brasil(),
            "diferenca_dias": self.diferenca_dias,
        }
        if self.dados_extras_a:
            for k, v in self.dados_extras_a.items():
                dados[f"a_{k}"] = v
        if self.dados_extras_b:
            for k, v in self.dados_extras_b.items():
                dados[f"b_{k}"] = v
        return dados


class RegistroErro(BaseModel):
    """Modelo para registro com erro."""

    model_config = ConfigDict(extra="forbid")

    linha: int
    planilha: str
    cpf: str | None = None
    matricula: str | None = None
    data: str | datetime | None = None
    erro: str
    dados_extras: dict[str, Any] | None = None

    @field_validator("data", mode="before")
    @classmethod
    def normalizar_data_erro(cls, v):
        """Normaliza data do erro se for string."""
        if v is None or v == "":
            return None
        if isinstance(v, datetime):
            return v
        if isinstance(v, str):
            try:
                return NormalizadorDados.normalizar_data_admissao(v)
            except:  # noqa: E722
                return None
        return None

    def data_brasil(self) -> str | None:
        if self.data:
            return NormalizadorDados.formatar_data_brasil(self.data)
        return None

    def cpf_mascarado(self) -> str | None:
        if self.cpf:
            from src.validators import ValidadorCPF
            return ValidadorCPF.mascarar(self.cpf)
        return None

    def to_dict(self, mascarar_cpf: bool = False) -> dict[str, Any]:
        dados = {
            "linha": self.linha,
            "planilha": self.planilha,
            "cpf": self.cpf_mascarado() if mascarar_cpf and self.cpf else self.cpf,
            "matricula": self.matricula or "",
            "data": self.data_brasil() if self.data else "",
            "erro": self.erro,
        }
        if self.dados_extras:
            dados.update(self.dados_extras)
        return dados


class ResultadoComparacao(BaseModel):
    """Modelo com todos os resultados da comparação."""

    model_config = ConfigDict(extra="forbid")

    apenas_a: list[RegistroPlanilha] = Field(
        default_factory=list,
        description="Registros apenas na planilha A"
    )
    apenas_b: list[RegistroPlanilha] = Field(
        default_factory=list,
        description="Registros apenas na planilha B"
    )
    divergencias: list[RegistroDivergente] = Field(
        default_factory=list,
        description="Registros com datas diferentes"
    )
    iguais: list[RegistroPlanilha] = Field(
        default_factory=list,
        description="Registros idênticos"
    )
    erros: list[RegistroErro] = Field(
        default_factory=list,
        description="Registros com erros"
    )

    total_registros_a: int = 0
    total_registros_b: int = 0
    total_apenas_a: int = 0
    total_apenas_b: int = 0
    total_divergencias: int = 0
    total_iguais: int = 0
    total_erros: int = 0

    def calcular_totais(self) -> None:
        """Calcula os totais de cada categoria."""
        self.total_apenas_a = len(self.apenas_a)
        self.total_apenas_b = len(self.apenas_b)
        self.total_divergencias = len(self.divergencias)
        self.total_iguais = len(self.iguais)
        self.total_erros = len(self.erros)

    def to_dict(self, mascarar_cpf: bool = True) -> dict[str, Any]:
        return {
            "resumo": {
                "total_registros_a": self.total_registros_a,
                "total_registros_b": self.total_registros_b,
                "total_apenas_a": self.total_apenas_a,
                "total_apenas_b": self.total_apenas_b,
                "total_divergencias": self.total_divergencias,
                "total_iguais": self.total_iguais,
                "total_erros": self.total_erros,
            },
            "apenas_a": [r.to_dict(mascarar_cpf) for r in self.apenas_a],
            "apenas_b": [r.to_dict(mascarar_cpf) for r in self.apenas_b],
            "divergencias": [r.to_dict(mascarar_cpf) for r in self.divergencias],
            "iguais": [r.to_dict(mascarar_cpf) for r in self.iguais],
            "erros": [r.to_dict(mascarar_cpf) for r in self.erros],
        }