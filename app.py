import streamlit as st

# ===== 页面配置（必须放在最前面）=====
st.set_page_config(
    page_title="SCLC知识库",
    page_icon="🧬",
    layout="wide"
)

# ===== 全局自定义样式（已生效部分完全保留，仅追加修复）=====
st.markdown(
    """
    <style>
    /* ========== 以下是你已验证生效的部分，完全不动 ========== */
    /* 侧边栏导航 */
    [data-testid="stSidebarNav"] span {
        font-size: 22px !important;
    }
    [data-testid="stSidebarNav"] svg {
        width: 20px !important;
        height: 20px !important;
    }
    [data-testid="stSidebarNav"] li {
        padding: 8px 0 !important;
    }

    /* 主内容区正文段落、列表 */
    [data-testid="stMain"] .stMarkdown p,
    [data-testid="stMain"] .stMarkdown li,
    [data-testid="stMain"] .stMarkdown span {
        font-size: 20px !important;
        line-height: 1.6 !important;
    }

    /* 二级标题 */
    [data-testid="stMain"] h2,
    [data-testid="stMain"] .stHeading h2 {
        font-size: 24px !important;
    }

    /* 三级标题 */
    [data-testid="stMain"] h3,
    [data-testid="stMain"] .stHeading h3 {
        font-size: 20px !important;
    }

    /* ========== 以下是追加修复：输入框、按钮、提示框 ========== */
    /* 输入框 */
    [data-testid="stTextInput"] input[type="text"] {
        font-size: 20px !important;
        padding: 0.6rem 0.8rem !important;
    }

    /* 按钮 */
    [data-testid="stButton"] > button {
        font-size: 20px !important;
        padding: 0.5rem 1.2rem !important;
    }

    /* 所有类型提示框（warning/info/success/error） */
    [data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {
        font-size: 20px !important;
    }

    /* ========== 表格说明 ========== */
    /* st.dataframe 是 Canvas 画布渲染，CSS 无法稳定修改画布内文字，
       下面的变量写法仅部分版本生效，若无效请用 st.table() 替代 */
    [data-testid="stDataFrame"] {
        --gdg-font-size: 20px !important;
        --gdg-header-font-size: 20px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ===== 首页函数 =====
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

# ===== 注册所有页面 =====
home = st.Page(show_home, title="首页", icon="🏠")
disease = st.Page("pages/1_疾病概况.py", title="疾病概况", icon="🫁")
gene = st.Page("pages/2_基因与分型.py", title="基因与分型", icon="🧬")
analysis = st.Page("pages/3_差异分析.py", title="差异分析", icon="📊")
kg = st.Page("pages/4_知识图谱.py", title="知识图谱", icon="🔗")
market = st.Page("pages/5_市场调研.py", title="市场调研", icon="📋")

# ===== 启动导航 =====
pg = st.navigation([home, disease, gene, analysis, kg, market])
pg.run()