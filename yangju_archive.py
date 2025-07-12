import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import os

# ---- 한글 폰트 설정 ----
font_path = os.path.join(os.getcwd(), "fonts", "NanumGothicCoding.ttf")
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    mpl.rc('font', family=font_prop.get_name())
    plt.rcParams['font.family'] = font_prop.get_name()
else:
    font_prop = None

# ---- 웹 전체 폰트 크기 조정 ----
st.markdown("""
    <style>
    html, body, [class*="css"]  {
      font-size: 16px !important;
    }
    .markdown-text-container {
      font-size: 16px !important;
    }
    h1, h2, h3 {
      font-size: 2em !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏙️ 양주시 아카이브: 과거, 현재, 미래")
st.markdown("경기도 양주시의 역사와 미래 비전을 살펴보는 디지털 아카이브입니다.", unsafe_allow_html=True)

tabs = st.tabs(["📜 과거", "🏙️ 현재", "🌐 미래"])

# --------- 📜 과거 탭 ---------
with tabs[0]:
    st.markdown("<h1 style='font-size:28px;'>양주시의 과거</h1>", unsafe_allow_html=True)
    st.markdown("""
    <span style='font-size:12pt;'>
    <b>1. 삼국시대와 고려시대</b><br>
    • 양주 지역은 삼국시대 때부터 한강 유역의 전략적 요충지로서, 백제·고구려·신라의 영향을 받음.<br>
    • 고려시대에는 ‘양주(楊州)’라는 명칭이 공식적으로 사용되었고, 관청과 교통, 군사 요지로 성장.<br><br>
    <b>2. 조선시대의 발전</b><br>
    • 조선 초기 한성(서울)의 외곽을 담당하는 중요한 행정구역으로 발전.<br>
    • 광해군 때 '양주목' 승격, 8도(道)와 이어지는 교통·군사적 거점.<br>
    • 다양한 전통시장과 장시, 문화 유적지(회암사지 등)가 번성.<br><br>
    <b>3. 일제강점기 ~ 근대화</b><br>
    • 1914년 부군면 통폐합, 양주군에서 현재의 남양주, 의정부, 동두천, 포천 등 분리.<br>
    • 20세기 중후반 행정구역 개편(읍·면 분리), 인구 증대 및 농업 중심지 역할.<br>
    </span>
    """, unsafe_allow_html=True)

# --------- 🏙️ 현재 탭 ---------
with tabs[1]:
    st.markdown("<h1 style='font-size:28px;'>양주시의 현재</h1>", unsafe_allow_html=True)
    st.markdown("""
    <span style='font-size:12pt;'>
    <b>1. 인구와 행정</b><br>
    • 2025년 인구 약 29만 명, 면적 310.4㎢, 1읍 4면 7동.<br>
    • 초중고대학 67교, 약 2,800여 개의 공장 및 산업시설이 위치.<br><br>
    <b>2. 신도시 개발 및 교통</b><br>
    • 옥정·회천 신도시 개발로 수도권 내 인구 급증(최근 수도권 증가율 1위).<br>
    • GTX-C 개통 등 서울 접근성 향상, 교통망 빠르게 확장.<br><br>
    <b>3. 산업기반 확충</b><br>
    • 양주테크노밸리, 첨단산업단지 개발<br>
    • 의료·바이오·IT 기업 유치 및 고용 창출, 세수 확대<br><br>
    <b>4. 문화·관광 자원 리브랜딩</b><br>
    • 장흥 조각공원, 승일전망대, 나리농원, 회암사지 등 관광자원 리브랜딩<br>
    • 전통+현대예술 융합, 청년예술가 지원<br><br>
    <b>5. 도시·농촌 복합형 구조</b><br>
    • 도심은 아파트 중심, 외곽은 농촌·산업지<br>
    • 다양한 주거·라이프스타일 공존
    </span>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 🍼 양주시 5년 단위 연도별 출생자수·사망자수 변화(2005~최신)")
    st.markdown(
        "<span style='font-size:12pt;'>양주시의 인구 구조 변화는 5년 단위로 간략하게 시각화합니다. <br>데이터 출처: KOSIS 국가통계포털</span>",
        unsafe_allow_html=True
    )

    # ----- 데이터 불러오기 및 전처리 -----
    data_path = "양주시_연도별_출생자수_사망자수.csv"
    df = pd.read_csv(data_path, encoding="utf-8")
    # 컬럼명에 공백이 있으면 자동 trim
    df.columns = [c.strip() for c in df.columns]
    # "행정구역별" 컬럼에서 "양주시"만 필터링
    df_yangju = df[df["행정구역별"] == "양주시"].reset_index(drop=True)

    # 데이터 형태 wide → long 전환
    data_long = []
    for col in df_yangju.columns:
        if "출생건수" in col or "사망건수" in col:
            year = col.split()[0]
            value = int(df_yangju.loc[0, col])
            kind = "출생자수" if "출생" in col else "사망자수"
            data_long.append({"연도": int(year), "구분": kind, "값": value})
    df_long = pd.DataFrame(data_long)

    # 2005년부터 5년 단위로만 필터링
    year_list = list(range(2005, 2026, 5))
    df_long = df_long[df_long["연도"].isin(year_list)]

    # wide 형태로 pivot
    df_pivot = df_long.pivot(index="연도", columns="구분", values="값").sort_index()

    # ---- 시각화: 그래프 크기/폰트 최적화 ----
    fig, ax = plt.subplots(figsize=(5.5, 3.2))  # 크기 축소
    ax.plot(df_pivot.index, df_pivot["출생자수"], marker="o", label="출생자수", linewidth=2)
    ax.plot(df_pivot.index, df_pivot["사망자수"], marker="o", label="사망자수", linewidth=2)
    ax.set_title("양주시 5년 단위 출생자수 · 사망자수 변화", fontproperties=font_prop, fontsize=16)
    ax.set_xlabel("연도", fontproperties=font_prop, fontsize=12)
    ax.set_ylabel("명", fontproperties=font_prop, fontsize=12)
    ax.legend(prop=font_prop, fontsize=12)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)

# --------- 🌐 미래 탭 ---------
with tabs[2]:
    st.markdown("<h1 style='font-size:28px;'>양주시의 미래</h1>", unsafe_allow_html=True)
    st.markdown("""
    <span style='font-size:12pt;'>
    <b>1. 인구 30만 돌파와 도시 성장</b><br>
    • 신도시, 신규 아파트 단지 확장, GTX-C 개통 등으로 2030년 인구 30만 명 돌파 예상.<br>
    • 고령화율 증가와 청년층 유입, 인구구조 다변화.<br><br>
    <b>2. 첨단산업·미래도시</b><br>
    • 양주테크노밸리, 바이오·IT 융합산업단지 확대.<br>
    • 친환경, 스마트도시 인프라 도입, 공공데이터·AI·에너지 혁신.<br><br>
    <b>3. 문화·관광·예술 중심지</b><br>
    • 장흥·회암사지 등 관광·예술 자원과 ICT 접목, 국내외 관광객 확대.<br>
    • 청년예술인·디지털콘텐츠, 다양한 창업 및 예술 지원.<br><br>
    <b>4. 도시와 농촌의 공존, 지속가능 성장</b><br>
    • 스마트 농업, 그린에너지 도입 등으로 농촌과 도시가 함께 성장.<br>
    • 도시정책과 교육, 주민참여 확대.<br>
    </span>
    """, unsafe_allow_html=True)
