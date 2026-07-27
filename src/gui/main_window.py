"""Janela principal do Comparador de Planilhas."""

import sys
from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src import __version__
from src.leitor import LeitorPlanilhas


class MainWindow(QMainWindow):
    """Janela principal da aplicação."""

    # Sinais
    comparar_clicked = pyqtSignal()
    configurar_clicked = pyqtSignal()
    ajuda_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.leitor_a = LeitorPlanilhas()
        self.leitor_b = LeitorPlanilhas()

        self.init_ui()

    def init_ui(self):
        """Inicializa a interface da janela principal."""
        self.setWindowTitle(f"🛡️ Comparador de Planilhas v{__version__}")
        self.setMinimumSize(900, 600)
        self.setStyleSheet(self._get_styles())

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)

        # ===== TÍTULO =====
        title_label = QLabel("🛡️ COMPARADOR DE PLANILHAS")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px;
        """)
        main_layout.addWidget(title_label)

        # ===== SELEÇÃO DE PLANILHAS =====
        planilhas_group = QGroupBox("📂 Seleção de Planilhas")
        planilhas_layout = QGridLayout()
        planilhas_group.setLayout(planilhas_layout)

        # Planilha A
        planilhas_layout.addWidget(QLabel("Planilha A:"), 0, 0)
        self.campo_a = QLineEdit()
        self.campo_a.setPlaceholderText("Selecione a primeira planilha...")
        planilhas_layout.addWidget(self.campo_a, 0, 1)
        self.botao_a = QPushButton("📂 Selecionar")
        self.botao_a.clicked.connect(lambda: self.selecionar_planilha("A"))
        planilhas_layout.addWidget(self.botao_a, 0, 2)

        # Aba A
        planilhas_layout.addWidget(QLabel("Aba A:"), 1, 0)
        self.combo_a = QComboBox()
        self.combo_a.setEnabled(False)
        self.combo_a.addItem("Selecione uma planilha primeiro")
        planilhas_layout.addWidget(self.combo_a, 1, 1, 1, 2)

        # Planilha B
        planilhas_layout.addWidget(QLabel("Planilha B:"), 2, 0)
        self.campo_b = QLineEdit()
        self.campo_b.setPlaceholderText("Selecione a segunda planilha...")
        planilhas_layout.addWidget(self.campo_b, 2, 1)
        self.botao_b = QPushButton("📂 Selecionar")
        self.botao_b.clicked.connect(lambda: self.selecionar_planilha("B"))
        planilhas_layout.addWidget(self.botao_b, 2, 2)

        # Aba B
        planilhas_layout.addWidget(QLabel("Aba B:"), 3, 0)
        self.combo_b = QComboBox()
        self.combo_b.setEnabled(False)
        self.combo_b.addItem("Selecione uma planilha primeiro")
        planilhas_layout.addWidget(self.combo_b, 3, 1, 1, 2)

        main_layout.addWidget(planilhas_group)

        # ===== BOTÕES DE AÇÃO =====
        botoes_layout = QHBoxLayout()
        botoes_layout.setSpacing(15)

        self.btn_comparar = QPushButton("🔍 COMPARAR PLANILHAS")
        self.btn_comparar.setEnabled(False)
        self.btn_comparar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 12px 30px;
                border-radius: 8px;
            }
            QPushButton:hover:!pressed {
                background-color: #2ecc71;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        self.btn_comparar.clicked.connect(self.comparar_clicked.emit)
        botoes_layout.addWidget(self.btn_comparar)

        self.btn_config = QPushButton("⚙️ Configurações")
        self.btn_config.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                padding: 12px 20px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.btn_config.clicked.connect(self.configurar_clicked.emit)
        botoes_layout.addWidget(self.btn_config)

        self.btn_ajuda = QPushButton("❓ Ajuda")
        self.btn_ajuda.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                font-weight: bold;
                padding: 12px 20px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        self.btn_ajuda.clicked.connect(self.ajuda_clicked.emit)
        botoes_layout.addWidget(self.btn_ajuda)

        botoes_layout.addStretch()

        main_layout.addLayout(botoes_layout)

        # ===== STATUS =====
        status_frame = QFrame()
        status_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        status_frame.setStyleSheet("background-color: #ecf0f1; border-radius: 8px;")

        status_layout = QVBoxLayout(status_frame)

        self.status_label = QLabel("✅ Aguardando seleção das planilhas...")
        self.status_label.setStyleSheet("padding: 5px; font-weight: bold;")
        status_layout.addWidget(self.status_label)

        self.detalhes_status = QTextEdit()
        self.detalhes_status.setReadOnly(True)
        self.detalhes_status.setMaximumHeight(80)
        self.detalhes_status.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: none;
                font-family: 'Consolas', monospace;
                font-size: 10pt;
            }
        """)
        status_layout.addWidget(self.detalhes_status)

        main_layout.addWidget(status_frame)

        # ===== PROGRESSO =====
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 6px;
            }
        """)
        main_layout.addWidget(self.progress_bar)

    def _get_styles(self) -> str:
        """Retorna os estilos da aplicação."""
        return """
            QMainWindow {
                background-color: #f5f6fa;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding-top: 15px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
            QComboBox {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                background-color: white;
            }
            QComboBox:focus {
                border-color: #3498db;
            }
            QPushButton {
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
            QLabel {
                font-weight: bold;
            }
        """

    def selecionar_planilha(self, origem: str):
        """Abre diálogo para selecionar planilha."""
        caminho, _ = QFileDialog.getOpenFileName(
            self,
            f"Selecionar Planilha {origem}",
            "",
            "Planilhas Excel (*.xlsx *.xls);;Arquivos Excel (*.xlsx);;Arquivos Excel Antigos (*.xls);;Todos os Arquivos (*.*)"
        )

        if not caminho:
            return

        try:
            leitor = self.leitor_a if origem == "A" else self.leitor_b

            # Carrega o arquivo
            leitor.carregar_arquivo(caminho)

            # Atualiza o campo
            if origem == "A":
                self.campo_a.setText(caminho)
                self.combo_a.clear()
                self.combo_a.addItems(leitor.abas)
                self.combo_a.setEnabled(len(leitor.abas) > 1)

                # Se só tem 1 aba, seleciona automaticamente
                if len(leitor.abas) == 1:
                    self.combo_a.setCurrentIndex(0)
                    leitor.selecionar_aba(leitor.abas[0])

                self.atualizar_status(f"✅ Planilha A carregada: {Path(caminho).name} (Abas: {len(leitor.abas)})")

            else:
                self.campo_b.setText(caminho)
                self.combo_b.clear()
                self.combo_b.addItems(leitor.abas)
                self.combo_b.setEnabled(len(leitor.abas) > 1)

                if len(leitor.abas) == 1:
                    self.combo_b.setCurrentIndex(0)
                    leitor.selecionar_aba(leitor.abas[0])

                self.atualizar_status(f"✅ Planilha B carregada: {Path(caminho).name} (Abas: {len(leitor.abas)})")

            # Verifica se pode habilitar o botão Comparar
            self.verificar_pronto_para_comparar()

        except ImportError as e:
            QMessageBox.critical(
                self,
                "Erro de Dependência",
                f"Biblioteca necessária não encontrada:\n\n{e!s}\n\n"
                "Execute no terminal:\n"
                "pip install xlrd openpyxl"
            )
        except Exception as e:  # noqa: BLE001
            QMessageBox.critical(self, "Erro", f"Erro ao carregar planilha:\n\n{e!s}")

    def verificar_pronto_para_comparar(self):
        """Verifica se ambas as planilhas estão prontas para comparação."""
        pronto = (
            self.campo_a.text() != ""
            and self.campo_b.text() != ""
            and self.combo_a.currentText() != "Selecione uma planilha primeiro"
            and self.combo_b.currentText() != "Selecione uma planilha primeiro"
        )
        self.btn_comparar.setEnabled(pronto)

        if pronto:
            self.atualizar_status("✅ Pronto para comparar!")

    def atualizar_status(self, mensagem: str):
        """Atualiza a mensagem de status."""
        self.status_label.setText(mensagem)

    def adicionar_detalhe(self, mensagem: str):
        """Adiciona uma linha ao detalhamento de status."""
        self.detalhes_status.append(mensagem)

    def mostrar_progresso(self, mostrar: bool = True):
        """Mostra ou oculta a barra de progresso."""
        self.progress_bar.setVisible(mostrar)

    def atualizar_progresso(self, valor: int, maximo: int = 100):
        """Atualiza a barra de progresso."""
        self.progress_bar.setMaximum(maximo)
        self.progress_bar.setValue(valor)
        self.progress_bar.setFormat(f"{int(valor/maximo*100)}%")

    def closeEvent(self, event):
        """Evento ao fechar a janela."""
        reply = QMessageBox.question(
            self,
            "Sair",
            "Deseja realmente sair?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

    def ajuda_clicked(self):  # noqa: F811
        """Abre a janela de ajuda."""
        from src.gui.help_window import HelpWindow
        help_window = HelpWindow(self)
        help_window.exec()


def main():
    """Função principal para teste da GUI."""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()