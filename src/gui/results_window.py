"""Janela de resultados da comparação."""

import os
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.models import ResultadoComparacao


class ResultsWindow(QDialog):
    """Janela de resultados da comparação."""

    def __init__(self, resultado: ResultadoComparacao, caminho_relatorio: Path, parent=None):
        super().__init__(parent)
        self.resultado = resultado
        self.caminho_relatorio = caminho_relatorio
        self.resultado.calcular_totais()

        self.setWindowTitle("📊 Resultados da Comparação")
        self.setMinimumSize(900, 600)
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        """Inicializa a interface."""
        layout = QVBoxLayout(self)

        # ===== TÍTULO =====
        titulo = QLabel("✅ COMPARAÇÃO CONCLUÍDA!")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #27ae60;
            padding: 10px;
        """)
        layout.addWidget(titulo)

        # ===== RESUMO =====
        resumo_group = QGroupBox("📊 Resumo da Comparação")
        resumo_layout = QGridLayout()
        resumo_group.setLayout(resumo_layout)

        # Calcula totais
        total = self.resultado.total_apenas_a + self.resultado.total_apenas_b + \
                self.resultado.total_divergencias + self.resultado.total_iguais + \
                self.resultado.total_erros

        # Adiciona métricas
        metrics = [
            ("📄 Total Registros A:", str(self.resultado.total_registros_a), "#3498db"),
            ("📄 Total Registros B:", str(self.resultado.total_registros_b), "#3498db"),
            ("🔴 Divergências:", str(self.resultado.total_divergencias), "#e74c3c"),
            ("🟡 Apenas na A:", str(self.resultado.total_apenas_a), "#f39c12"),
            ("🟡 Apenas na B:", str(self.resultado.total_apenas_b), "#f39c12"),
            ("🟢 Iguais:", str(self.resultado.total_iguais), "#27ae60"),
            ("⚠️ Erros:", str(self.resultado.total_erros), "#e67e22"),
            ("📊 Total Processado:", str(total), "#2c3e50"),
        ]

        for i, (label, value, color) in enumerate(metrics):
            row = i // 2
            col = (i % 2) * 2

            lbl = QLabel(label)
            lbl.setStyleSheet("font-weight: bold;")
            resumo_layout.addWidget(lbl, row, col)

            val_lbl = QLabel(value)
            val_lbl.setStyleSheet(f"""
                font-weight: bold;
                font-size: 16px;
                color: {color};
            """)
            resumo_layout.addWidget(val_lbl, row, col + 1)

        layout.addWidget(resumo_group)

        # ===== ABAS COM DADOS =====
        tabs = QTabWidget()
        tabs.addTab(self._criar_aba_apenas_a(), "📋 Apenas na A")
        tabs.addTab(self._criar_aba_apenas_b(), "📋 Apenas na B")
        tabs.addTab(self._criar_aba_divergencias(), "🔴 Divergências")
        tabs.addTab(self._criar_aba_iguais(), "🟢 Iguais")
        tabs.addTab(self._criar_aba_erros(), "⚠️ Erros")
        layout.addWidget(tabs)

        # ===== BOTÕES =====
        botoes_layout = QHBoxLayout()

        btn_abrir = QPushButton("📂 Abrir Relatório")
        btn_abrir.clicked.connect(self.abrir_relatorio)
        btn_abrir.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-weight: bold;
                padding: 10px 25px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        botoes_layout.addWidget(btn_abrir)

        btn_pasta = QPushButton("📁 Abrir Pasta")
        btn_pasta.clicked.connect(self.abrir_pasta)
        btn_pasta.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                padding: 10px 25px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        botoes_layout.addWidget(btn_pasta)

        btn_fechar = QPushButton("✅ Fechar")
        btn_fechar.clicked.connect(self.accept)
        btn_fechar.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                font-weight: bold;
                padding: 10px 25px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        botoes_layout.addWidget(btn_fechar)

        botoes_layout.addStretch()

        # Informação do relatório
        info_relatorio = QLabel(f"📄 {self.caminho_relatorio.name}")
        info_relatorio.setStyleSheet("color: #7f8c8d; font-style: italic;")
        botoes_layout.addWidget(info_relatorio)

        layout.addLayout(botoes_layout)

    def _criar_tabela(self, dados: list, colunas: list) -> QTableWidget:
        """Cria uma tabela com os dados."""
        tabela = QTableWidget()
        tabela.setColumnCount(len(colunas))
        tabela.setHorizontalHeaderLabels(colunas)

        if not dados:
            tabela.setRowCount(1)
            tabela.setItem(0, 0, QTableWidgetItem("Nenhum dado encontrado"))
            return tabela

        tabela.setRowCount(len(dados))

        for row, item in enumerate(dados):
            if isinstance(item, dict):
                for col, key in enumerate(colunas):
                    valor = item.get(key, "")
                    if valor is None:
                        valor = ""
                    tabela.setItem(row, col, QTableWidgetItem(str(valor)))
            else:
                # Se for objeto, usa to_dict
                dados_dict = item.to_dict(mascarar_cpf=True)
                for col, key in enumerate(colunas):
                    valor = dados_dict.get(key, "")
                    if valor is None:
                        valor = ""
                    tabela.setItem(row, col, QTableWidgetItem(str(valor)))

        # Ajusta largura das colunas
        tabela.resizeColumnsToContents()
        tabela.setSortingEnabled(True)

        return tabela

    def _criar_aba_apenas_a(self) -> QWidget:
        """Cria aba de registros apenas na A."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        colunas = ["cpf", "matricula", "data_admissao"]
        headers = ["CPF", "Matrícula", "Data de Admissão"]

        dados = [r.to_dict(mascarar_cpf=True) for r in self.resultado.apenas_a]
        tabela = self._criar_tabela(dados, colunas)
        tabela.setHorizontalHeaderLabels(headers)

        layout.addWidget(tabela)
        return widget

    def _criar_aba_apenas_b(self) -> QWidget:
        """Cria aba de registros apenas na B."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        colunas = ["cpf", "matricula", "data_admissao"]
        headers = ["CPF", "Matrícula", "Data de Admissão"]

        dados = [r.to_dict(mascarar_cpf=True) for r in self.resultado.apenas_b]
        tabela = self._criar_tabela(dados, colunas)
        tabela.setHorizontalHeaderLabels(headers)

        layout.addWidget(tabela)
        return widget

    def _criar_aba_divergencias(self) -> QWidget:
        """Cria aba de divergências."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        colunas = ["cpf", "matricula", "data_a", "data_b", "diferenca_dias"]
        headers = ["CPF", "Matrícula", "Data A", "Data B", "Diferença (dias)"]

        dados = [r.to_dict(mascarar_cpf=True) for r in self.resultado.divergencias]
        tabela = self._criar_tabela(dados, colunas)
        tabela.setHorizontalHeaderLabels(headers)

        # Destaca diferenças grandes
        for row in range(tabela.rowCount()):
            item = tabela.item(row, 4)
            if item:
                try:
                    dias = int(item.text())
                    if dias > 30:
                        item.setBackground(QColor(255, 200, 200))
                    elif dias > 7:
                        item.setBackground(QColor(255, 235, 200))
                except:  # noqa: E722, S110
                    pass

        layout.addWidget(tabela)
        return widget

    def _criar_aba_iguais(self) -> QWidget:
        """Cria aba de registros idênticos."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        colunas = ["cpf", "matricula", "data_admissao"]
        headers = ["CPF", "Matrícula", "Data de Admissão"]

        dados = [r.to_dict(mascarar_cpf=True) for r in self.resultado.iguais]
        tabela = self._criar_tabela(dados, colunas)
        tabela.setHorizontalHeaderLabels(headers)

        layout.addWidget(tabela)
        return widget

    def _criar_aba_erros(self) -> QWidget:
        """Cria aba de erros."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        colunas = ["linha", "planilha", "cpf", "matricula", "data", "erro"]
        headers = ["Linha", "Planilha", "CPF", "Matrícula", "Data", "Erro"]

        dados = [r.to_dict(mascarar_cpf=True) for r in self.resultado.erros]
        tabela = self._criar_tabela(dados, colunas)
        tabela.setHorizontalHeaderLabels(headers)

        # Destaca erros
        for row in range(tabela.rowCount()):
            item = tabela.item(row, 5)  # Coluna Erro
            if item:
                item.setBackground(QColor(255, 220, 220))

        layout.addWidget(tabela)
        return widget

    def abrir_relatorio(self):
        """Abre o relatório no Excel."""
        try:
            if self.caminho_relatorio.exists():
                os.startfile(str(self.caminho_relatorio))
            else:
                QMessageBox.warning(self, "Erro", "Arquivo não encontrado!")
        except Exception as e:  # noqa: BLE001
            QMessageBox.critical(self, "Erro", f"Erro ao abrir relatório:\n{e!s}")

    def abrir_pasta(self):
        """Abre a pasta do relatório."""
        try:
            pasta = self.caminho_relatorio.parent
            if pasta.exists():
                os.startfile(str(pasta))
            else:
                QMessageBox.warning(self, "Erro", "Pasta não encontrada!")
        except Exception as e:  # noqa: BLE001
            QMessageBox.critical(self, "Erro", f"Erro ao abrir pasta:\n{e!s}")