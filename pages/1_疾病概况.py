import streamlit as st
import pandas as pd

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

treatment_display = treatment_df[["treatment_name_cn", "treatment_type", "applicable_stage", "clinical_role"]].rename(
    columns={
        "treatment_name_cn": "治疗名称",
        "treatment_type": "治疗类型",
        "applicable_stage": "适用分期",
        "clinical_role": "临床作用"
    }
)
st.dataframe(treatment_display, use_container_width=True, hide_index=True)

st.markdown("---")

st.subheader("📚 数据来源")

for _, row in ref_df.iterrows():
    st.markdown(f"- {row['gbt7714']}")