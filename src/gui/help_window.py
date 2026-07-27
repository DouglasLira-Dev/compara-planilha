"""Janela de ajuda do Comparador de Planilhas."""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QTabWidget,
    QWidget,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from src import __version__


class HelpWindow(QDialog):
    """Janela de ajuda e tutorial."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("❓ Ajuda - Comparador de Planilhas")
        self.setMinimumSize(700, 500)
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        """Inicializa a interface da janela de ajuda."""
        layout = QVBoxLayout(self)

        # Título
        titulo = QLabel(f"🛡️ Comparador de Planilhas v{__version__}")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        layout.addWidget(titulo)

        # Abas de ajuda
        tabs = QTabWidget()
        tabs.addTab(self._criar_aba_como_usar(), "📖 Como Usar")
        tabs.addTab(self._criar_aba_configuracoes(), "⚙️ Configurações")
        tabs.addTab(self._criar_aba_dicas(), "💡 Dicas")
        tabs.addTab(self._criar_aba_sobre(), "ℹ️ Sobre")
        layout.addWidget(tabs)

        # Botão fechar
        btn_fechar = QPushButton("✅ Fechar")
        btn_fechar.clicked.connect(self.accept)
        btn_fechar.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                padding: 10px 30px;
                border-radius: 8px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        layout.addWidget(btn_fechar, alignment=Qt.AlignmentFlag.AlignCenter)

    def _criar_aba_como_usar(self) -> QWidget:
        """Cria a aba 'Como Usar'."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        texto = QTextEdit()
        texto.setReadOnly(True)
        texto.setStyleSheet("font-size: 12px; line-height: 1.6;")
        texto.setHtml("""
        <h2>📋 Como Comparar Planilhas</h2>

        <h3>Passo 1: Selecionar Planilhas</h3>
        <ul>
            <li>Clique em <b>"Selecionar"</b> na Planilha A e escolha o arquivo</li>
            <li>Clique em <b>"Selecionar"</b> na Planilha B e escolha o arquivo</li>
            <li>O sistema suporta arquivos <b>.xlsx</b> (Excel moderno) e <b>.xls</b> (Excel antigo)</li>
        </ul>

        <h3>Passo 2: Selecionar Abas</h3>
        <ul>
            <li>Se a planilha tiver <b>múltiplas abas</b>, escolha qual comparar</li>
            <li>Se tiver apenas <b>uma aba</b>, será selecionada automaticamente</li>
        </ul>

        <h3>Passo 3: Configurar (Opcional)</h3>
        <ul>
            <li>Clique em <b>"Configurações"</b> para personalizar o relatório</li>
            <li>Escolha quais colunas incluir</li>
            <li>Defina o nome e pasta do relatório</li>
        </ul>

        <h3>Passo 4: Comparar</h3>
        <ul>
            <li>Clique em <b>"COMPARAR PLANILHAS"</b></li>
            <li>Aguarde o processamento</li>
            <li>Visualize o relatório gerado</li>
        </ul>

        <h3>Passo 5: Resultados</h3>
        <ul>
            <li>O relatório será gerado em Excel com várias abas:</li>
            <ul>
                <li><b>Divergências</b> - Datas diferentes</li>
                <li><b>Apenas na A</b> - Registros únicos</li>
                <li><b>Apenas na B</b> - Registros únicos</li>
                <li><b>Iguais</b> - Registros idênticos</li>
                <li><b>Erros</b> - Registros ignorados</li>
                <li><b>Resumo</b> - Estatísticas</li>
            </ul>
        </ul>
        """)
        layout.addWidget(texto)

        return widget

    def _criar_aba_configuracoes(self) -> QWidget:
        """Cria a aba 'Configurações'."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        texto = QTextEdit()
        texto.setReadOnly(True)
        texto.setStyleSheet("font-size: 12px; line-height: 1.6;")
        texto.setHtml("""
        <h2>⚙️ Configurações Disponíveis</h2>

        <h3>📄 Relatório</h3>
        <ul>
            <li><b>Nome do arquivo:</b> Defina o nome do relatório gerado</li>
            <li><b>Pasta de destino:</b> Escolha onde salvar o relatório</li>
        </ul>

        <h3>📋 Colunas</h3>
        <ul>
            <li>Selecione quais colunas extras incluir no relatório</li>
            <li>Colunas obrigatórias: CPF, Matrícula, Data de Admissão</li>
        </ul>

        <h3>📊 Abas do Relatório</h3>
        <ul>
            <li>Escolha quais abas incluir no relatório final</li>
            <li>Por padrão, todas as abas são incluídas</li>
        </ul>

        <h3>📌 Ordenação</h3>
        <ul>
            <li>Ordene os dados por: CPF, Matrícula ou Data</li>
            <li>Padrão: ordenação por CPF</li>
        </ul>
        """)
        layout.addWidget(texto)

        return widget

    def _criar_aba_dicas(self) -> QWidget:
        """Cria a aba 'Dicas'."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        texto = QTextEdit()
        texto.setReadOnly(True)
        texto.setStyleSheet("font-size: 12px; line-height: 1.6;")
        texto.setHtml("""
        <h2>💡 Dicas e Boas Práticas</h2>

        <h3>📊 Preparação das Planilhas</h3>
        <ul>
            <li>Certifique-se que as colunas têm os nomes: <b>CPF</b>, <b>Matrícula</b>, <b>Data de Admissão</b></li>
            <li>O sistema aceita variações: cpf, CPF, Cpf, etc.</li>
            <li>As colunas podem estar em qualquer ordem</li>
            <li>O sistema ignora linhas em branco automaticamente</li>
        </ul>

        <h3>🔒 Segurança</h3>
        <ul>
            <li>Os CPFs são mascarados nos relatórios</li>
            <li>Logs não contêm dados sensíveis</li>
            <li>Conforme LGPD - dados pessoais protegidos</li>
        </ul>

        <h3>⚡ Performance</h3>
        <ul>
            <li>Planilhas com até 100.000 linhas são suportadas</li>
            <li>O processamento é otimizado para grandes volumes</li>
        </ul>

        <h3>❓ Erros Comuns</h3>
        <ul>
            <li><b>CPF inválido:</b> O registro é ignorado e listado na aba "Erros"</li>
            <li><b>Data em formato diferente:</b> O sistema tenta interpretar automaticamente</li>
            <li><b>Matrícula com zeros:</b> Os zeros são preservados</li>
        </ul>
        """)
        layout.addWidget(texto)

        return widget

    def _criar_aba_sobre(self) -> QWidget:
        """Cria a aba 'Sobre'."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        texto = QTextEdit()
        texto.setReadOnly(True)
        texto.setStyleSheet("font-size: 12px; line-height: 1.8;")
        texto.setHtml(f"""
        <h2>ℹ️ Sobre o Comparador de Planilhas</h2>

        <p><b>Versão:</b> {__version__}</p>
        <p><b>Descrição:</b> Ferramenta para comparação segura de planilhas Excel</p>

        <h3>🎯 Objetivo</h3>
        <p>Comparar duas planilhas utilizando CPF, Matrícula e Data de Admissão como chaves,
        com foco em segurança de dados e conformidade com a LGPD.</p>

        <h3>🔧 Tecnologias</h3>
        <ul>
            <li><b>Python</b> 3.10+</li>
            <li><b>PyQt6</b> - Interface gráfica</li>
            <li><b>Pandas</b> - Processamento de dados</li>
            <li><b>OpenPyXL / xlrd</b> - Leitura de Excel</li>
            <li><b>Pydantic</b> - Validação de dados</li>
        </ul>

        <h3>📝 Licença</h3>
        <p>MIT License - Código aberto para uso comercial e pessoal</p>

        <h3>👨‍💻 Desenvolvedor</h3>
        <p>Douglas Lira</p>
        <p>📧 douglasliradafonseca.ds@gmail.com</p>
        """
        )
        layout.addWidget(texto)

        return widget