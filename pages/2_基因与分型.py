import streamlit as st
import pandas as pd
from pathlib import Path
import re

st.header("🧬 关键基因与分子分型")

current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent

def find_file(filename):
    path1 = current_dir / filename
    path2 = parent_dir / filename

    if path1.exists():
        return path1
    if path2.exists():
        return path2

    return path1

def read_csv_auto(filename):
    path = find_file(filename)
    encodings = ["utf-8-sig", "utf-8", "gb18030", "gbk"]

    if not path.exists():
        st.warning(f"未找到文件：{filename}")
        return pd.DataFrame()

    last_error = None

    for enc in encodings:
        try:
            df = pd.read_csv(path, encoding=enc)
            df.columns = df.columns.str.strip()

            if "source_urh" in df.columns and "source_url" not in df.columns:
                df = df.rename(columns={"source_urh": "source_url"})

            return df

        except Exception as e:
            last_error = e

    st.error(f"无法读取文件：{filename}")
    st.exception(last_error)
    return pd.DataFrame()

def filter_dataframe(df, keyword, columns):
    if df.empty:
        return pd.DataFrame()

    if not keyword:
        return pd.DataFrame()

    keyword = str(keyword).strip()

    if keyword == "":
        return pd.DataFrame()

    mask = pd.Series(False, index=df.index)

    for col in columns:
        if col in df.columns:
            mask = mask | df[col].astype(str).str.contains(
                keyword,
                case=False,
                na=False,
                regex=False
            )

    return df[mask]

def safe_merge_gene_annotation(gene_df, annotation_df):
    if gene_df.empty:
        return pd.DataFrame()

    if annotation_df.empty:
        return gene_df.copy()

    if "gene_symbol" not in gene_df.columns or "gene_symbol" not in annotation_df.columns:
        return gene_df.copy()

    merged = pd.merge(
        gene_df,
        annotation_df,
        on="gene_symbol",
        how="left",
        suffixes=("", "_annotation")
    )

    return merged

def get_value(row, col):
    if col in row.index:
        value = row[col]
        if pd.isna(value):
            return ""
        return str(value)
    return ""

def split_gene_list(text):
    if pd.isna(text):
        return []

    text = str(text).strip()

    if text == "":
        return []

    parts = re.split(r"[;,；，/]+", text)
    genes = []

    for item in parts:
        item = item.strip()
        if item != "":
            genes.append(item)

    return genes

def add_genes_from_column(df, col, gene_set):
    if df.empty or col not in df.columns:
        return

    for value in df[col].dropna().astype(str).tolist():
        for gene in split_gene_list(value):
            gene_set.add(gene)

def add_values_from_column(df, col, value_set):
    if df.empty or col not in df.columns:
        return

    for value in df[col].dropna().astype(str).tolist():
        value = value.strip()
        if value != "":
            value_set.add(value)

