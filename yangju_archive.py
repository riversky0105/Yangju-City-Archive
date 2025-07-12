import os
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import pandas as pd

# 한글 폰트 경로 설정
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
**1. 삼국~고려시대: 전략 요충지**
- 신라 경덕왕 때 ‘내소군’, 고려시대 ‘한양군’ 등으로 불리며 북한산 일대 전략적 요충지 역할.
- 대모산성, 도락산 등지에서 삼국시대 유적 출토, 군사적 중요성 입증.

**2. 조선시대: 경기 북부 행정·군사 중심**
- 1395년 ‘양주’로 개칭, 세조 1466년 양주목 승격. 
- 치소(관아) 설치, 의정부·동두천·포천·남양주 등 광범위한 관할, 서울 외곽 방어선 역할.
- 회암사: 태조 이성계의 수행처, 세종 때까지 국가 불교 중심지(승과 시행, 왕실 불교 행사 중심지).
- 장흥, 은현, 남면 등 곡창지대, 읍내 장터에서 한양 상인과 활발한 교역.

**3. 근대~현대: 격동의 시기와 변동**
- 1801년 신유박해 시기 여성 신자 등 다수 순교, 천주교 박해의 현장(순교 기념비, 성지 조성).
- 한국전쟁 1·4 후퇴 시 격전지, 대규모 민간인 피해, 전쟁 후 복구 과정.
- 1922년 양주군청 의정부로 이전, 1960~80년대 행정구역 일부 편입(서울·의정부), 2003년 도·농복합도시로 독립.
    """)

with tabs[1]:
    st.header("🏙️ 양주시의 현재")
    st.markdown("""
**1. 인구와 행정**
- 2025년 인구 약 29만 명, 면적 310.4㎢, 1읍 4면 7동.
- 초중고대학 67교, 약 2,800여 개의 공장 및 산업시설이 위치.

**2. 신도시 개발 및 교통**
- 옥정·회천 신도시 개발로 수도권 내 인구 급증(최근 수도권 증가율 1위).
- 7호선 연장, GTX-C 개통 예정, 수도권 제2순환도로 등 광역교통망 빠르게 확장.
- 다양한 커뮤니티(아파트 중심 도시+농촌·산림지 공존), 도시·농촌 복합 구조.

**3. 산업, 문화, 관광**
- 양주테크노밸리·은남산업단지 등 첨단산업단지 개발, 의료·IT·바이오기업 유치.
- 회암사지박물관, 장흥아트파크, 송암천문대, 장흥자생수목원 등 관광지 활성화.
- 천일홍 축제, 왕실축제, 드론봇 페스티벌 등 다양한 문화행사 및 지역 축제 개최.
- 장흥문화예술촌·예술인 레지던시 운영, 전통+현대 예술 융합 지향.

**4. 환경 및 도시계획**
- 성장관리계획 통해 난개발 방지, 친환경 개발·도시숲·생태공원 추진.
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
**1. 2035 도시기본계획(비전)**
- 인구 목표 50만 명, 상생·경제·문화복지·녹색관광 4대 목표로 장기 발전 추진.
- 기존 시가화 지역과 함께 대규모 도시 용지 확보, 광역 교통망 중심지 계획.

**2. 첨단산업, 혁신, 창업도시**
- 테크노밸리, 산업단지 추가 개발, 4차 산업(스마트팜, AI, 디지털트윈 등) 기반 신산업도시로 전환.
- 청년 창업 인큐베이팅, 스타트업 지원, 혁신기업 유치로 경제 체질 개선.

**3. 문화·예술·복지**
- 장흥문화예술촌, 청소년 복합문화센터, 스마트복지시설, 다문화지원센터 등 생활SOC 대폭 확대.
- 회암사지, 왕실 축제 등 역사와 문화의 국제 브랜드화.
- 메타버스·치즈 클러스터, 수변 관광 브랜드화 등 미래형 관광 추진.

**4. 탄소중립·스마트시티**
- AI 행정, 스마트 교통, 태양광 등 친환경 에너지 정책 도입.
- 생태공원·도시숲·스마트팜 확장, 디지털 기반 환경 도시 실현 목표.

**5. 광역 물류·교통 거점**
- GTX‑C, 7호선, 교외선, 제2순환도로 등 확충, 물류·유통기지로 성장.
- 은현 물류단지 등 신성장 거점 확보.
    """)
