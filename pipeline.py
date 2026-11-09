# -*- coding: utf-8 -*-
"""DeepSeek 调用与四阶段管道"""
import json, os
from dotenv import load_dotenv
from openai import OpenAI
from prompts import STAGE1_EXTRACT, STAGE2_SUMMARIZE, STAGE3_COMPARE, STAGE4_GTM

load_dotenv()
client = OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"],
                base_url="https://api.deepseek.com")


def _chat(user, system="You are a helpful assistant", temperature=0.2, max_tokens=3000):
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": user}],
        temperature=temperature,
        response_format={"type": "json_object"},
        max_tokens=max_tokens,
        extra_headers={"Accept-Encoding": "identity"},
    )
    return json.loads(resp.choices[0].message.content)


def extract_materials(kind, text):
    """阶段1：单条素材 -> 结构化情报"""
    return _chat(STAGE1_EXTRACT.format(kind=kind, text=text))


def summarize_brand(brand, source, extractions):
    """阶段2：品牌周度汇总"""
    return _chat(STAGE2_SUMMARIZE.format(brand=brand, source=source,
                                         data=json.dumps(extractions, ensure_ascii=False)),
                 temperature=0.3)


def compare_brands(summaries):
    """阶段3：竞品对比矩阵"""
    brands = "、".join(summaries.keys())
    return _chat(STAGE3_COMPARE.format(brands=brands,
                                         data=json.dumps(summaries, ensure_ascii=False)),
                 temperature=0.4, max_tokens=4000)


def generate_gtm(comparison, positioning):
    """阶段4：可执行GTM建议"""
    return _chat(STAGE4_GTM.format(comparison=json.dumps(comparison, ensure_ascii=False),
                                   positioning=positioning),
                 temperature=0.5, max_tokens=4000)
