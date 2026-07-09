import streamlit as st
import pandas as pd

# CSS样式不变
st.markdown(
    """
    <style>
    [data-testid="stTable"] table td {
        font-size: 20px !important;
        padding: 14px 10px !important;
    }
    [data-testid="stTable"] table th {
        font-size: 22px !important;
        font-weight: 900 !important;
        padding: 14px 10px !important;
    }
    [data-testid="stTable"] table tr th:first-child,
    [data-testid="stTable"] table tr td:first-child {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header("🫁 小细胞肺癌疾病概况")

disease_df = pd.read_csv("disease/disease_final.csv")
clinical_df = pd.read_csv("disease/clinical_features.csv")
treatment_df = pd.read_csv("disease/treatment_final.csv")
ref_df = pd.read_csv("disease/references.csv")

disease = disease_df.iloc[0]

st.markdown(f"**{disease['disease_name_cn']}（{disease['disease_name_en']}，{disease['abbreviation']}）**")
st.markdown(f"*{disease['disease_category']}*")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**📌 定义**\n\n{disease['definition']}")
    st.markdown(f"**📊 流行病学**\n\n{disease['epidemiology']}")
    st.markdown(f"**⚠️ 主要危险因素**\n\n{disease['main_risk_factors']}")
with col2:
    st.markdown(f"**🩺 临床特征**\n\n{disease['clinical_features']}")
    st.markdown(f"**📋 分期方式**\n\n{disease['staging']}")
    st.markdown(f"**🔬 诊断方式**\n\n{disease['diagnosis']}")

st.markdown("---")

st.subheader("📌 临床特征详情")
for _, row in clinical_df.iterrows():
    with st.expander(f"{row['module']} — {row['category']}"):
        st.markdown(f"**{row['structured_content']}**")
        st.caption(f"解读：{row['interpretation']}")

st.markdown("---")

st.subheader("💊 治疗方式")
# 单独表格搜索框
treat_search = st.text_input("筛选治疗方案", placeholder="输入免疫、化疗、放疗、广泛期等")

treatment_display = treatment_df[["treatment_name_cn", "treatment_type", "applicable_stage", "clinical_role"]].rename(
    columns={
        "treatment_name_cn": "治疗名称",
        "treatment_type": "治疗类型",
        "applicable_stage": "适用分期",
        "clinical_role": "临床作用"
    }
)
treatment_display.insert(0, "序号", list(range(1, len(treatment_display)+1)))

# 筛选逻辑
if treat_search:
    kw = treat_search.lower()
    show_df = treatment_display[treatment_display.apply(lambda r: kw in str(r).lower(), axis=1)]
    if show_df.empty:
        st.warning("无匹配治疗方案")
    else:
        st.table(show_df, border="horizontal")
else:
    st.table(treatment_display, border="horizontal")

st.markdown("---")

st.subheader("📚 数据来源")
for _, row in ref_df.iterrows():
    st.markdown(f"- {row['gbt7714']}")