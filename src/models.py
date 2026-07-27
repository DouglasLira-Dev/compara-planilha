"""Modelos de dados com validação automática."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from src.normalizers import NormalizadorDados


class RegistroPlanilha(BaseModel):
    """Modelo de um registro da planilha com normalização automática."""

    cpf: str = Field(..., description="CPF com 11 dígitos")
    matricula: str = Field(..., description="Matrícula normalizada")
    data_admissao: datetime = Field(..., description="Data de admissão normalizada")
    linha_original: Optional[int] = Field(None, description="Número da linha na planilha")
    origem: Optional[str] = Field(None, description="Origem do registro (A ou B)")

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
        """Gera chave única para comparação (CPF + Matrícula)."""
        return f"{self.cpf}|{self.matricula}"

    class Config:
        """Configuração do modelo."""

        extra = "forbid"  # Não permite campos extras


class RegistroDivergente(BaseModel):
    """Modelo para registro com divergência de data."""

    cpf: str
    matricula: str
    data_a: datetime
    data_b: datetime
    diferenca_dias: int

    def data_a_brasil(self) -> str:
        return NormalizadorDados.formatar_data_brasil(self.data_a)

    def data_b_brasil(self) -> str:
        return NormalizadorDados.formatar_data_brasil(self.data_b)


class RegistroErro(BaseModel):
    """Modelo para registro com erro."""

    linha: int
    planilha: str
    cpf: Optional[str] = None
    matricula: Optional[str] = None
    data: Optional[datetime] = None
    erro: str

    def data_brasil(self) -> Optional[str]:
        if self.data:
            return NormalizadorDados.formatar_data_brasil(self.data)
        return None