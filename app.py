import streamlit as st

# ===== 页面配置 =====
st.set_page_config(
    page_title="SCLC知识库",
    page_icon="🧬",
    layout="wide"
)

# ===== 定义首页函数（直接在 app.py 里写）=====
def show_home():
    st.header("🏠 欢迎来到 SCLC 知识库")
    st.markdown("""
    本项目整合小细胞肺癌（Small Cell Lung Cancer, SCLC）的：
    - 疾病特征与临床治疗现状
    - 关键基因与分子分型（SCLC-A/N/P/I）
    - 基因表达差异分析结果
    - 结构化数据库与知识图谱
    - 网页系统可视化展示
    """)
    st.divider()

# ===== 定义所有页面（注意：首页用 callable 参数，指向函数）=====
home = st.Page(show_home, title="首页", icon="🏠")
disease = st.Page("pages/1_疾病概况.py", title="疾病概况", icon="🫁")
gene = st.Page("pages/2_基因与分型.py", title="基因与分型", icon="🧬")
analysis = st.Page("pages/3_差异分析.py", title="差异分析", icon="📊")
kg = st.Page("pages/4_知识图谱.py", title="知识图谱", icon="🔗")
market = st.Page("pages/5_市场调研.py", title="市场调研", icon="📋")

# ===== 导航 =====
pg = st.navigation([home, disease, gene, analysis, kg, market])
pg.run()