def build_query_result(keyword, gene_full_df, subtype_df, relation_df, pathway_df):
    result_rows = []

    if not keyword or str(keyword).strip() == "":
        return pd.DataFrame()

    keyword = str(keyword).strip()

    valid_subtypes = {"SCLC-A", "SCLC-N", "SCLC-P", "SCLC-I"}

    gene_search_columns = [
        "gene_symbol",
        "official_full_name",
        "description",
        "aliases",
        "gene_category",
        "sclc_relevance",
        "related_subtype",
        "related_process",
        "knowledge_role"
    ]

    subtype_search_columns = [
        "subtype_name",
        "main_marker",
        "marker_type",
        "molecular_feature",
        "biological_feature",
        "related_process",
        "representative_genes"
    ]

    relation_search_columns = [
        "source_gene",
        "relation_type",
        "target_entity",
        "target_type",
        "description",
        "evidence"
    ]

    pathway_search_columns = [
        "gene_symbol",
        "pathway_name",
        "pathway_category",
        "relation_type",
        "biological_meaning",
        "remark"
    ]

    gene_match = filter_dataframe(gene_full_df, keyword, gene_search_columns)
    subtype_match = filter_dataframe(subtype_df, keyword, subtype_search_columns)
    subtype_name_match = filter_dataframe(subtype_df, keyword, ["subtype_name"])
    relation_match = filter_dataframe(relation_df, keyword, relation_search_columns)
    pathway_match = filter_dataframe(pathway_df, keyword, pathway_search_columns)

    related_genes = set()
    related_subtypes = set()

    add_values_from_column(gene_match, "gene_symbol", related_genes)
    add_values_from_column(relation_match, "source_gene", related_genes)
    add_values_from_column(pathway_match, "gene_symbol", related_genes)

    if not subtype_name_match.empty:
        add_values_from_column(subtype_name_match, "subtype_name", related_subtypes)
        add_values_from_column(subtype_name_match, "main_marker", related_genes)
        add_genes_from_column(subtype_name_match, "representative_genes", related_genes)

    related_subtypes = {
        value for value in related_subtypes
        if value in valid_subtypes
    }

    if not gene_full_df.empty and "gene_symbol" in gene_full_df.columns and related_genes:
        gene_by_related = gene_full_df[
            gene_full_df["gene_symbol"].astype(str).isin(related_genes)
        ]
    else:
        gene_by_related = pd.DataFrame()

    if not relation_df.empty and "source_gene" in relation_df.columns and related_genes:
        relation_by_gene = relation_df[
            relation_df["source_gene"].astype(str).isin(related_genes)
        ]
    else:
        relation_by_gene = pd.DataFrame()

    if not relation_df.empty and "target_entity" in relation_df.columns and related_subtypes:
        relation_by_subtype = relation_df[
            relation_df["target_entity"].astype(str).isin(related_subtypes)
        ]
    else:
        relation_by_subtype = pd.DataFrame()

    if not pathway_df.empty and "gene_symbol" in pathway_df.columns and related_genes:
        pathway_by_gene = pathway_df[
            pathway_df["gene_symbol"].astype(str).isin(related_genes)
        ]
    else:
        pathway_by_gene = pd.DataFrame()

    gene_all = pd.concat(
        [gene_match, gene_by_related],
        ignore_index=True
    ).drop_duplicates()

    relation_all = pd.concat(
        [relation_match, relation_by_gene, relation_by_subtype],
        ignore_index=True
    ).drop_duplicates()

    pathway_all = pd.concat(
        [pathway_match, pathway_by_gene],
        ignore_index=True
    ).drop_duplicates()

    for _, row in gene_all.iterrows():
        result_rows.append({
            "结果类型": "基因信息",
            "基因": get_value(row, "gene_symbol"),
            "基因全称": get_value(row, "official_full_name"),
            "关联分型": get_value(row, "related_subtype"),
            "关系类型": "",
            "通路名称": "",
            "相关过程/说明": get_value(row, "sclc_relevance") or get_value(row, "related_process"),
            "数据来源": get_value(row, "source_database") or get_value(row, "data_source"),
            "来源链接": get_value(row, "source_url")
        })

    for _, row in subtype_match.iterrows():
        result_rows.append({
            "结果类型": "分型信息",
            "基因": get_value(row, "main_marker"),
            "基因全称": "",
            "关联分型": get_value(row, "subtype_name"),
            "关系类型": get_value(row, "marker_type"),
            "通路名称": "",
            "相关过程/说明": get_value(row, "biological_feature") or get_value(row, "molecular_feature"),
            "数据来源": get_value(row, "evidence_source"),
            "来源链接": get_value(row, "source_url")
        })

    for _, row in relation_all.iterrows():
        gene_symbol = get_value(row, "source_gene")
        gene_name = ""

        if not gene_full_df.empty and "gene_symbol" in gene_full_df.columns:
            temp_gene = gene_full_df[
                gene_full_df["gene_symbol"].astype(str) == gene_symbol
            ]

            if not temp_gene.empty:
                gene_name = get_value(temp_gene.iloc[0], "official_full_name")

        result_rows.append({
            "结果类型": "基因-分型关系",
            "基因": gene_symbol,
            "基因全称": gene_name,
            "关联分型": get_value(row, "target_entity"),
            "关系类型": get_value(row, "relation_type"),
            "通路名称": "",
            "相关过程/说明": get_value(row, "description") or get_value(row, "evidence"),
            "数据来源": get_value(row, "source_database"),
            "来源链接": get_value(row, "source_url")
        })

    for _, row in pathway_all.iterrows():
        gene_symbol = get_value(row, "gene_symbol")
        gene_name = ""

        if not gene_full_df.empty and "gene_symbol" in gene_full_df.columns:
            temp_gene = gene_full_df[
                gene_full_df["gene_symbol"].astype(str) == gene_symbol
            ]

            if not temp_gene.empty:
                gene_name = get_value(temp_gene.iloc[0], "official_full_name")

        result_rows.append({
            "结果类型": "基因-通路关系",
            "基因": gene_symbol,
            "基因全称": gene_name,
            "关联分型": "",
            "关系类型": get_value(row, "relation_type"),
            "通路名称": get_value(row, "pathway_name"),
            "相关过程/说明": get_value(row, "biological_meaning"),
            "数据来源": get_value(row, "database_source"),
            "来源链接": get_value(row, "source_url")
        })

    result_df = pd.DataFrame(result_rows)

    if result_df.empty:
        return result_df

    result_df = result_df.drop_duplicates()

    result_order = {
        "基因信息": 1,
        "分型信息": 2,
        "基因-分型关系": 3,
        "基因-通路关系": 4
    }

    result_df["_order"] = result_df["结果类型"].map(result_order).fillna(99)
    result_df = result_df.sort_values(by=["_order", "基因", "关联分型", "通路名称"])
    result_df = result_df.drop(columns=["_order"])

    return result_df

