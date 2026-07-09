import streamlit as st
import pandas as pd
import os

st.header("📊 基因表达差异分析")

st.markdown("**数据集：** GSE43346 ｜ **分组：** SCLC vs Control ｜ **筛选标准：** |log2FC| > 1, adj.P.Val < 0.05")

deg_df = pd.read_csv("GSE43346.top.table.tsv", sep="\t")

sig_df = deg_df[(deg_df["logFC"].abs() > 1) & (deg_df["adj.P.Val"] < 0.05)]

col1, col2, col3 = st.columns(3)
col1.metric("📈 上调基因", len(sig_df[sig_df["logFC"] > 0]))
col2.metric("📉 下调基因", len(sig_df[sig_df["logFC"] < 0]))
col3.metric("📊 总差异基因", len(sig_df))

st.divider()

st.subheader("🔬 可视化结果")

fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    if os.path.exists("volcano_plot.png"):
        st.image("volcano_plot.png", caption="火山图 (Volcano Plot)")

with fig_col2:
    if os.path.exists("ma_plot.png"):
        st.image("ma_plot.png", caption="MA图 (Mean-Difference Plot)")

if os.path.exists("umap_plot.png"):
    st.image("umap_plot.png", caption="UMAP降维图 (样本聚类展示)")

st.divider()

st.subheader("📋 Top 20 差异表达基因")

top_genes = sig_df.nlargest(20, "logFC")[["Gene.symbol", "logFC", "adj.P.Val", "Gene.title"]]
top_genes.columns = ["基因符号", "logFC", "校正后p值", "基因全称"]

top_genes_display = top_genes.copy()
top_genes_display["logFC"] = top_genes_display["logFC"].map(lambda x: f"{x:.2f}")
top_genes_display["校正后p值"] = top_genes_display["校正后p值"].map(lambda x: f"{x:.2e}")

st.dataframe(top_genes_display, use_container_width=True, hide_index=True)