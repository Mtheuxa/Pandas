# Projetos em Python / Automações de Dados

Este diretório contém projetos de automação e processamento de dados desenvolvidos em Python, voltados para facilitar o trabalho com planilhas Excel e arquivos PDF.

O diretório está organizado em duas pastas/ferramentas principais:

---

## 1. Calculadora (`/Calculadora`)
Este módulo é focado em cálculos financeiros e apuração de fechamentos semanais.

**Arquivos Principais:**
* `calculadora_lucro.py`: Script principal que automatiza o cálculo de lucro e o fechamento financeiro com base em planilhas de registro.
* `Fechamento 11_18.xlsx` e `Fechamento semana 11 a 18.xlsx`: Planilhas que servem como base de dados (entrada/saída) para serem processadas pela calculadora.

**Resumo da Funcionalidade:**
O script em Python faz a leitura das planilhas brutas, realiza a matemática financeira necessária para calcular lucros e emite resultados precisos para facilitar o controle e fechamento da semana.

---

## 2. Ordem (`/Ordem`)
Este módulo é uma ferramenta de extração de texto e organização de dados em ordem alfabética. É muito útil para gerar listas de presença ou listas de turmas a partir de PDFs de sistemas.

**Arquivos Principais:**
* `ordem_alpha.py`: Script que usa as bibliotecas `pdfplumber` e `openpyxl` para ler o PDF, extrair e limpar nomes, organizar em ordem alfabética e exportar para Excel.
* `BIO 1P MANHÃ.pdf`: Documento em PDF servindo como arquivo de entrada original (exemplo de uma turma).
* `Turma_Formatada_v2.xlsx`: O resultado (saída) gerado pelo script, contendo os nomes perfeitamente organizados e formatados em uma planilha.

**Resumo da Funcionalidade:**
O programa entra no PDF e varre linha por linha, descartando cabeçalhos e informações indesejadas (como as palavras "curso:", "classe:", "série:"). Depois, ele pega apenas os nomes válidos (com limites de caracteres), coloca tudo em ordem alfabética e constrói uma planilha Excel com as colunas certinhas para uso.
