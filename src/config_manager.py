"""Gerenciador de configurações persistente."""

import json
from pathlib import Path
from typing import Any


class ConfigManager:
    """Gerencia as configurações do usuário em arquivo JSON."""

    CONFIG_FILE = "config.json"

    def __init__(self):
        self.config_file = Path(__file__).parent.parent / self.CONFIG_FILE
        self.defaults = {
            "relatorio": {
                "nome": "relatorio_comparacao.xlsx",
                "pasta": "",
                "colunas": [
                    "CPF",
                    "Matrícula",
                    "Data de Admissão",
                    "Nome",
                    "Departamento",
                    "Cargo",
                    "Telefone",
                    "Email"
                ],
                "abas": [
                    "Divergências",
                    "Apenas na A",
                    "Apenas na B",
                    "Iguais",
                    "Erros",
                    "Resumo"
                ],
                "ordenacao": "cpf"
            },
            "processamento": {
                "max_registros": 0,
                "max_linhas_cabecalho": 10
            }
        }
        self._config: dict[str, Any] | None = None
        self.carregar()

    def carregar(self) -> dict[str, Any]:
        """Carrega as configurações do arquivo."""
        if self._config is not None:
            return self._config

        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
                # Garante que todas as chaves existem
                self._config = self._mesclar_com_defaults(self._config)
                return self._config
            except Exception:  # noqa: BLE001, S110
                pass

        self._config = self.defaults.copy()
        self.salvar()
        return self._config

    def salvar(self) -> None:
        """Salva as configurações no arquivo."""
        if self._config is None:
            self._config = self.defaults.copy()

        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=4, ensure_ascii=False)
        except Exception as e:  # noqa: BLE001
            print(f"⚠️ Erro ao salvar configurações: {e}")

    def _mesclar_com_defaults(self, config: dict[str, Any]) -> dict[str, Any]:
        """Mescla a configuração com os defaults para garantir todas as chaves."""
        merged = self.defaults.copy()
        
        # Mescla recursivamente
        for key, value in config.items():
            if key in merged:
                if isinstance(value, dict) and isinstance(merged[key], dict):
                    merged[key].update(value)
                else:
                    merged[key] = value
            else:
                merged[key] = value

        return merged

    def get(self, key: str, default: Any = None) -> Any:
        """Obtém um valor da configuração."""
        config = self.carregar()
        keys = key.split('.')
        value = config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value if value is not None else default

    def set(self, key: str, value: Any) -> None:
        """Define um valor na configuração."""
        config = self.carregar()
        keys = key.split('.')
        target = config
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        target[keys[-1]] = value
        self._config = config
        self.salvar()

    def get_colunas_selecionadas(self) -> list[str]:
        """Retorna a lista de colunas selecionadas."""
        return self.get('relatorio.colunas', self.defaults['relatorio']['colunas'])

    def set_colunas_selecionadas(self, colunas: list[str]) -> None:
        """Define a lista de colunas selecionadas."""
        self.set('relatorio.colunas', colunas)

    def get_abas_selecionadas(self) -> list[str]:
        """Retorna a lista de abas selecionadas."""
        return self.get('relatorio.abas', self.defaults['relatorio']['abas'])

    def set_abas_selecionadas(self, abas: list[str]) -> None:
        """Define a lista de abas selecionadas."""
        self.set('relatorio.abas', abas)

    def get_ordenacao(self) -> str:
        """Retorna o critério de ordenação."""
        return self.get('relatorio.ordenacao', 'cpf')

    def set_ordenacao(self, ordenacao: str) -> None:
        """Define o critério de ordenação."""
        self.set('relatorio.ordenacao', ordenacao)

    def reset_defaults(self) -> None:
        """Restaura as configurações padrão."""
        self._config = self.defaults.copy()
        self.salvar()