gene_df = read_csv_auto("gene.csv")
annotation_df = read_csv_auto("gene_annotation.csv")
subtype_df = read_csv_auto("subtype.csv")
relation_df = read_csv_auto("gene_subtype_relation.csv")
pathway_df = read_csv_auto("gene_pathway.csv")

gene_full_df = safe_merge_gene_annotation(gene_df, annotation_df)

if not subtype_df.empty and "subtype_name" in subtype_df.columns:
    subtype_df = subtype_df[subtype_df["subtype_name"] != "SCLC-Y"]

st.markdown(
    """
    本页面分为三部分：第一部分展示 SCLC 相关关键基因，第二部分展示 SCLC 分子分型，
    第三部分展示基因与分型、通路之间的知识关系。输入关键词后，会在输入框下方生成综合查询结果表。
    """
)

search = st.text_input(
    "🔍 综合查询",
    placeholder="输入基因、分型、通路或关键词，如 TP53、ASCL1、SCLC-A、神经内分泌、DNA损伤、细胞周期、Notch"
)

query_result_df = build_query_result(
    search,
    gene_full_df,
    subtype_df,
    relation_df,
    pathway_df
)

st.subheader("🔎 综合查询结果表")

if not search:
    st.info("请输入关键词后，这里会生成新的综合查询结果表。")
elif query_result_df.empty:
    st.warning("未找到匹配结果，请检查关键词。")
else:
    st.dataframe(
        query_result_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "来源链接": st.column_config.LinkColumn("来源链接")
        }
    )

    st.caption(f"关键词“{search}”共生成 {len(query_result_df)} 条综合查询结果。")

st.divider()

st.subheader("📌 一、SCLC 相关关键基因信息")

gene_display_columns = [
    "gene_symbol",
    "official_full_name",
    "organism",
    "chromosome",
    "map_location",
    "source_database",
    "source_url"
]

gene_column_mapping = {
    "gene_symbol": "基因符号",
    "official_full_name": "基因全称",
    "organism": "物种",
    "chromosome": "染色体",
    "map_location": "染色体定位",
    "source_database": "来源数据库",
    "source_url": "来源链接"
}

