# =============================================================================
# PROJETO G2 — ANÁLISE DE PRODUÇÃO AGRÍCOLA NO BRASIL
# Dashboard Streamlit — app.py
# =============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# =============================================================================
# CONFIGURAÇÃO DA PÁGINA
# Deve ser o PRIMEIRO comando Streamlit do arquivo
# =============================================================================
st.set_page_config(
    page_title="Produção Agrícola no Brasil",
    page_icon="🌾",
    layout="wide",                  # Usa toda a largura da tela
    initial_sidebar_state="expanded"
)

# =============================================================================
# ESTILO VISUAL PERSONALIZADO (CSS)
# Deixa o dashboard mais bonito
# =============================================================================
st.markdown("""
    <style>
        /* Fundo geral */
        .main { background-color: #f5f7f2; }

        /* Cards de KPI */
        .kpi-card {
            background: linear-gradient(135deg, #1b4332, #2d6a4f);
            border-radius: 12px;
            padding: 20px;
            color: white;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .kpi-value {
            font-size: 28px;
            font-weight: bold;
            margin: 8px 0;
        }
        .kpi-label {
            font-size: 13px;
            opacity: 0.85;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* Título principal */
        h1 { color: #1b4332; }

        /* Subtítulos de seção */
        h2, h3 { color: #2d6a4f; border-bottom: 2px solid #95d5b2; padding-bottom: 6px; }

        /* Caixa de interpretação */
        .interpretacao {
            background: #d8f3dc;
            border-left: 5px solid #2d6a4f;
            border-radius: 8px;
            padding: 16px 20px;
            margin: 10px 0;
            color: #1b4332;
        }
    </style>
""", unsafe_allow_html=True)


# =============================================================================
# CARREGAMENTO DOS DADOS
# @st.cache_data faz o arquivo ser lido só uma vez (mais rápido)
# =============================================================================
@st.cache_data
def carregar_dados():
    df = pd.read_csv("dados/simulacao_producao_agricola_brasil.csv", encoding="utf-8-sig")

    # Garante que a coluna data seja do tipo datetime
    df["data"] = pd.to_datetime(df["data"])

    # Remove linhas completamente vazias
    df.dropna(how="all", inplace=True)

    # Preenche valores nulos numéricos com 0
    colunas_numericas = [
        "area_plantada_ha", "producao_toneladas", "produtividade",
        "chuva_mm", "temperatura_media", "valor_producao", "exportacoes"
    ]
    df[colunas_numericas] = df[colunas_numericas].fillna(0)

    # Garante que ano e mes são inteiros
    df["ano"] = df["ano"].astype(int)
    df["mes"] = df["mes"].astype(int)

    # Cria coluna de nome do mês para visualizações
    meses_nomes = {
        1:"Janeiro", 2:"Fevereiro", 3:"Março", 4:"Abril",
        5:"Maio", 6:"Junho", 7:"Julho", 8:"Agosto",
        9:"Setembro", 10:"Outubro", 11:"Novembro", 12:"Dezembro"
    }
    df["nome_mes"] = df["mes"].map(meses_nomes)

    return df

df_original = carregar_dados()


# =============================================================================
# NAVEGAÇÃO — MENU DE PÁGINAS (Dashboard Multipágina)
# =============================================================================
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Brazil.svg/320px-Flag_of_Brazil.svg.png",
    width=120
)
st.sidebar.title("🌾 Agro Dashboard")
st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "Navegação",
    [
        "🏠 Visão Geral",
        "📈 Evolução Temporal",
        "🗺️ Análise Regional",
        "🌱 Análise por Cultura",
        "🌧️ Clima x Produtividade",
        "📊 Exportações",
        "🔍 Exploração de Dados",
    ]
)

st.sidebar.markdown("---")

# =============================================================================
# FILTROS GLOBAIS (ficam na barra lateral)
# Todos os filtros são aplicados em todas as páginas
# =============================================================================
st.sidebar.subheader("⚙️ Filtros")

# Filtro de Ano
anos_disponiveis = sorted(df_original["ano"].unique())
anos_selecionados = st.sidebar.multiselect(
    "Ano", anos_disponiveis, default=anos_disponiveis
)

# Filtro de Mês
meses_disponiveis = sorted(df_original["mes"].unique())
meses_selecionados = st.sidebar.multiselect(
    "Mês (número)", meses_disponiveis, default=meses_disponiveis
)

