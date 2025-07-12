import os
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import pandas as pd

# 한글 폰트 경로 설정 (os.path.join 사용!)
font_path = os.path.join(os.getcwd(), "fonts", "NanumGothicCoding.ttf")
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    mpl.rcParams['axes.unicode_minus'] = False
else:
    font_prop = None

st.set_page_config(page_title="양주시 아카이브", layout="wide")

st.markdown("""
    <style>
        .markdown-text-container { line-height: 1.8; }
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        h1, h2, h3 { margin-top: 1.2em; margin-bottom: 0.6em; }
        p { margin-bottom: 1.2em; }
    </style>
""", unsafe_allow_html=True)

st.title("🏙️ 양주시 아카이브: 과거, 현재, 미래")
st.markdown("경기도 양주시의 역사와 미래 비전을 살펴보는 디지털 아카이브입니다.")

if not os.path.exists(font_path):
    st.error("⚠️ 폰트 파일이 없습니다: fonts/NanumGothicCoding.ttf 파일을 확인하세요!")

tabs = st.tabs(["📜 과거", "🏙️ 현재", "🌐 미래"])

with tabs[0]:
    st.header("📜 양주시의 과거")
    st.markdown("""
    ... (본문 생략, 이전과 동일하게 유지)
    """)

with tabs[1]:
    st.header("🏙️ 양주시의 현재")
    st.markdown("""
    ... (본문 생략, 이전과 동일하게 유지)
    """)

    # ▷ 인구 추이 그래프
    st.subheader("📊 인구 추이 (2023~2025)")
    years = [2023, 2024, 2025]
    pops = [270000, 290000, 292089]
    fig, ax = plt.subplots()
    ax.plot(years, pops, marker='o')
    ax.set_title('양주시 인구 추이', fontproperties=font_prop)
    ax.set_xlabel('연도', fontproperties=font_prop)
    ax.set_ylabel('인구수 (명)', fontproperties=font_prop)
    ax.set_xticks(years)
    ax.set_xticklabels([str(year) for year in years], fontproperties=font_prop)
    for label in ax.get_yticklabels():
        if font_prop: label.set_fontproperties(font_prop)
    st.pyplot(fig)
    st.caption("자료: 행정안전부 주민등록 인구통계, 양주시청 기본현황")

    # ▷ 출생·사망 통계 그래프
    st.subheader("📊 2025년 5월 기준 출생·사망 비교")
    events = ['출생', '사망']
    counts = [765, 820]
    fig2, ax2 = plt.subplots()
    bars = ax2.bar(events, counts, color=['green', 'red'])
    ax2.set_ylabel('명', fontproperties=font_prop)
    ax2.set_title('출생/사망 현황', fontproperties=font_prop)
    ax2.set_xticks(range(len(events)))
    ax2.set_xticklabels(events, fontproperties=font_prop)
    for label in ax2.get_yticklabels():
        if font_prop: label.set_fontproperties(font_prop)
    for bar in bars:
        height = bar.get_height()
        ax2.annotate(f'{height}',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3),
                     textcoords="offset points",
                     ha='center', va='bottom',
                     fontproperties=font_prop)
    st.pyplot(fig2)
    st.caption("자료: 양주시청 (2025.5.31 기준)")

    # ▷ 산업·교육 인프라 그래프
    st.subheader("📊 산업·교육 인프라 현황")
    categories = ['공장', '학교']
    values = [2845, 67]
    fig3, ax3 = plt.subplots()
    bars3 = ax3.bar(categories, values, color=['blue', 'orange'])
    ax3.set_ylabel('개수', fontproperties=font_prop)
    ax3.set_title('등록 공장 수 / 학교 수', fontproperties=font_prop)
    ax3.set_xticks(range(len(categories)))
    ax3.set_xticklabels(categories, fontproperties=font_prop)
    for label in ax3.get_yticklabels():
        if font_prop: label.set_fontproperties(font_prop)
    for bar in bars3:
        height = bar.get_height()
        ax3.annotate(f'{height}',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3),
                     textcoords="offset points",
                     ha='center', va='bottom',
                     fontproperties=font_prop)
    st.pyplot(fig3)
    st.caption("자료: 양주시청 (2025.5.31 기준)")

with tabs[2]:
    st.header("🌐 양주시의 미래")
    st.markdown("""
    ... (본문 생략, 이전과 동일하게 유지)
    """)

