import streamlit as st
import pandas as pd

# 全局统一表格样式（与疾病概况页完全一致）
st.markdown(
    """
    <style>
    /* 单元格字体放大 */
    [data-testid="stTable"] table td {
        font-size: 20px !important;
        padding: 14px 10px !important;
    }
    /* 表头加粗放大 */
    [data-testid="stTable"] table th {
        font-size: 22px !important;
        font-weight: 900 !important;
        padding: 14px 10px !important;
    }
    /* 隐藏原生0索引，只保留我们1开始的序号 */
    [data-testid="stTable"] table tr th:first-child,
    [data-testid="stTable"] table tr td:first-child {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header("📋 市场调研与项目定位")

# ===== 竞品数据库对比数据 =====
data = {
    "数据库名称": [
        "GeneCards",
        "DrugBank",
        "KEGG",
        "STRING",
        "SCLC cBioPortal",
        "LCGene",
        "LOSTdb"
    ],
 "核心功能": [
        "人类基因综合信息大全，提供基因功能、表达、定位等全面注释",
        "详细的药物靶点、化学结构及药理作用数据库，支持药物-基因互作查询",
        "经典的生物通路数据库",
        "蛋白质-蛋白质相互作用（PPI）网络数据库",
        "SCLC 基因组/转录组可视化分析",
        "基于文献挖掘的肺癌基因数据库",
        "肺癌分子亚型多组学注释系统"
    ],
    "局限性": [
        "数据泛化，未针对SCLC进行分子分型归类",
        "侧重药理机制，缺乏与SCLC临床治疗方案的直接关联",
        "通路模型通用，未根据SCLC神经内分泌特性进行裁剪简化",
        "网络节点多，难以聚焦SCLC核心驱动基因",
        "界面复杂，无知识图谱整合",
        "偏向基因列表，无分型/治疗结构化关联",
        "偏向研究工具，不直接展示知识图谱"
    ],
    "启发": [
        "作为基因功能描述的权威来源",
        "补充 SCLC 免疫治疗药物与对应生物标志物的关系",
        "直接引用其通路名称和核心基因",
        "辅助构建 SCLC 关键基因之间的互作关系",
        "借鉴其差异表达可视化思路",
        "验证我们整理的 SCLC 核心基因",
        "参考其分型-基因关联逻辑"
    ]
}

df = pd.DataFrame(data)
# 添加从1开始的序号
df.insert(0, "序号", list(range(1, len(df)+1)))

# 使用适配你版本的 st.table
st.table(df, border="horizontal")

st.divider()
st.success("🎯 项目定位与差异化亮点")

st.markdown("""
**1. 面向人群**
            
本平台主要面向**医学生与初级临床医生**。
现有数据库都是科研用途、门槛高、内容复杂，**不适合用来学习**，我们专门做「教学型」SCLC知识库。

**2. 与竞品最大区别**
- 其他数据库：**通用、偏科研、只有数据、无临床逻辑**
- 本项目：**SCLC专属、偏教学、结构化、贴合临床学习逻辑**

**3. 核心创新**

市面上没有平台将 **疾病、分型、基因、通路、治疗、文献** 完整串联。
我们填补了**小细胞肺癌专属教学知识库的空白**，适合快速系统学习。
""")