# 🛡️ Comparador de Planilhas

Ferramenta desktop para comparação de planilhas Excel com foco em **segurança de dados** e **LGPD**.

---

## 📋 Funcionalidades

- ✅ Comparação entre duas planilhas Excel (.xlsx, .xls)
- ✅ Chaves de comparação: CPF + Matrícula + Data de Admissão
- ✅ Identificação de divergências, registros únicos e erros
- ✅ Interface gráfica intuitiva (PyQt6)
- ✅ Validação de CPF com dígitos verificadores
- ✅ Normalização automática de dados
- ✅ Relatório detalhado em Excel
- ✅ Logs seguros (sem exposição de dados sensíveis)
- ✅ Executável portátil (.exe)

---

## 🔒 Segurança

- ✅ CPF validado com dígitos verificadores
- ✅ Logs sem exposição de dados sensíveis
- ✅ Mascaramento automático de CPF
- ✅ Sanitização de entradas
- ✅ Conformidade com LGPD

---

## 🚀 Como Executar

### Opção 1: Executável (Recomendado)

1. Baixe o arquivo `comparador.exe` da [página de releases](https://github.com/seu-usuario/comparador-planilhas/releases)
2. Execute o arquivo (não precisa instalar nada)

### Opção 2: Código Fonte

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/comparador-planilhas.git
cd comparador-planilhas

# Instale as dependências
pip install -r requirements.txt

# Execute a GUI
python src/main.py

# Ou execute a CLI
python src/cli.py planilhaA.xlsx planilhaB.xlsx
```

## 📊 Relatório Gerado

O relatório é gerado em formato Excel (.xlsx) com as seguintes abas:

| Aba | Conteúdo|
| Divergências | Registros com datas diferentes |
| Apenas na A | Registros apenas na Planilha A |
| Apenas na B | Registros apenas na Planilha B |
| Iguais | Registros idênticos |
| Erros | Registros ignorados |
| Resumo | Estatísticas da comparação |

## 📖 Documentação

- Requisitos

- Manual do Usuário

- Manual Técnico

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Com cobertura de código
pytest --cov=src
```

## 🤝 Contribuição

Leia o CONTRIBUTING.md para saber como contribuir.

## 📝 Licença

MIT License - veja o arquivo LICENSE para detalhes.

## 📧 Autor

Douglas Lira.