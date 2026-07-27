"""Janela de detalhes de erros."""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)


class ErrorsWindow(QDialog):
    """Janela para exibir detalhes dos erros."""

    def __init__(self, erros: list, parent=None):
        super().__init__(parent)
        self.erros = erros

        self.setWindowTitle("⚠️ Detalhes dos Erros")
        self.setMinimumSize(800, 400)
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        """Inicializa a interface."""
        layout = QVBoxLayout(self)

        # Título
        titulo = QLabel(f"⚠️ Registros Ignorados ({len(self.erros)})")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #e67e22;
            padding: 10px;
        """)
        layout.addWidget(titulo)

        # Tabela de erros
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels(["Linha", "Planilha", "CPF", "Matrícula", "Data", "Erro"])
        self.tabela.setSortingEnabled(True)

        self._popular_tabela()

        layout.addWidget(self.tabela)

        # Botões
        botoes_layout = QHBoxLayout()

        btn_exportar = QPushButton("💾 Exportar CSV")
        btn_exportar.clicked.connect(self.exportar_csv)
        btn_exportar.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                padding: 8px 20px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        botoes_layout.addWidget(btn_exportar)

        btn_fechar = QPushButton("✅ Fechar")
        btn_fechar.clicked.connect(self.accept)
        btn_fechar.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                font-weight: bold;
                padding: 8px 20px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        botoes_layout.addWidget(btn_fechar)

        botoes_layout.addStretch()
        layout.addLayout(botoes_layout)

    def _popular_tabela(self):
        """Popula a tabela com os erros."""
        if not self.erros:
            self.tabela.setRowCount(1)
            self.tabela.setItem(0, 0, QTableWidgetItem("Nenhum erro encontrado"))
            return

        self.tabela.setRowCount(len(self.erros))

        for row, erro in enumerate(self.erros):
            # Linha
            item = QTableWidgetItem(str(erro.get("linha", "")))
            self.tabela.setItem(row, 0, item)

            # Planilha
            item = QTableWidgetItem(erro.get("planilha", ""))
            self.tabela.setItem(row, 1, item)

            # CPF (mascarado)
            cpf = erro.get("cpf", "")
            if cpf:
                from src.validators import ValidadorCPF
                cpf = ValidadorCPF.mascarar(cpf)
            item = QTableWidgetItem(cpf)
            self.tabela.setItem(row, 2, item)

            # Matrícula
            item = QTableWidgetItem(erro.get("matricula", ""))
            self.tabela.setItem(row, 3, item)

            # Data
            item = QTableWidgetItem(erro.get("data", ""))
            self.tabela.setItem(row, 4, item)

            # Erro (destacado)
            item = QTableWidgetItem(erro.get("erro", ""))
            item.setBackground(QColor(255, 220, 220))
            self.tabela.setItem(row, 5, item)

        # Ajusta largura das colunas
        self.tabela.resizeColumnsToContents()

    def exportar_csv(self):
        """Exporta os erros para CSV."""
        import csv
        from datetime import datetime
        from pathlib import Path

        try:
            # Nome do arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # noqa: DTZ005
            caminho = Path("logs") / f"erros_{timestamp}.csv"
            caminho.parent.mkdir(exist_ok=True)

            # Escreve CSV
            with open(caminho, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Linha", "Planilha", "CPF", "Matrícula", "Data", "Erro"])

                for erro in self.erros:
                    writer.writerow([
                        erro.get("linha", ""),
                        erro.get("planilha", ""),
                        erro.get("cpf", ""),
                        erro.get("matricula", ""),
                        erro.get("data", ""),
                        erro.get("erro", ""),
                    ])

            QMessageBox.information(
                self,
                "Exportado",
                f"✅ Erros exportados com sucesso!\n\n📄 Arquivo: {caminho}"
            )

        except Exception as e:  # noqa: BLE001
            QMessageBox.critical(self, "Erro", f"Erro ao exportar:\n{e!s}")