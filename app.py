# -*- coding: utf-8 -*-
"""北美市场AI情报助手 - Streamlit 演示界面
运行：streamlit run app.py
"""
import json
import pandas as pd
import streamlit as st
import pipeline

st.set_page_config(page_title="北美市场AI情报助手", layout="wide")
st.title("北美市场AI情报助手")
st.caption("输入竞品与品类，自动生成周度市场洞察 + 可执行GTM建议")

@st.cache_data
def load_data():
    ads = pd.read_csv("data/ads.csv")
    reviews = pd.read_csv("data/reviews.csv")
    pricing = pd.read_csv("data/pricing.csv")
    return ads, reviews, pricing

ads, reviews, pricing = load_data()
all_brands = sorted(set(ads["brand"]) | set(reviews["brand"]) | set(pricing["brand"]))

with st.sidebar:
    st.header("分析设置")
    selected = st.multiselect("选择竞品品牌（2-3个）", all_brands, default=all_brands[:2])
    positioning = st.text_area("我方产品定位", value="面向北美25-35岁健身人群的TWS耳机，主打运动稳固+IPX7防水，定价$35-45切入中端空档")
    run = st.button("生成周报", type="primary", disabled=len(selected) < 2)

if run:
    with st.spinner("正在分析（约2-3分钟）..."):
        summaries = {}
        for brand in selected:
            extractions = []
            for _, r in reviews[reviews.brand == brand].iterrows():
                extractions.append(pipeline.extract_materials("用户评论", r["review_text"]))
            for _, r in ads[ads.brand == brand].iterrows():
                extractions.append(pipeline.extract_materials("广告文案", r["ad_copy"]))
            summaries[brand] = pipeline.summarize_brand(brand, "Amazon评论+社媒广告", extractions)

        comparison = pipeline.compare_brands(summaries)
        gtm = pipeline.generate_gtm(comparison, positioning)

    st.success("周报生成完毕")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📊 竞品对比矩阵")
        st.json(comparison)
    with c2:
        st.subheader("🎯 本周GTM建议")
        st.markdown(f"**市场机会：** {gtm['market_opportunity']}")
        for i, a in enumerate(gtm["actions"], 1):
            st.markdown(f"{i}. {a}")
        st.warning(f"⚠️ 风险：{gtm['risk']}")

    st.subheader("💬 品牌口碑概览")
    for brand, s in summaries.items():
        with st.expander(brand):
            ratio = s.get("sentiment_ratio", {})
            if ratio:
                st.bar_chart(pd.Series(ratio, name="情绪占比"))
            st.markdown(f"**本周主题：** {' / '.join(s.get('top_themes', []))}")
            st.markdown(f"**主要抱怨：** {'; '.join(s.get('main_complaints', []))}")
            st.markdown(f"**未被满足的需求：** {'; '.join(s.get('unmet_needs', []))}")
else:
    st.info('在左侧选择2-3个竞品品牌，点击"生成周报"开始分析')