# Filtro de Região
regioes_disponiveis = sorted(df_original["regiao"].unique())
regioes_selecionadas = st.sidebar.multiselect(
    "Região", regioes_disponiveis, default=regioes_disponiveis
)

# Filtro de Estado (depende da região selecionada)
estados_filtrados = df_original[df_original["regiao"].isin(regioes_selecionadas)]["uf"].unique()
estados_selecionados = st.sidebar.multiselect(
    "Estado (UF)", sorted(estados_filtrados), default=sorted(estados_filtrados)
)

# Filtro de Cultura
culturas_disponiveis = sorted(df_original["cultura"].unique())
culturas_selecionadas = st.sidebar.multiselect(
    "Cultura", culturas_disponiveis, default=culturas_disponiveis
)

# Filtro de Nível de Produtividade
niveis_disponiveis = df_original["nivel_produtividade"].unique().tolist()
niveis_selecionados = st.sidebar.multiselect(
    "Nível de Produtividade", niveis_disponiveis, default=niveis_disponiveis
)

# =============================================================================
# APLICAÇÃO DOS FILTROS NO DATAFRAME
# =============================================================================
df = df_original[
    (df_original["ano"].isin(anos_selecionados)) &
    (df_original["mes"].isin(meses_selecionados)) &
    (df_original["regiao"].isin(regioes_selecionadas)) &
    (df_original["uf"].isin(estados_selecionados)) &
    (df_original["cultura"].isin(culturas_selecionadas)) &
    (df_original["nivel_produtividade"].isin(niveis_selecionados))
].copy()

# Avisa se não houver dados após filtragem
if df.empty:
    st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados. Ajuste os filtros na barra lateral.")
    st.stop()

# =============================================================================
# FUNÇÃO AUXILIAR — FORMATAR NÚMEROS GRANDES
# =============================================================================
def formatar_numero(n):
    if n >= 1_000_000_000:
        return f"{n/1_000_000_000:.1f} Bi"
    elif n >= 1_000_000:
        return f"{n/1_000_000:.1f} Mi"
    elif n >= 1_000:
        return f"{n/1_000:.1f} Mil"
    else:
        return f"{n:.1f}"

# =============================================================================
# CÁLCULO DOS KPIs GLOBAIS
# =============================================================================
total_producao      = df["producao_toneladas"].sum()
total_area          = df["area_plantada_ha"].sum()
total_valor         = df["valor_producao"].sum()
total_exportacoes   = df["exportacoes"].sum()
media_produtividade = df["produtividade"].mean()
cultura_top         = df.groupby("cultura")["producao_toneladas"].sum().idxmax()
estado_top          = df.groupby("uf")["producao_toneladas"].sum().idxmax()


# =============================================================================
#
#  ██████╗  █████╗  ██████╗ ██╗███╗   ██╗ █████╗ ███████╗
#  ██╔══██╗██╔══██╗██╔════╝ ██║████╗  ██║██╔══██╗██╔════╝
#  ██████╔╝███████║██║  ███╗██║██╔██╗ ██║███████║███████╗
#  ██╔═══╝ ██╔══██║██║   ██║██║██║╚██╗██║██╔══██║╚════██║
#  ██║     ██║  ██║╚██████╔╝██║██║ ╚████║██║  ██║███████║
#  ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝
#
# =============================================================================

