"""Janela principal do Comparador de Planilhas."""

import sys
from datetime import datetime
from pathlib import Path

import PyQt6.QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal

from src import __version__
from src.leitor import LeitorPlanilhas


class MainWindow(PyQt6.QtWidgets.QMainWindow):
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
        
        # Conectar sinais
        self.comparar_clicked.connect(self.on_comparar_clicked)
        self.configurar_clicked.connect(self.on_configurar_clicked)
        self.ajuda_clicked.connect(self.on_ajuda_clicked)

    def init_ui(self):
        """Inicializa a interface da janela principal."""
        self.setWindowTitle(f"🛡️ Comparador de Planilhas v{__version__}")
        self.setMinimumSize(900, 600)
        self.setStyleSheet(self._get_styles())

        # Widget central
        central_widget = PyQt6.QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = PyQt6.QtWidgets.QVBoxLayout(central_widget)
        main_layout.setSpacing(20)

        # ===== TÍTULO =====
        title_label = PyQt6.QtWidgets.QLabel("🛡️ COMPARADOR DE PLANILHAS")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px;
        """)
        main_layout.addWidget(title_label)

        # ===== SELEÇÃO DE PLANILHAS =====
        planilhas_group = PyQt6.QtWidgets.QGroupBox("📂 Seleção de Planilhas")
        planilhas_layout = PyQt6.QtWidgets.QGridLayout()
        planilhas_group.setLayout(planilhas_layout)

        # Planilha A
        planilhas_layout.addWidget(PyQt6.QtWidgets.QLabel("Planilha A:"), 0, 0)
        self.campo_a = PyQt6.QtWidgets.QLineEdit()
        self.campo_a.setPlaceholderText("Selecione a primeira planilha...")
        planilhas_layout.addWidget(self.campo_a, 0, 1)
        self.botao_a = PyQt6.QtWidgets.QPushButton("📂 Selecionar")
        self.botao_a.clicked.connect(lambda: self.selecionar_planilha("A"))
        planilhas_layout.addWidget(self.botao_a, 0, 2)

        # Aba A
        planilhas_layout.addWidget(PyQt6.QtWidgets.QLabel("Aba A:"), 1, 0)
        self.combo_a = PyQt6.QtWidgets.QComboBox()
        self.combo_a.setEnabled(False)
        self.combo_a.addItem("Selecione uma planilha primeiro")
        planilhas_layout.addWidget(self.combo_a, 1, 1, 1, 2)

        # Planilha B
        planilhas_layout.addWidget(PyQt6.QtWidgets.QLabel("Planilha B:"), 2, 0)
        self.campo_b = PyQt6.QtWidgets.QLineEdit()
        self.campo_b.setPlaceholderText("Selecione a segunda planilha...")
        planilhas_layout.addWidget(self.campo_b, 2, 1)
        self.botao_b = PyQt6.QtWidgets.QPushButton("📂 Selecionar")
        self.botao_b.clicked.connect(lambda: self.selecionar_planilha("B"))
        planilhas_layout.addWidget(self.botao_b, 2, 2)

        # Aba B
        planilhas_layout.addWidget(PyQt6.QtWidgets.QLabel("Aba B:"), 3, 0)
        self.combo_b = PyQt6.QtWidgets.QComboBox()
        self.combo_b.setEnabled(False)
        self.combo_b.addItem("Selecione uma planilha primeiro")
        planilhas_layout.addWidget(self.combo_b, 3, 1, 1, 2)

        main_layout.addWidget(planilhas_group)

        # ===== BOTÕES DE AÇÃO =====
        botoes_layout = PyQt6.QtWidgets.QHBoxLayout()
        botoes_layout.setSpacing(15)

        self.btn_comparar = PyQt6.QtWidgets.QPushButton("🔍 COMPARAR PLANILHAS")
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

        self.btn_config = PyQt6.QtWidgets.QPushButton("⚙️ Configurações")
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

        self.btn_ajuda = PyQt6.QtWidgets.QPushButton("❓ Ajuda")
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
        status_frame = PyQt6.QtWidgets.QFrame()
        status_frame.setFrameStyle(PyQt6.QtWidgets.QFrame.Shape.Box | PyQt6.QtWidgets.QFrame.Shadow.Sunken)
        status_frame.setStyleSheet("background-color: #ecf0f1; border-radius: 8px;")

        status_layout = PyQt6.QtWidgets.QVBoxLayout(status_frame)

        self.status_label = PyQt6.QtWidgets.QLabel("✅ Aguardando seleção das planilhas...")
        self.status_label.setStyleSheet("padding: 5px; font-weight: bold;")
        status_layout.addWidget(self.status_label)

        self.detalhes_status = PyQt6.QtWidgets.QTextEdit()
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
        self.progress_bar = PyQt6.QtWidgets.QProgressBar()
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
        caminho, _ = PyQt6.QtWidgets.QFileDialog.getOpenFileName(
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
            PyQt6.QtWidgets.QMessageBox.critical(
                self,
                "Erro de Dependência",
                f"Biblioteca necessária não encontrada:\n\n{e!s}\n\n"
                "Execute no terminal:\n"
                "pip install xlrd openpyxl"
            )
        except Exception as e:  # noqa: BLE001
            PyQt6.QtWidgets.QMessageBox.critical(self, "Erro", f"Erro ao carregar planilha:\n\n{e!s}")

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

    # ===== SLOTS DOS BOTÕES =====
    
    def on_comparar_clicked(self):
        """Slot para o botão Comparar."""
        self.iniciar_comparacao()

    def on_configurar_clicked(self):
        """Slot para o botão Configurações."""
        self.abrir_configuracoes()

    def on_ajuda_clicked(self):
        """Slot para o botão Ajuda."""
        self.abrir_ajuda()

    # ===== FUNÇÕES DOS BOTÕES =====

    def abrir_ajuda(self):
        """Abre a janela de ajuda."""
        from src.gui.help_window import HelpWindow
        help_window = HelpWindow(self)
        help_window.exec()

    def abrir_configuracoes(self):
        """Abre a janela de configurações."""
        from src.gui.config_window import ConfigWindow
        config_window = ConfigWindow(self)
        config_window.config_saved.connect(self.atualizar_status_config)
        config_window.exec()

    def atualizar_status_config(self):
        """Atualiza status após salvar configurações."""
        self.atualizar_status("✅ Configurações salvas com sucesso!")

    def iniciar_comparacao(self):
        """Inicia o processo de comparação com dados reais."""

        from src.relatorio import GeradorRelatorio

        from ..comparador import ComparadorPlanilhas

        # Valida se as planilhas estão carregadas
        if not self.campo_a.text() or not self.campo_b.text():
            PyQt6.QtWidgets.QMessageBox.warning(self, "Aviso", "Selecione ambas as planilhas primeiro!")
            return

        # Valida se as abas estão selecionadas
        if self.combo_a.currentText() == "Selecione uma planilha primeiro":
            PyQt6.QtWidgets.QMessageBox.warning(self, "Aviso", "Selecione uma aba válida para a Planilha A!")
            return

        if self.combo_b.currentText() == "Selecione uma planilha primeiro":
            PyQt6.QtWidgets.QMessageBox.warning(self, "Aviso", "Selecione uma aba válida para a Planilha B!")
            return

        try:
            # Desabilita botões durante processamento
            self.btn_comparar.setEnabled(False)
            self.btn_config.setEnabled(False)
            self.botao_a.setEnabled(False)
            self.botao_b.setEnabled(False)

            # Mostra barra de progresso
            self.mostrar_progresso(True)
            self.atualizar_progresso(0, 100)
            self.detalhes_status.clear()
            self.atualizar_status("⏳ Processando...")

            # ===== ETAPA 1: CARREGAR PLANILHA A =====
            self.atualizar_progresso(5, 100)
            self.adicionar_detalhe("📊 Carregando planilha A...")
            
            aba_a = self.combo_a.currentText()
            self.leitor_a.selecionar_aba(aba_a)
            dados_a, erros_a = self.leitor_a.processar_dados("A")
            self.adicionar_detalhe(f"   ✅ {len(dados_a)} registros válidos, {len(erros_a)} erros")

            # ===== ETAPA 2: CARREGAR PLANILHA B =====
            self.atualizar_progresso(20, 100)
            self.adicionar_detalhe("📊 Carregando planilha B...")
            
            aba_b = self.combo_b.currentText()
            self.leitor_b.selecionar_aba(aba_b)
            dados_b, erros_b = self.leitor_b.processar_dados("B")
            self.adicionar_detalhe(f"   ✅ {len(dados_b)} registros válidos, {len(erros_b)} erros")

            # ===== ETAPA 3: COMPARAR =====
            self.atualizar_progresso(40, 100)
            self.adicionar_detalhe("🔍 Iniciando comparação...")
            
            comparador = ComparadorPlanilhas()
            
            # Define callback de progresso
            def atualizar_progresso_callback(valor, mensagem):
                progresso = 40 + int(valor * 0.55)  # 40% a 95%
                self.atualizar_progresso(progresso, 100)
                self.adicionar_detalhe(f"   {mensagem}")
                PyQt6.QtWidgets.QApplication.processEvents()  # Atualiza a interface
            
            comparador.definir_callback_progresso(atualizar_progresso_callback)
            
            # Carrega dados no comparador
            comparador.carregar_dados(dados_a, dados_b, erros_a, erros_b)
            
            # Executa comparação
            resultado = comparador.comparar()

            # ===== ETAPA 4: GERAR RELATÓRIO =====
            self.atualizar_progresso(95, 100)
            self.adicionar_detalhe("📄 Gerando relatório...")
            
            gerador = GeradorRelatorio()
            gerador.carregar_resultado(resultado)
            
            # Define nome do relatório (com timestamp)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # noqa: DTZ005
            nome_relatorio = f"relatorio_comparacao_{timestamp}.xlsx"
            gerador.definir_nome_arquivo(nome_relatorio)
            
            # Gera o relatório
            caminho_relatorio = gerador.gerar()
            self.adicionar_detalhe(f"   ✅ Relatório gerado: {caminho_relatorio.name}")

            # ===== FINALIZAR =====
            self.atualizar_progresso(100, 100)
            self.atualizar_status("✅ Comparação concluída!")
            self.mostrar_progresso(False)

            # Reabilita botões
            self.btn_comparar.setEnabled(True)
            self.btn_config.setEnabled(True)
            self.botao_a.setEnabled(True)
            self.botao_b.setEnabled(True)

            # ===== MOSTRA JANELA DE RESULTADOS =====
            from src.gui.results_window import ResultsWindow
            
            results_window = ResultsWindow(resultado, caminho_relatorio, self)
            results_window.exec()

        except Exception as e:  # noqa: BLE001
            # Em caso de erro
            import traceback
            self.mostrar_progresso(False)
            self.btn_comparar.setEnabled(True)
            self.btn_config.setEnabled(True)
            self.botao_a.setEnabled(True)
            self.botao_b.setEnabled(True)
            
            self.atualizar_status("❌ Erro durante a comparação!")
            self.adicionar_detalhe(f"❌ ERRO: {e!s}")
            self.adicionar_detalhe(traceback.format_exc())
            
            PyQt6.QtWidgets.QMessageBox.critical(
                self,
                "❌ Erro",
                f"Ocorreu um erro durante a comparação:\n\n{e!s}\n\n"
                f"Detalhes adicionais no status."
            )


def main():
    """Função principal para teste da GUI."""
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()