gene_existing_columns = [
    col for col in gene_display_columns
    if col in gene_df.columns
]

if gene_df.empty:
    st.warning("未读取到 gene.csv，无法显示基因信息。")
else:
    st.dataframe(
        gene_df[gene_existing_columns].rename(columns=gene_column_mapping),
        use_container_width=True,
        hide_index=True,
        column_config={
            "来源链接": st.column_config.LinkColumn("来源链接")
        }
    )

st.caption(f"gene.csv 共 {len(gene_df)} 条记录。")

st.divider()

st.subheader("📌 二、SCLC 分子分型 A/N/P/I")

subtype_display_columns = [
    "subtype_name",
    "main_marker",
    "marker_type",
    "molecular_feature",
    "biological_feature",
    "related_process",
    "representative_genes",
    "source_url"
]

subtype_column_mapping = {
    "subtype_name": "分型代号",
    "main_marker": "主要标志物",
    "marker_type": "标志物类型",
    "molecular_feature": "分子特征",
    "biological_feature": "生物学特征",
    "related_process": "相关过程",
    "representative_genes": "代表性基因",
    "source_url": "来源链接"
}

subtype_existing_columns = [
    col for col in subtype_display_columns
    if col in subtype_df.columns
]

if subtype_df.empty:
    st.warning("未读取到 subtype.csv，无法显示分子分型。")
else:
    st.dataframe(
        subtype_df[subtype_existing_columns].rename(columns=subtype_column_mapping),
        use_container_width=True,
        hide_index=True,
        column_config={
            "来源链接": st.column_config.LinkColumn("来源链接")
        }
    )

st.caption(f"subtype.csv 当前显示 {len(subtype_df)} 条记录，已隐藏 SCLC-Y。")

st.divider()

st.subheader("📌 三、基因-分型-通路关系")

tab1, tab2 = st.tabs(["基因-分型关系", "基因-通路关系"])

with tab1:
    relation_display_columns = [
        "source_gene",
        "relation_type",
        "target_entity",
        "target_type",
        "description",
        "source_database",
        "source_url"
    ]

    relation_column_mapping = {
        "source_gene": "基因",
        "relation_type": "关系类型",
        "target_entity": "关联对象",
        "target_type": "对象类型",
        "description": "关系说明",
        "source_database": "来源数据库/文献",
        "source_url": "来源链接"
    }

    relation_existing_columns = [
        col for col in relation_display_columns
        if col in relation_df.columns
    ]

    if relation_df.empty:
        st.warning("未读取到 gene_subtype_relation.csv，无法显示基因-分型关系。")
    else:
        st.dataframe(
            relation_df[relation_existing_columns].rename(columns=relation_column_mapping),
            use_container_width=True,
            hide_index=True,
            column_config={
                "来源链接": st.column_config.LinkColumn("来源链接")
            }
        )

    st.caption(f"gene_subtype_relation.csv 共 {len(relation_df)} 条记录。")

with tab2:
    pathway_display_columns = [
        "gene_symbol",
        "pathway_name",
        "pathway_category",
        "relation_type",
        "biological_meaning",
        "database_source",
        "source_url"
    ]

    pathway_column_mapping = {
        "gene_symbol": "基因符号",
        "pathway_name": "通路名称",
        "pathway_category": "通路类别",
        "relation_type": "关系类型",
        "biological_meaning": "生物学意义",
        "database_source": "数据来源",
        "source_url": "来源链接"
    }

    pathway_existing_columns = [
        col for col in pathway_display_columns
        if col in pathway_df.columns
    ]

    if pathway_df.empty:
        st.warning("未读取到 gene_pathway.csv，无法显示通路关系。")
    else:
        st.dataframe(
            pathway_df[pathway_existing_columns].rename(columns=pathway_column_mapping),
            use_container_width=True,
            hide_index=True,
            column_config={
                "来源链接": st.column_config.LinkColumn("来源链接")
            }
        )

    st.caption(f"gene_pathway.csv 共 {len(pathway_df)} 条记录。")