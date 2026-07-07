import streamlit as st
import pandas as pd

st.header("🧬 关键基因与分子分型")

gene_df = pd.read_csv("gene.csv")
subtype_df = pd.read_csv("subtype.csv")

st.subheader("📌 SCLC 核心驱动基因")

gene_display = gene_df[["gene_symbol", "description", "chromosome"]].rename(
    columns={
        "gene_symbol": "基因符号",
        "description": "功能描述",
        "chromosome": "染色体位置"
    }
)

search = st.text_input("🔍 搜索基因", placeholder="输入基因符号，如 TP53")

if search:
    result = gene_df[gene_df["gene_symbol"].str.contains(search.upper(), case=False, na=False)]
    if not result.empty:
        st.dataframe(
            result[["gene_symbol", "description", "chromosome", "source_url"]].rename(
                columns={
                    "gene_symbol": "基因符号",
                    "description": "功能描述",
                    "chromosome": "染色体位置",
                    "source_url": "来源链接"
                }
            ),
            use_container_width=True,
            hide_index=True,
            column_config={
                "来源链接": st.column_config.LinkColumn("来源链接")
            }
        )
    else:
        st.warning("未找到该基因，请检查拼写。")
else:
    st.dataframe(gene_display, use_container_width=True, hide_index=True)

st.divider()
st.subheader("📌 SCLC 分子分型 (A/N/P/I)")

subtype_display = subtype_df[[
    "subtype_name",
    "molecular_feature",
    "biological_feature",
    "representative_genes"
]].rename(
    columns={
        "subtype_name": "分型代号",
        "molecular_feature": "分子特征",
        "biological_feature": "生物学特征",
        "representative_genes": "代表性基因"
    }
)

st.dataframe(subtype_display, use_container_width=True, hide_index=True)