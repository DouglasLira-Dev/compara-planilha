"""Janela de configurações do Comparador de Planilhas."""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QDialog,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.config import Config
from src.config_manager import ConfigManager


class ConfigWindow(QDialog):
    """Janela de configurações."""

    config_saved = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⚙️ Configurações")
        self.setMinimumSize(600, 500)
        self.setModal(True)

        self.config_manager = ConfigManager()
        self.config = Config

        self.init_ui()
        self.carregar_configuracoes()

    def init_ui(self):
        """Inicializa a interface."""
        layout = QVBoxLayout(self)

        # Widget com abas
        tabs = QTabWidget()
        tabs.addTab(self._criar_aba_geral(), "📄 Geral")
        tabs.addTab(self._criar_aba_colunas(), "📋 Colunas")
        tabs.addTab(self._criar_aba_abas(), "📊 Abas")
        tabs.addTab(self._criar_aba_ordenacao(), "📌 Ordenação")
        layout.addWidget(tabs)

        # Botões
        botoes_layout = QHBoxLayout()
        btn_salvar = QPushButton("💾 Salvar")
        btn_salvar.clicked.connect(self.salvar_configuracoes)
        btn_salvar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-weight: bold;
                padding: 10px 30px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)

        btn_cancelar = QPushButton("❌ Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        btn_cancelar.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-weight: bold;
                padding: 10px 30px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)

        btn_restaurar = QPushButton("🔄 Restaurar Padrões")
        btn_restaurar.clicked.connect(self.restaurar_padroes)
        btn_restaurar.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)

        botoes_layout.addWidget(btn_restaurar)
        botoes_layout.addStretch()
        botoes_layout.addWidget(btn_salvar)
        botoes_layout.addWidget(btn_cancelar)
        layout.addLayout(botoes_layout)

    def _criar_aba_geral(self) -> QWidget:
        """Cria aba de configurações gerais."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Nome do relatório
        group_relatorio = QGroupBox("📄 Relatório")
        group_layout = QGridLayout()
        group_relatorio.setLayout(group_layout)

        group_layout.addWidget(QLabel("Nome do arquivo:"), 0, 0)
        self.nome_relatorio = QLineEdit()
        self.nome_relatorio.setPlaceholderText("relatorio_comparacao.xlsx")
        group_layout.addWidget(self.nome_relatorio, 0, 1)

        group_layout.addWidget(QLabel("Pasta de destino:"), 1, 0)
        self.pasta_destino = QLineEdit()
        self.pasta_destino.setPlaceholderText("Selecione a pasta...")
        group_layout.addWidget(self.pasta_destino, 1, 1)

        btn_selecionar_pasta = QPushButton("📂 Selecionar")
        btn_selecionar_pasta.clicked.connect(self.selecionar_pasta)
        group_layout.addWidget(btn_selecionar_pasta, 1, 2)

        layout.addWidget(group_relatorio)

        # Limites de processamento
        group_limites = QGroupBox("⚡ Processamento")
        group_limites_layout = QGridLayout()
        group_limites.setLayout(group_limites_layout)

        group_limites_layout.addWidget(QLabel("Máximo de registros (0 = sem limite):"), 0, 0)
        self.max_registros = QLineEdit()
        self.max_registros.setPlaceholderText("0")
        group_limites_layout.addWidget(self.max_registros, 0, 1)

        group_limites_layout.addWidget(QLabel("Linhas para buscar cabeçalho:"), 1, 0)
        self.max_linhas_cabecalho = QLineEdit()
        self.max_linhas_cabecalho.setPlaceholderText("10")
        group_limites_layout.addWidget(self.max_linhas_cabecalho, 1, 1)

        layout.addWidget(group_limites)

        layout.addStretch()
        return widget

    def _criar_aba_colunas(self) -> QWidget:
        """Cria aba de seleção de colunas."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        group_colunas = QGroupBox("📋 Colunas a incluir no relatório")
        group_layout = QVBoxLayout()
        group_colunas.setLayout(group_layout)

        self.colunas_checkboxes = {}
        colunas = ["CPF", "Matrícula", "Data de Admissão", "Nome", "Departamento", "Cargo", "Telefone", "Email"]

        # Grid para colunas
        grid_layout = QGridLayout()
        row, col = 0, 0
        for coluna in colunas:
            checkbox = QCheckBox(coluna)
            self.colunas_checkboxes[coluna] = checkbox
            grid_layout.addWidget(checkbox, row, col)
            col += 1
            if col >= 2:
                col = 0
                row += 1

        group_layout.addLayout(grid_layout)

        # Aviso
        aviso = QLabel("ℹ️ CPF, Matrícula e Data de Admissão são obrigatórios e sempre incluídos")
        aviso.setStyleSheet("color: #7f8c8d; font-style: italic;")
        group_layout.addWidget(aviso)

        layout.addWidget(group_colunas)
        layout.addStretch()
        return widget

    def _criar_aba_abas(self) -> QWidget:
        """Cria aba de seleção de abas do relatório."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        group_abas = QGroupBox("📊 Abas a incluir no relatório")
        group_layout = QVBoxLayout()
        group_abas.setLayout(group_layout)

        self.abas_checkboxes = {}
        abas = ["Divergências", "Apenas na A", "Apenas na B", "Iguais", "Erros", "Resumo"]

        for aba in abas:
            checkbox = QCheckBox(aba)
            self.abas_checkboxes[aba] = checkbox
            group_layout.addWidget(checkbox)

        layout.addWidget(group_abas)
        layout.addStretch()
        return widget

    def _criar_aba_ordenacao(self) -> QWidget:
        """Cria aba de ordenação."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        group_ordenacao = QGroupBox("📌 Ordenação dos dados")
        group_layout = QVBoxLayout()
        group_ordenacao.setLayout(group_layout)

        self.ordenacao_group = QButtonGroup(self)

        opcoes = [
            ("cpf", "CPF (Recomendado)"),
            ("matricula", "Matrícula"),
            ("nome", "Nome"),
            ("data", "Data de Admissão"),
        ]

        for valor, texto in opcoes:
            radio = QRadioButton(texto)
            radio.setObjectName(valor)
            self.ordenacao_group.addButton(radio)
            group_layout.addWidget(radio)

        layout.addWidget(group_ordenacao)
        layout.addStretch()
        return widget

    def selecionar_pasta(self):
        """Abre diálogo para selecionar pasta."""
        pasta = QFileDialog.getExistingDirectory(self, "Selecionar Pasta de Destino")
        if pasta:
            self.pasta_destino.setText(pasta)

    def carregar_configuracoes(self):
        """Carrega as configurações atuais do config_manager."""
        config = self.config_manager.carregar()
        
        # Geral
        self.nome_relatorio.setText(config.get('relatorio', {}).get('nome', Config.RELATORIO_NOME_PADRAO))
        
        pasta = config.get('relatorio', {}).get('pasta', '')
        if pasta:
            self.pasta_destino.setText(pasta)
        else:
            self.pasta_destino.setText(str(Config.REPORTS_DIR))
        
        self.max_registros.setText(str(config.get('processamento', {}).get('max_registros', 0)))
        self.max_linhas_cabecalho.setText(str(config.get('processamento', {}).get('max_linhas_cabecalho', 10)))

        # Colunas
        colunas_selecionadas = config.get('relatorio', {}).get('colunas', [])
        for nome, checkbox in self.colunas_checkboxes.items():
            checkbox.setChecked(nome in colunas_selecionadas)

        # Abas
        abas_selecionadas = config.get('relatorio', {}).get('abas', [])
        for nome, checkbox in self.abas_checkboxes.items():
            checkbox.setChecked(nome in abas_selecionadas)

        # Ordenação
        ordenacao = config.get('relatorio', {}).get('ordenacao', 'cpf')
        for btn in self.ordenacao_group.buttons():
            if btn.objectName() == ordenacao:
                btn.setChecked(True)
                break

    def salvar_configuracoes(self):
        """Salva as configurações no config_manager."""
        try:
            # Valida os valores
            nome = self.nome_relatorio.text().strip()
            if not nome:
                raise ValueError("Nome do relatório não pode estar vazio")

            if not nome.endswith('.xlsx'):
                nome += '.xlsx'

            pasta = self.pasta_destino.text().strip()
            if not pasta:
                pasta = str(Config.REPORTS_DIR)

            max_registros = int(self.max_registros.text() or "0")
            if max_registros < 0:
                raise ValueError("Máximo de registros deve ser >= 0")

            max_linhas = int(self.max_linhas_cabecalho.text() or "10")
            if max_linhas < 1:
                raise ValueError("Linhas para busca deve ser >= 1")

            # Salva no config_manager
            self.config_manager.set('relatorio.nome', nome)
            self.config_manager.set('relatorio.pasta', pasta)
            self.config_manager.set('processamento.max_registros', max_registros)
            self.config_manager.set('processamento.max_linhas_cabecalho', max_linhas)

            # Colunas selecionadas
            colunas_selecionadas = [
                nome for nome, checkbox in self.colunas_checkboxes.items()
                if checkbox.isChecked()
            ]
            # Garante que colunas obrigatórias estão incluídas
            obrigatorias = ["CPF", "Matrícula", "Data de Admissão"]
            for col in obrigatorias:
                if col not in colunas_selecionadas:
                    colunas_selecionadas.append(col)
            self.config_manager.set_colunas_selecionadas(colunas_selecionadas)

            # Abas selecionadas
            abas_selecionadas = [
                nome for nome, checkbox in self.abas_checkboxes.items()
                if checkbox.isChecked()
            ]
            # Garante que Resumo está sempre incluído
            if "Resumo" not in abas_selecionadas:
                abas_selecionadas.append("Resumo")
            self.config_manager.set_abas_selecionadas(abas_selecionadas)

            # Ordenação
            for btn in self.ordenacao_group.buttons():
                if btn.isChecked():
                    self.config_manager.set_ordenacao(btn.objectName())
                    break

            QMessageBox.information(
                self,
                "Configurações Salvas",
                f"✅ Configurações salvas com sucesso!\n\n"
                f"📄 Relatório: {nome}\n"
                f"📁 Pasta: {pasta}\n"
                f"⚡ Max registros: {max_registros}\n"
                f"🔍 Max linhas cabeçalho: {max_linhas}"
            )

            self.config_saved.emit()
            self.accept()

        except ValueError as e:
            QMessageBox.warning(self, "Erro de Validação", f"❌ {e!s}")
        except Exception as e:  # noqa: BLE001
            QMessageBox.critical(self, "Erro", f"❌ Erro ao salvar: {e!s}")

    def restaurar_padroes(self):
        """Restaura as configurações padrão."""
        reply = QMessageBox.question(
            self,
            "Restaurar Padrões",
            "Deseja restaurar todas as configurações para os valores padrão?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.config_manager.reset_defaults()
            self.carregar_configuracoes()
            QMessageBox.information(self, "Padrões Restaurados", "✅ Configurações restauradas para os valores padrão!")