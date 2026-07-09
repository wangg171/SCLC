import streamlit as st
import pandas as pd

st.header("🔗 SCLC 知识图谱")

st.image("graph.png", caption="SCLC 分子分型与关键基因-通路-治疗关联图")

st.divider()

st.subheader("📋 基因-通路关联表")

pathway_df = pd.read_csv("pathway.csv")

pathway_display = pathway_df[[
    "gene_symbol",
    "pathway_name",
    "pathway_category",
    "biological_meaning"
]].rename(
    columns={
        "gene_symbol": "基因符号",
        "pathway_name": "通路名称",
        "pathway_category": "通路分类",
        "biological_meaning": "生物学意义"
    }
)

st.dataframe(pathway_display, use_container_width=True, hide_index=True)