# ─────────────────────────────────────────────────────────────────────────────
# PÁGINA 1 — VISÃO GERAL
# ─────────────────────────────────────────────────────────────────────────────
if pagina == "🏠 Visão Geral":

    st.title("🌾 Análise de Produção Agrícola no Brasil")
    st.markdown(
        "**Período:** 2015–2024 | **Fonte:** Dataset Simulado — Projeto G2 | "
        "**Disciplina:** Linguagem de Programação — Análise e Visualização de Dados com Python"
    )
    st.markdown("---")

    # Descrição do problema
    st.markdown("""
    <div class="interpretacao">
    O agronegócio é um dos pilares da economia brasileira, respondendo por parcela expressiva
    do PIB nacional, das exportações e da geração de empregos. Este dashboard analisa os dados
    de produção agrícola do Brasil entre 2015 e 2024, investigando culturas, regiões, tendências
    climáticas e desempenho econômico do setor.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📌 KPIs — Indicadores-Chave")

    # ── Linha de KPIs ─────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)

    kpis = [
        (c1, "🌾 Produção Total",       f"{formatar_numero(total_producao)} ton"),
        (c2, "🏆 Cultura Líder",         cultura_top),
        (c3, "📍 Estado Líder",          estado_top),
        (c4, "🌍 Área Plantada",         f"{formatar_numero(total_area)} ha"),
        (c5, "💰 Valor Econômico",       f"R$ {formatar_numero(total_valor)}"),
        (c6, "✈️ Exportações",           f"{formatar_numero(total_exportacoes)} ton"),
        (c7, "⚡ Produtividade Média",   f"{media_produtividade:.1f} t/ha"),
    ]

    for col, label, value in kpis:
        col.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Gráficos de resumo ────────────────────────────────────────────────────
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### Produção por Região")
        prod_regiao = df.groupby("regiao")["producao_toneladas"].sum().reset_index()
        prod_regiao = prod_regiao.sort_values("producao_toneladas", ascending=True)
        fig = px.bar(
            prod_regiao, x="producao_toneladas", y="regiao", orientation="h",
            color="producao_toneladas", color_continuous_scale="Greens",
            labels={"producao_toneladas": "Produção (ton)", "regiao": "Região"},
            template="plotly_white"
        )
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig, width="stretch")

    with col_b:
        st.markdown("### Distribuição por Cultura")
        prod_cultura = df.groupby("cultura")["producao_toneladas"].sum().reset_index()
        fig2 = px.pie(
            prod_cultura, values="producao_toneladas", names="cultura",
            color_discrete_sequence=px.colors.sequential.Greens[::-1],
            template="plotly_white", hole=0.4
        )
        fig2.update_traces(textposition="outside", textinfo="percent+label")
        st.plotly_chart(fig2, width="stretch")

    # ── Interpretação ─────────────────────────────────────────────────────────
    st.markdown("### 📝 Interpretação dos Resultados")
    regiao_lider = df.groupby("regiao")["producao_toneladas"].sum().idxmax()
    st.markdown(f"""
    <div class="interpretacao">
    Com base nos filtros aplicados, a cultura com maior volume total de produção é
    <b>{cultura_top}</b>, e o estado de maior destaque é <b>{estado_top}</b>.
    A região <b>{regiao_lider}</b> concentra o maior volume produtivo do período analisado.
    A produtividade média atingiu <b>{media_produtividade:.1f} t/ha</b>, e o valor econômico
    total da produção somou <b>R$ {formatar_numero(total_valor)}</b>, evidenciando a relevância
    estratégica do agronegócio brasileiro.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PÁGINA 2 — EVOLUÇÃO TEMPORAL
# ─────────────────────────────────────────────────────────────────────────────
elif pagina == "📈 Evolução Temporal":

    st.title("📈 Evolução Temporal da Produção Agrícola")
    st.markdown("Análise da trajetória de produção, área plantada e valor econômico ao longo dos anos.")
    st.markdown("---")

    # ── Linha de produção por ano ─────────────────────────────────────────────
    st.markdown("### Produção Total por Ano")
    prod_ano = df.groupby("ano")["producao_toneladas"].sum().reset_index()
    fig = px.line(
        prod_ano, x="ano", y="producao_toneladas",
        markers=True, line_shape="spline",
        labels={"ano": "Ano", "producao_toneladas": "Produção (toneladas)"},
        template="plotly_white", color_discrete_sequence=["#2d6a4f"]
    )
    fig.update_traces(line_width=3, marker_size=8)
    fig.update_xaxes(dtick=1)
    st.plotly_chart(fig, width="stretch")

    # ── Produção por ano e cultura ────────────────────────────────────────────
    st.markdown("### Produção por Ano e Cultura")
    prod_ano_cult = df.groupby(["ano", "cultura"])["producao_toneladas"].sum().reset_index()
    fig2 = px.line(
        prod_ano_cult, x="ano", y="producao_toneladas", color="cultura",
        markers=True, line_shape="spline",
        labels={"ano": "Ano", "producao_toneladas": "Produção (ton)", "cultura": "Cultura"},
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig2.update_traces(line_width=2, marker_size=6)
    fig2.update_xaxes(dtick=1)
    st.plotly_chart(fig2, width="stretch")

    # ── Heatmap sazonal ────────────────────────────────────────────────────────
    st.markdown("### 🗓️ Heatmap Sazonal — Produção por Mês e Ano")
    heat = df.groupby(["ano", "mes"])["producao_toneladas"].sum().reset_index()
    heat_pivot = heat.pivot(index="mes", columns="ano", values="producao_toneladas")

    meses_nomes = {
        1:"Jan", 2:"Fev", 3:"Mar", 4:"Abr", 5:"Mai", 6:"Jun",
        7:"Jul", 8:"Ago", 9:"Set", 10:"Out", 11:"Nov", 12:"Dez"
    }
    heat_pivot.index = [meses_nomes.get(m, m) for m in heat_pivot.index]

    fig3 = go.Figure(data=go.Heatmap(
        z=heat_pivot.values,
        x=[str(c) for c in heat_pivot.columns],
        y=heat_pivot.index,
        colorscale="Greens",
        colorbar=dict(title="Produção (ton)")
    ))
    fig3.update_layout(
        xaxis_title="Ano", yaxis_title="Mês",
        template="plotly_white", height=420
    )
    st.plotly_chart(fig3, width="stretch")

    # ── Interpretação ─────────────────────────────────────────────────────────
    ano_pico = prod_ano.loc[prod_ano["producao_toneladas"].idxmax(), "ano"]
    st.markdown(f"""
    <div class="interpretacao">
    A análise temporal revela a trajetória da produção agrícola brasileira ao longo do período
    2015–2024. O heatmap sazonal evidencia os meses de maior intensidade produtiva, permitindo
    identificar <b>padrões sazonais</b> e possíveis impactos climáticos ao longo do calendário
    agrícola. O ano de <b>{ano_pico}</b> registrou o maior volume de produção no período filtrado.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PÁGINA 3 — ANÁLISE REGIONAL
# ─────────────────────────────────────────────────────────────────────────────
elif pagina == "🗺️ Análise Regional":

    st.title("🗺️ Análise Regional da Produção Agrícola")
    st.markdown("Comparação de desempenho produtivo entre regiões e estados brasileiros.")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Produção por Região")
        prod_reg = df.groupby("regiao")["producao_toneladas"].sum().reset_index()
        prod_reg = prod_reg.sort_values("producao_toneladas", ascending=False)
        fig = px.bar(
            prod_reg, x="regiao", y="producao_toneladas",
            color="producao_toneladas", color_continuous_scale="Greens",
            labels={"regiao": "Região", "producao_toneladas": "Produção (ton)"},
            template="plotly_white", text_auto=".2s"
        )
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig, width="stretch")

    with col2:
        st.markdown("### Área Plantada por Região")
        area_reg = df.groupby("regiao")["area_plantada_ha"].sum().reset_index()
        area_reg = area_reg.sort_values("area_plantada_ha", ascending=False)
        fig2 = px.bar(
            area_reg, x="regiao", y="area_plantada_ha",
            color="area_plantada_ha", color_continuous_scale="Teal",
            labels={"regiao": "Região", "area_plantada_ha": "Área (ha)"},
            template="plotly_white", text_auto=".2s"
        )
        fig2.update_coloraxes(showscale=False)
        st.plotly_chart(fig2, width="stretch")

    # ── Ranking de estados ─────────────────────────────────────────────────────
    st.markdown("### 🏆 Ranking de Estados Produtores (Top 15)")
    top_estados = (
        df.groupby("uf")["producao_toneladas"]
        .sum()
        .reset_index()
        .sort_values("producao_toneladas", ascending=True)
        .tail(15)
    )
    fig3 = px.bar(
        top_estados, x="producao_toneladas", y="uf", orientation="h",
        color="producao_toneladas", color_continuous_scale="Greens",
        labels={"uf": "Estado", "producao_toneladas": "Produção (ton)"},
        template="plotly_white", text_auto=".2s"
    )
    fig3.update_coloraxes(showscale=False)
    st.plotly_chart(fig3, width="stretch")

    # ── Valor econômico por estado ─────────────────────────────────────────────
    st.markdown("### 💰 Valor Econômico por Estado (Top 15)")
    top_valor = (
        df.groupby("uf")["valor_producao"]
        .sum()
        .reset_index()
        .sort_values("valor_producao", ascending=True)
        .tail(15)
    )
    fig4 = px.bar(
        top_valor, x="valor_producao", y="uf", orientation="h",
        color="valor_producao", color_continuous_scale="YlGn",
        labels={"uf": "Estado", "valor_producao": "Valor (R$)"},
        template="plotly_white", text_auto=".2s"
    )
    fig4.update_coloraxes(showscale=False)
    st.plotly_chart(fig4, width="stretch")

    # ── Interpretação ─────────────────────────────────────────────────────────
    regiao_lider = df.groupby("regiao")["producao_toneladas"].sum().idxmax()
    st.markdown(f"""
    <div class="interpretacao">
    A análise regional demonstra que a <b>{regiao_lider}</b> concentra o maior volume de
    produção agrícola no período selecionado. O ranking de estados reflete a concentração
    da produção em determinados polos agroindustriais, evidenciando desigualdades regionais
    e oportunidades de desenvolvimento em estados com menor participação no total nacional.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PÁGINA 4 — ANÁLISE POR CULTURA
# ─────────────────────────────────────────────────────────────────────────────
elif pagina == "🌱 Análise por Cultura":

    st.title("🌱 Análise por Cultura Agrícola")
    st.markdown("Comparação de produção, produtividade e valor econômico entre as culturas.")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Produção Total por Cultura")
        prod_cult = (
            df.groupby("cultura")["producao_toneladas"]
            .sum().reset_index()
            .sort_values("producao_toneladas", ascending=False)
        )
        fig = px.bar(
            prod_cult, x="cultura", y="producao_toneladas",
            color="cultura", color_discrete_sequence=px.colors.qualitative.Set2,
            labels={"cultura": "Cultura", "producao_toneladas": "Produção (ton)"},
            template="plotly_white", text_auto=".2s"
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width="stretch")

    with col2:
        st.markdown("### Valor Econômico por Cultura")
        val_cult = (
            df.groupby("cultura")["valor_producao"]
            .sum().reset_index()
            .sort_values("valor_producao", ascending=False)
        )
        fig2 = px.bar(
            val_cult, x="cultura", y="valor_producao",
            color="cultura", color_discrete_sequence=px.colors.qualitative.Pastel,
            labels={"cultura": "Cultura", "valor_producao": "Valor (R$)"},
            template="plotly_white", text_auto=".2s"
        )
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, width="stretch")

    # ── Produtividade média por cultura ────────────────────────────────────────
    st.markdown("### ⚡ Produtividade Média por Cultura (t/ha)")
    prod_media = (
        df.groupby("cultura")["produtividade"]
        .mean().reset_index()
        .sort_values("produtividade", ascending=False)
    )
    fig3 = px.bar(
        prod_media, x="cultura", y="produtividade",
        color="produtividade", color_continuous_scale="Greens",
        labels={"cultura": "Cultura", "produtividade": "Produtividade Média (t/ha)"},
        template="plotly_white", text_auto=".1f"
    )
    fig3.update_coloraxes(showscale=False)
    st.plotly_chart(fig3, width="stretch")

    # ── Evolução por cultura ao longo dos anos ────────────────────────────────
    st.markdown("### Evolução da Produção por Cultura ao Longo dos Anos")
    ev_cult = df.groupby(["ano", "cultura"])["producao_toneladas"].sum().reset_index()
    fig4 = px.area(
        ev_cult, x="ano", y="producao_toneladas", color="cultura",
        labels={"ano": "Ano", "producao_toneladas": "Produção (ton)", "cultura": "Cultura"},
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig4.update_xaxes(dtick=1)
    st.plotly_chart(fig4, width="stretch")

    # ── Nível de produtividade ─────────────────────────────────────────────────
    st.markdown("### Distribuição do Nível de Produtividade por Cultura")
    nivel_cult = df.groupby(["cultura", "nivel_produtividade"]).size().reset_index(name="contagem")
    ordem_nivel = ["Baixo", "Médio", "Alto", "Muito Alto"]
    fig5 = px.bar(
        nivel_cult, x="cultura", y="contagem", color="nivel_produtividade",
        barmode="stack",
        category_orders={"nivel_produtividade": ordem_nivel},
        labels={"cultura": "Cultura", "contagem": "Registros", "nivel_produtividade": "Nível"},
        template="plotly_white",
        color_discrete_sequence=["#d9ed92", "#b7e4c7", "#52b788", "#1b4332"]
    )
    st.plotly_chart(fig5, width="stretch")

    # ── Interpretação ─────────────────────────────────────────────────────────
    cultura_valor = val_cult.iloc[0]["cultura"]
    st.markdown(f"""
    <div class="interpretacao">
    A análise por cultura evidencia diferenças significativas de produtividade e valor econômico
    entre as principais culturas brasileiras. A cultura <b>{cultura_top}</b> lidera em volume de
    produção, enquanto <b>{cultura_valor}</b> apresenta o maior valor econômico agregado no período.
    A distribuição dos níveis de produtividade revela quais culturas operam com maior eficiência
    produtiva e onde há espaço para melhoria tecnológica.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PÁGINA 5 — CLIMA X PRODUTIVIDADE
# ─────────────────────────────────────────────────────────────────────────────
elif pagina == "🌧️ Clima x Produtividade":

    st.title("🌧️ Impacto Climático na Produtividade Agrícola")
    st.markdown("Relação entre precipitação, temperatura e eficiência produtiva das culturas.")
    st.markdown("---")

    # ── Dispersão chuva x produtividade ───────────────────────────────────────
    st.markdown("### Dispersão: Chuva × Produtividade")
    # Amostra para não sobrecarregar o gráfico
    amostra = df.sample(min(1500, len(df)), random_state=42)
    fig = px.scatter(
        amostra, x="chuva_mm", y="produtividade",
        color="cultura", size="area_plantada_ha",
        size_max=20, opacity=0.7,
        hover_data=["uf", "ano", "nivel_produtividade"],
        labels={
            "chuva_mm": "Chuva (mm)",
            "produtividade": "Produtividade (t/ha)",
            "cultura": "Cultura"
        },
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    # Linha de tendência geral
    z = np.polyfit(amostra["chuva_mm"], amostra["produtividade"], 1)
    p = np.poly1d(z)
    x_line = np.linspace(amostra["chuva_mm"].min(), amostra["chuva_mm"].max(), 100)
    fig.add_trace(go.Scatter(
        x=x_line, y=p(x_line),
        mode="lines", name="Tendência",
        line=dict(color="red", width=2, dash="dash")
    ))
    st.plotly_chart(fig, width="stretch")

    # ── Temperatura x produtividade ────────────────────────────────────────────
    st.markdown("### Dispersão: Temperatura × Produtividade")
    fig2 = px.scatter(
        amostra, x="temperatura_media", y="produtividade",
        color="regiao", opacity=0.7,
        hover_data=["uf", "cultura", "ano"],
        labels={
            "temperatura_media": "Temperatura Média (°C)",
            "produtividade": "Produtividade (t/ha)",
            "regiao": "Região"
        },
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    st.plotly_chart(fig2, width="stretch")

    # ── Correlação estatística ─────────────────────────────────────────────────
    st.markdown("### 🔗 Matriz de Correlação Estatística")
    colunas_corr = [
        "producao_toneladas", "produtividade", "area_plantada_ha",
        "chuva_mm", "temperatura_media", "valor_producao", "exportacoes"
    ]
    corr = df[colunas_corr].corr().round(2)

    # Nomes mais amigáveis para exibir
    nomes_amigaveis = {
        "producao_toneladas": "Produção",
        "produtividade": "Produtividade",
        "area_plantada_ha": "Área Plantada",
        "chuva_mm": "Chuva (mm)",
        "temperatura_media": "Temperatura",
        "valor_producao": "Valor Econômico",
        "exportacoes": "Exportações"
    }
    corr.rename(index=nomes_amigaveis, columns=nomes_amigaveis, inplace=True)

    fig3 = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns.tolist(),
        y=corr.index.tolist(),
        colorscale="RdYlGn",
        zmin=-1, zmax=1,
        text=corr.values,
        texttemplate="%{text:.2f}",
        colorbar=dict(title="Correlação")
    ))
    fig3.update_layout(template="plotly_white", height=450)
    st.plotly_chart(fig3, width="stretch")

    # ── Chuva média por mês ────────────────────────────────────────────────────
    st.markdown("### Precipitação Média por Mês")
    chuva_mes = df.groupby("mes")["chuva_mm"].mean().reset_index()
    meses_nomes = {
        1:"Jan", 2:"Fev", 3:"Mar", 4:"Abr", 5:"Mai", 6:"Jun",
        7:"Jul", 8:"Ago", 9:"Set", 10:"Out", 11:"Nov", 12:"Dez"
    }
    chuva_mes["nome_mes"] = chuva_mes["mes"].map(meses_nomes)
    fig4 = px.bar(
        chuva_mes, x="nome_mes", y="chuva_mm",
        color="chuva_mm", color_continuous_scale="Blues",
        labels={"nome_mes": "Mês", "chuva_mm": "Chuva Média (mm)"},
        template="plotly_white"
    )
    fig4.update_coloraxes(showscale=False)
    st.plotly_chart(fig4, width="stretch")

    # ── Interpretação ─────────────────────────────────────────────────────────
    corr_chuva = df["chuva_mm"].corr(df["produtividade"])
    corr_temp  = df["temperatura_media"].corr(df["produtividade"])
    st.markdown(f"""
    <div class="interpretacao">
    A correlação entre chuva e produtividade é de <b>{corr_chuva:.2f}</b>, indicando
    {'uma relação positiva moderada' if corr_chuva > 0.3 else 'uma relação fraca ou ausente'}.
    Já a correlação com temperatura é de <b>{corr_temp:.2f}</b>. A matriz de correlação permite
    identificar quais variáveis têm maior influência sobre a produtividade agrícola, informação
    essencial para o planejamento de safras e políticas agrícolas.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PÁGINA 6 — EXPORTAÇÕES
# ─────────────────────────────────────────────────────────────────────────────
elif pagina == "📊 Exportações":

    st.title("📊 Análise das Exportações Agrícolas")
    st.markdown("Volume exportado por cultura, estado e evolução ao longo do tempo.")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Exportações por Cultura")
        exp_cult = (
            df.groupby("cultura")["exportacoes"]
            .sum().reset_index()
            .sort_values("exportacoes", ascending=False)
        )
        fig = px.bar(
            exp_cult, x="cultura", y="exportacoes",
            color="cultura", color_discrete_sequence=px.colors.qualitative.Set3,
            labels={"cultura": "Cultura", "exportacoes": "Exportações (ton)"},
            template="plotly_white", text_auto=".2s"
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width="stretch")

    with col2:
        st.markdown("### Exportações por Região")
        exp_reg = (
            df.groupby("regiao")["exportacoes"]
            .sum().reset_index()
            .sort_values("exportacoes", ascending=False)
        )
        fig2 = px.pie(
            exp_reg, values="exportacoes", names="regiao", hole=0.4,
            color_discrete_sequence=px.colors.sequential.Greens[::-1],
            template="plotly_white"
        )
        fig2.update_traces(textposition="outside", textinfo="percent+label")
        st.plotly_chart(fig2, width="stretch")

    # ── Evolução exportações ───────────────────────────────────────────────────
    st.markdown("### Evolução das Exportações por Ano")
    exp_ano = df.groupby(["ano", "cultura"])["exportacoes"].sum().reset_index()
    fig3 = px.line(
        exp_ano, x="ano", y="exportacoes", color="cultura",
        markers=True, line_shape="spline",
        labels={"ano": "Ano", "exportacoes": "Exportações (ton)", "cultura": "Cultura"},
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig3.update_xaxes(dtick=1)
    st.plotly_chart(fig3, width="stretch")

    # ── Top 10 estados exportadores ────────────────────────────────────────────
    st.markdown("### 🏆 Top 10 Estados Exportadores")
    top_exp_uf = (
        df.groupby("uf")["exportacoes"]
        .sum().reset_index()
        .sort_values("exportacoes", ascending=True)
        .tail(10)
    )
    fig4 = px.bar(
        top_exp_uf, x="exportacoes", y="uf", orientation="h",
        color="exportacoes", color_continuous_scale="Teal",
        labels={"uf": "Estado", "exportacoes": "Exportações (ton)"},
        template="plotly_white", text_auto=".2s"
    )
    fig4.update_coloraxes(showscale=False)
    st.plotly_chart(fig4, width="stretch")

    # ── Interpretação ─────────────────────────────────────────────────────────
    cultura_exp_lider = exp_cult.iloc[0]["cultura"]
    st.markdown(f"""
    <div class="interpretacao">
    As exportações agrícolas demonstram a inserção do Brasil no mercado global de commodities.
    A cultura <b>{cultura_exp_lider}</b> lidera o volume exportado, refletindo a competitividade
    do agronegócio brasileiro no comércio internacional. O acompanhamento da evolução anual
    das exportações permite identificar ciclos e oportunidades para expansão do mercado externo.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PÁGINA 7 — EXPLORAÇÃO DE DADOS
# ─────────────────────────────────────────────────────────────────────────────
elif pagina == "🔍 Exploração de Dados":

    st.title("🔍 Exploração Detalhada dos Dados")
    st.markdown("Tabela dinâmica, estatísticas descritivas e conclusão executiva.")
    st.markdown("---")

    # ── Estatísticas descritivas ───────────────────────────────────────────────
    st.markdown("### 📊 Estatísticas Descritivas")
    colunas_stats = [
        "producao_toneladas", "area_plantada_ha", "produtividade",
        "chuva_mm", "temperatura_media", "valor_producao", "exportacoes"
    ]
    stats = df[colunas_stats].describe().T.round(2)
    stats.index = [
        "Produção (ton)", "Área Plantada (ha)", "Produtividade (t/ha)",
        "Chuva (mm)", "Temperatura (°C)", "Valor Econômico (R$)", "Exportações (ton)"
    ]
    st.dataframe(stats, width="stretch")

    # ── Tabela dinâmica ────────────────────────────────────────────────────────
    st.markdown("### 📋 Tabela Dinâmica — Exploração Completa")

    # Permite ao usuário escolher quantas linhas ver
    n_linhas = st.slider("Número de registros a exibir", 10, 500, 50, step=10)

    colunas_exibir = [
        "ano", "mes", "regiao", "uf", "cultura",
        "area_plantada_ha", "producao_toneladas", "produtividade",
        "chuva_mm", "temperatura_media", "valor_producao",
        "exportacoes", "nivel_produtividade"
    ]

    # Ordenação
    col_ordem = st.selectbox("Ordenar por:", colunas_exibir, index=6)
    ordem_asc = st.radio("Ordem:", ["Decrescente", "Crescente"]) == "Crescente"

    tabela = (
        df[colunas_exibir]
        .sort_values(col_ordem, ascending=ordem_asc)
        .head(n_linhas)
        .reset_index(drop=True)
    )
    st.dataframe(tabela, width="stretch")

    # ── Download dos dados filtrados ───────────────────────────────────────────
    csv_download = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button(
        label="⬇️ Baixar dados filtrados como CSV",
        data=csv_download,
        file_name="dados_filtrados.csv",
        mime="text/csv"
    )

    st.markdown("---")

    # ── Conclusão Executiva ────────────────────────────────────────────────────
    st.markdown("### 🎯 Conclusão Executiva")

    regiao_lider    = df.groupby("regiao")["producao_toneladas"].sum().idxmax()
    cultura_exp_top = df.groupby("cultura")["exportacoes"].sum().idxmax()
    ano_melhor      = df.groupby("ano")["producao_toneladas"].sum().idxmax()

    st.markdown(f"""
    <div class="interpretacao">
    <b>Conclusão Executiva — Análise de Produção Agrícola no Brasil (2015–2024)</b><br><br>

    A análise dos dados de produção agrícola brasileira revela um setor dinâmico e estratégico
    para a economia nacional. Os principais achados são:<br><br>

    🌾 <b>Produção Total:</b> {formatar_numero(total_producao)} toneladas no período analisado.<br>
    🏆 <b>Cultura Líder:</b> {cultura_top} concentra o maior volume de produção.<br>
    📍 <b>Estado Destaque:</b> {estado_top} é o maior produtor individual.<br>
    🌍 <b>Região Dominante:</b> {regiao_lider} concentra a maior produção regional.<br>
    ✈️ <b>Exportações:</b> {cultura_exp_top} é a principal cultura exportada.<br>
    📅 <b>Melhor Ano:</b> {ano_melhor} registrou o maior volume produtivo.<br>
    💰 <b>Valor Econômico Total:</b> R$ {formatar_numero(total_valor)}.<br>
    ⚡ <b>Produtividade Média:</b> {media_produtividade:.1f} t/ha.<br><br>

    O setor agrícola brasileiro demonstra crescimento consistente, com diversificação de culturas
    e expansão das exportações. O impacto climático, especialmente da precipitação, é fator
    determinante na variação da produtividade. Regiões com maior infraestrutura logística
    tendem a apresentar melhor desempenho econômico na cadeia produtiva.
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# RODAPÉ
# =============================================================================
st.markdown("---")
st.markdown(
    "<center><small>🌾 Projeto G2 — Análise de Produção Agrícola no Brasil | "
    "Desenvolvido com Python + Streamlit + Plotly</small></center>",
    unsafe_allow_html=True
)
