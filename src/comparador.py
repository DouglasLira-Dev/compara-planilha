"""Módulo de comparação de planilhas."""

from src.models import (
    RegistroDivergente,
    RegistroErro,
    RegistroPlanilha,
    ResultadoComparacao,
)


class ComparadorPlanilhas:
    """Classe para comparação de duas planilhas."""

    def __init__(self):
        self.dados_a: dict[str, RegistroPlanilha] = {}
        self.dados_b: dict[str, RegistroPlanilha] = {}
        self.resultado: ResultadoComparacao | None = None
        self.progresso_callback = None

    def definir_callback_progresso(self, callback):
        """Define função de callback para atualizar progresso."""
        self.progresso_callback = callback

    def _atualizar_progresso(self, valor: int, mensagem: str = ""):
        """Atualiza o progresso via callback."""
        if self.progresso_callback:
            self.progresso_callback(valor, mensagem)

    def carregar_dados(
        self,
        dados_a: list[dict],
        dados_b: list[dict],
        erros_a: list[dict],
        erros_b: list[dict],
    ) -> None:
        """
        Carrega os dados das duas planilhas para comparação.

        Args:
            dados_a: Lista de registros da planilha A
            dados_b: Lista de registros da planilha B
            erros_a: Lista de erros da planilha A
            erros_b: Lista de erros da planilha B
        """
        self._atualizar_progresso(10, "🔄 Convertendo dados...")

        # Converte dicionários para objetos RegistroPlanilha
        registros_a = []
        for item in dados_a:
            try:
                reg = RegistroPlanilha(
                    cpf=item.get("cpf", ""),
                    matricula=item.get("matricula", ""),
                    data_admissao=item.get("data_admissao", ""),
                    linha_original=item.get("linha_original"),
                    origem=item.get("origem", "A"),
                    dados_extras=item.get("dados_extras", {}),
                )
                registros_a.append(reg)
            except Exception as e:  # noqa: BLE001
                erros_a.append({
                    "linha": item.get("linha_original", 0),
                    "cpf": item.get("cpf", ""),
                    "matricula": item.get("matricula", ""),
                    "data": item.get("data_admissao", ""),
                    "erro": f"Erro ao converter: {e!s}",
                })

        registros_b = []
        for item in dados_b:
            try:
                reg = RegistroPlanilha(
                    cpf=item.get("cpf", ""),
                    matricula=item.get("matricula", ""),
                    data_admissao=item.get("data_admissao", ""),
                    linha_original=item.get("linha_original"),
                    origem=item.get("origem", "B"),
                    dados_extras=item.get("dados_extras", {}),
                )
                registros_b.append(reg)
            except Exception as e:  # noqa: BLE001
                erros_b.append({
                    "linha": item.get("linha_original", 0),
                    "cpf": item.get("cpf", ""),
                    "matricula": item.get("matricula", ""),
                    "data": item.get("data_admissao", ""),
                    "erro": f"Erro ao converter: {e!s}",
                })

        # Indexa os dados por chave de comparação
        self._atualizar_progresso(20, "📊 Indexando dados...")
        self.dados_a = {r.chave_comparacao(): r for r in registros_a}
        self.dados_b = {r.chave_comparacao(): r for r in registros_b}

        # Inicializa o resultado
        self.resultado = ResultadoComparacao(
            total_registros_a=len(registros_a),
            total_registros_b=len(registros_b),
        )

        # Adiciona os erros
        for erro in erros_a:
            self.resultado.erros.append(
                RegistroErro(
                    linha=erro.get("linha", 0),
                    planilha="A",
                    cpf=erro.get("cpf"),
                    matricula=erro.get("matricula"),
                    data=erro.get("data"),
                    erro=erro.get("erro", "Erro desconhecido"),
                )
            )

        for erro in erros_b:
            self.resultado.erros.append(
                RegistroErro(
                    linha=erro.get("linha", 0),
                    planilha="B",
                    cpf=erro.get("cpf"),
                    matricula=erro.get("matricula"),
                    data=erro.get("data"),
                    erro=erro.get("erro", "Erro desconhecido"),
                )
            )

        self._atualizar_progresso(30, "✅ Dados carregados!")

    def comparar(self) -> ResultadoComparacao:
        """
        Executa a comparação entre as duas planilhas.

        Returns:
            ResultadoComparacao com todos os registros categorizados
        """
        if not self.resultado:
            raise ValueError("Dados não carregados. Execute carregar_dados() primeiro.")

        chaves_a = set(self.dados_a.keys())
        chaves_b = set(self.dados_b.keys())

        total = len(chaves_a) + len(chaves_b) + len(chaves_a & chaves_b)
        processado = 0

        # Registros apenas na planilha A
        self._atualizar_progresso(40, "🔍 Verificando registros apenas na A...")
        for chave in chaves_a - chaves_b:
            self.resultado.apenas_a.append(self.dados_a[chave])
            processado += 1
            if processado % 100 == 0:
                self._atualizar_progresso(40 + int((processado / total) * 30), f"⏳ Processando... {processado}/{total}")

        # Registros apenas na planilha B
        self._atualizar_progresso(55, "🔍 Verificando registros apenas na B...")
        for chave in chaves_b - chaves_a:
            self.resultado.apenas_b.append(self.dados_b[chave])
            processado += 1
            if processado % 100 == 0:
                self._atualizar_progresso(55 + int((processado / total) * 20), f"⏳ Processando... {processado}/{total}")

        # Registros em ambas as planilhas
        self._atualizar_progresso(70, "🔍 Comparando registros comuns...")
        for chave in chaves_a & chaves_b:
            reg_a = self.dados_a[chave]
            reg_b = self.dados_b[chave]

            # Compara as datas E os nomes
            data_igual = reg_a.data_admissao == reg_b.data_admissao
            nome_igual = reg_a.nome == reg_b.nome

            if data_igual and nome_igual:
                # Registros idênticos (data e nome iguais)
                self.resultado.iguais.append(reg_a)
            else:
                # Divergência de data OU nome
                diferenca_dias = abs((reg_a.data_admissao - reg_b.data_admissao).days) if not data_igual else 0
                
                divergente = RegistroDivergente(
                    cpf=reg_a.cpf,
                    matricula=reg_a.matricula,
                    nome_a=reg_a.nome if reg_a.nome else "",
                    nome_b=reg_b.nome if reg_b.nome else "",
                    data_a=reg_a.data_admissao,
                    data_b=reg_b.data_admissao,
                    diferenca_dias=diferenca_dias,
                    dados_extras_a=reg_a.dados_extras if reg_a.dados_extras else None,
                    dados_extras_b=reg_b.dados_extras if reg_b.dados_extras else None,
                )
                self.resultado.divergencias.append(divergente)

            processado += 1
            if processado % 100 == 0:
                progresso = 70 + int((processado / total) * 25)
                self._atualizar_progresso(progresso, f"⏳ Processando... {processado}/{total}")

        # Calcula os totais
        self._atualizar_progresso(95, "📊 Calculando totais...")
        self.resultado.calcular_totais()

        self._atualizar_progresso(100, "✅ Comparação concluída!")

        return self.resultado

    def obter_resumo(self) -> dict:
        """Retorna um resumo da comparação."""
        if not self.resultado:
            return {}

        return {
            "total_registros_a": self.resultado.total_registros_a,
            "total_registros_b": self.resultado.total_registros_b,
            "total_apenas_a": self.resultado.total_apenas_a,
            "total_apenas_b": self.resultado.total_apenas_b,
            "total_divergencias": self.resultado.total_divergencias,
            "total_iguais": self.resultado.total_iguais,
            "total_erros": self.resultado.total_erros,
            "taxa_divergencia": (
                self.resultado.total_divergencias / max(self.resultado.total_registros_a, 1) * 100
            ),
        }