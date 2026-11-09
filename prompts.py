# -*- coding: utf-8 -*-
"""四阶段 Prompt 管道：提取 -> 品牌汇总 -> 竞品对比 -> GTM建议"""

STAGE1_EXTRACT = """你是北美电商营销情报分析师。给定一条原始素材（广告文案 / 用户评论 / 价格记录），提取结构化情报。
只输出JSON，格式：
{{"selling_points": [str], "target_audience": str, "sentiment": "positive|neutral|negative", "price_signal": str, "marketing_angle": str}}
无法判断的字段填 "unknown"。
素材类型：{kind}
内容：{text}"""

STAGE2_SUMMARIZE = """你是品牌口碑分析师。以下是某品牌{brand}一周内从{source}提取的全部结构化情报（JSON数组）。
汇总为周报素材，只输出JSON：
{{"top_themes": [str, str, str], "sentiment_ratio": {{"positive": 0.0, "neutral": 0.0, "negative": 0.0}}, "main_complaints": [str], "unmet_needs": [str]}}
数据：{data}"""

STAGE3_COMPARE = """你是竞品战略分析师。以下是{brands}三个品牌的周报素材对比输入。
输出对比矩阵JSON：
{{"price_bands": {{"品牌名": "价格带描述"}}, "selling_point_overlap": str, "differentiation_gap": str, "overall_table": [{{"dimension": str, "A品牌": str, "B品牌": str, "C品牌": str}}]}}
数据：{data}"""

STAGE4_GTM = """你是北美电商GTM顾问。基于竞品对比结果和我方产品定位，输出本周可执行建议。
要求：建议必须是具体动作（谁、做什么、在哪个渠道、针对什么人群），禁止正确的废话。
只输出JSON：
{{"market_opportunity": str, "actions": [str, str, str], "risk": str}}
我方产品定位：{positioning}
竞品对比：{comparison}"""
