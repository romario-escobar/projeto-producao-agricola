# 🌾 Análise de Produção Agrícola no Brasil (2015–2024)

> Projeto G2 — Tema 29 | Disciplina: Linguagem de Programação — Análise e Visualização de Dados com Python

---

## 📋 Sobre o Projeto

Este projeto realiza uma análise exploratória completa dos dados de produção agrícola no Brasil entre **2015 e 2024**, investigando padrões de produção, regiões mais produtivas, impacto climático e desempenho das exportações.

O projeto é composto por:
- **Notebook Jupyter** com análise exploratória completa em 10 seções
- **Dashboard interativo** com 7 páginas temáticas construído com Streamlit e Plotly

---

## ❓ Perguntas Respondidas

- Quais estados apresentam maior produção agrícola?
- Quais culturas possuem maior produtividade?
- Houve crescimento da produção ao longo do tempo?
- Existe relação entre clima e produtividade?
- Quais regiões concentram maior área plantada?
- Quais culturas apresentam maior valor econômico?
- Como evoluíram as exportações agrícolas?

---

## 🚀 Tecnologias Utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python 3.11 | Linguagem principal |
| Pandas | Manipulação e análise dos dados |
| NumPy | Cálculos numéricos e correlações |
| Matplotlib | Gráficos estáticos do notebook |
| Seaborn | Heatmaps e visualizações do notebook |
| Plotly | Gráficos interativos do dashboard |
| Streamlit | Dashboard web interativo multipágina |
| GitHub | Controle de versão e publicação |

---

## 📊 Funcionalidades do Dashboard

- 7 páginas temáticas com navegação lateral
- 6 filtros simultâneos: ano, mês, região, estado, cultura e nível de produtividade
- KPIs dinâmicos que se atualizam conforme os filtros
- Gráficos interativos com zoom, hover e exportação
- Tabela dinâmica com ordenação e download dos dados filtrados
- Conclusão executiva automatizada

---

## 🗂️ Estrutura do Projeto

```
projeto-producao-agricola/
│
├── app.py                    → Dashboard Streamlit
├── requirements.txt          → Dependências do projeto
├── README.md                 → Este arquivo
├── index.html                → Página GitHub Pages
│
├── dados/
│   └── simulacao_producao_agricola_brasil.csv
│
├── notebooks/
│   └── analise_producao_agricola.ipynb
│
├── imagens/
│   ├── 01_evolucao_producao.png
│   ├── 02_producao_por_cultura.png
│   ├── 03_ranking_estados.png
│   ├── 04_heatmap_sazonal.png
│   ├── 05_dispersao_chuva_produtividade.png
│   ├── 06_comparacao_regional.png
│   ├── 07_matriz_correlacao.png
│   ├── 08_evolucao_exportacoes.png
│   ├── 09_produtividade.png
│   └── 10_clima_por_regiao.png
│
└── database/
```

---

## ⚙️ Como Executar Localmente

**1. Clone o repositório:**
```bash
git clone https://github.com/SEU_USUARIO/projeto-producao-agricola.git
cd projeto-producao-agricola
```

**2. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**3. Execute o dashboard:**
```bash
streamlit run app.py
```

**4. Abra o notebook:**

Abra o VSCode, navegue até `notebooks/analise_producao_agricola.ipynb` e execute as células.

---

## 🔗 Links

| Plataforma | Link |
|---|---|
| GitHub | *(este repositório)* |
| GitHub Pages | *(a preencher após publicação)* |
| Streamlit Cloud | *(a preencher após publicação)* |

---

## 📁 Base de Dados

**Arquivo:** `simulacao_producao_agricola_brasil.csv`  
**Período:** 2015 a 2024  
**Registros:** 4.441 linhas  
**Granularidade:** Mensal por estado e cultura agrícola  

| Coluna | Descrição |
|---|---|
| ano / mes / data | Referência temporal |
| regiao / uf | Localização geográfica |
| cultura | Tipo de cultura agrícola |
| area_plantada_ha | Área em hectares |
| producao_toneladas | Volume produzido |
| produtividade | Produção por hectare (t/ha) |
| chuva_mm | Precipitação em mm |
| temperatura_media | Temperatura em °C |
| valor_producao | Valor econômico em R$ |
| exportacoes | Volume exportado em toneladas |
| nivel_produtividade | Baixo / Médio / Alto / Muito Alto |

---

*Desenvolvido com Python + Streamlit + Plotly*
