import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import re
import numpy as np

# 🔵 1. 웹사이트 본문 폰트 크기 일괄 적용 (16px)
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-size: 16px !important;
    }
    .stMarkdown, .stText, .stSubheader, .stHeader, .stTitle {
        font-size: 18px !important;
        line-height: 1.7 !important;
    }
    .stApp {
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🔵 2. 한글 폰트 설정
FONT_PATH = os.path.join("fonts", "NanumGothicCoding.ttf")
if os.path.exists(FONT_PATH):
    font_prop = fm.FontProperties(fname=FONT_PATH)
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False
else:
    font_prop = None

# 🔵 3. Streamlit 페이지 세팅
st.set_page_config(page_title="양주시 아카이브: 과거, 현재, 미래", layout="wide")
st.title("🏙️ 양주시 아카이브: 과거, 현재, 미래")
st.markdown("<span style='font-size:15pt;'>경기도 양주시의 역사와 미래 비전을 살펴보는 디지털 아카이브입니다.</span>", unsafe_allow_html=True)

tabs = st.tabs(["📜 과거", "🏙️ 현재", "🌐 미래", "📊 인구 변화"])

# --- 과거 탭 ---
with tabs[0]:
    st.header("📜 양주시의 과거")
    st.markdown("""
    <div style='font-size:13pt;'>
    <b>1. 고려~조선 시대, 북방의 행정·군사 중심지</b><br>
    - 양주목 설치: 경기 북부 광역 행정 단위<br>
    - 조선시대 서울 외곽 방어선 역할<br>
    - 현재의 의정부, 동두천, 포천, 남양주 일대가 관할 지역<br>
    <br>
    <b>2. 회암사: 왕실의 불교 수행처</b><br>
    - 태조 이성계 퇴위 후 회암사 중건<br>
    - 세종 시대까지 국가 불교 중심지로 기능<br>
    - 승과(僧科) 시행 장소<br>
    - 현재는 회암사지 및 국립 회암사지박물관으로 보존<br>
    <br>
    <b>3. 조선 후기 천주교 박해의 현장</b><br>
    - 신유박해(1801) 시기 여성 신자 다수 순교<br>
    - 강완숙, 이순이 등 순교자 기록<br>
    - 장흥면에 순교 기념비, 성지 조성<br>
    <br>
    <b>4. 한국전쟁과 양주</b><br>
    - 1·4 후퇴 시 주요 격전지<br>
    - 1951년 대규모 민간인 피해<br>
    - 전쟁 후 장기 복구 과정<br>
    <br>
    <b>5. 농업과 장터</b><br>
    - 장흥, 은현, 남면은 조선시대 곡창지대<br>
    - 읍내 장터는 한양 상인과의 활발한 교역지
    </div>
    """, unsafe_allow_html=True)

# --- 현재 탭 ---
with tabs[1]:
    st.header("🏙️ 양주시의 현재")
    st.markdown("""
    <div style='font-size:13pt;'>
    <b>1. 인구와 행정</b><br>
    - 2025년 인구 약 29만 명, 면적 310.4㎢, 1읍 4면 7동.<br>
    - 초중고대학 67교, 약 2,800여 개의 공장 및 산업시설이 위치.<br>
    <br>
    <b>2. 신도시 개발 및 교통</b><br>
    - 옥정·회천 신도시 개발로 수도권 내 인구 급증(최근 수도권 증가율 1위).<br>
    - 7호선 연장, GTX-C 개통 등 서울 접근성 좋은 광역교통망 빠르게 확장.<br>
    <br>
    <b>3. 산업기반 확충</b><br>
    - 양주테크노밸리, 첨단산업단지 개발<br>
    - 의료·바이오·IT 기업 유치 및 고용 창출, 세수 확대<br>
    <br>
    <b>4. 문화·관광 자원 리브랜딩</b><br>
    - 장흥 조각공원, 송암천문대, 나리농원, 회암사지 등 관광자원 리브랜딩<br>
    - 전통+현대예술 융합, 청년예술가 지원<br>
    <br>
    <b>5. 도시·농촌 복합형 구조</b><br>
    - 도심은 아파트 중심, 외곽은 농촌·산림지<br>
    - 다양한 커뮤니티와 라이프스타일 공존
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

# --- 미래 탭 ---
with tabs[2]:
    st.header("🌐 양주시의 미래")
    st.markdown("""
    <div style='font-size:13pt;'>
    <b>1. 경기북부 중심도시 성장</b><br>
    - 수도권 동북부 거점도시로 발전<br>
    - 주거 중심에서 산업·문화·교육 복합도시로 전환<br>
    - 광역교통망 중심축으로 기대<br>
    <br>
    <b>2. 첨단산업과 창업도시</b><br>
    - 테크노밸리, 산업단지 중심 개발<br>
    - 청년 창업 및 스타트업 인큐베이팅<br>
    - 4차 산업 기반의 경제 체질 개선<br>
    <br>
    <b>3. 문화예술 중심도시</b><br>
    - 장흥문화예술촌 레지던시 확대<br>
    - 청년 예술가 정착 유도<br>
    - 회암사지 등 역사와 콘텐츠 결합한 스토리텔링<br>
    <br>
    <b>4. 탄소중립 스마트시티</b><br>
    - 스마트 교통, AI 행정 도입<br>
    - 공공건물 태양광 등 에너지 절감 도시계획<br>
    - 생태공원, 도시숲, 스마트팜 확장<br>
    <br>
    <b>5. 교육·복지 인프라</b><br>
    - 국공립 유치원 및 학교 확충<br>
    - 지역 대학 및 평생학습 거점 마련<br>
    - 맞춤형 복지 설계: 고령자, 청년, 다문화 가정 대상
    </div>
    """, unsafe_allow_html=True)

# --- 인구 변화 탭 ---
with tabs[3]:
    st.header("📊 양주시 인구 변화")
    st.markdown("양주시 인구 구조 변화를 월별/연도별 및 5년 단위 출생자수·사망자수와 함께 시각화합니다. 데이터 출처: KOSIS 국가통계포털")

    POPULATION_DATA_PATH = "양주시_연도별_인구수.csv"
    BIRTH_DEATH_DATA_PATH = "양주시_연도별_출생자수_사망자수.csv"

    # 인구수 5년 단위 집계
    try:
        df_pop = pd.read_csv(POPULATION_DATA_PATH, encoding="cp949", header=1)
        df_pop['행정구역(시군구)별'] = df_pop['행정구역(시군구)별'].astype(str).str.strip()
        df_yg_pop = df_pop[df_pop['행정구역(시군구)별'] == "양주시"].reset_index(drop=True)

        # 월별 컬럼 (예: 2011.01)
        pop_cols = [col for col in df_yg_pop.columns if re.match(r"\d{4}\.\d{1,2}", col)]
        
        # 연도만 추출해서 5년 단위로 필터링, 월별 데이터는 평균내기
        pop_year_month = []
        pop_values = []
        for col in pop_cols:
            year = int(col.split('.')[0])
            if year >= 2005:
                pop_year_month.append(col)
                try:
                    val = int(str(df_yg_pop.loc[0, col]).replace(",", "").strip())
                except:
                    val = 0
                pop_values.append(val)

        # 연도별 평균 집계 (5년 단위)
        df_pop_avg = pd.DataFrame({
            'year': [int(c.split('.')[0]) for c in pop_year_month],
            'value': pop_values
        })
        df_pop_avg_5yr = df_pop_avg.groupby('year').mean().reset_index()
        # 5년 단위만 필터링
        df_pop_avg_5yr = df_pop_avg_5yr[(df_pop_avg_5yr['year'] >= 2005) & (df_pop_avg_5yr['year'] % 5 == 0)]

        fig, ax = plt.subplots(figsize=(4.5,2.7))
        ax.plot(df_pop_avg_5yr['year'], df_pop_avg_5yr['value'], marker='o', color='tab:green', label='인구수 (연평균)')
        ax.set_title("양주시 5년 단위 연평균 인구수 변화", fontproperties=font_prop, fontsize=12)
        ax.set_xlabel("연도", fontproperties=font_prop, fontsize=10)
        ax.set_ylabel("명", fontproperties=font_prop, fontsize=10)
        ax.set_xticks(df_pop_avg_5yr['year'])
        ax.set_xticklabels(df_pop_avg_5yr['year'], fontproperties=font_prop, fontsize=9)
        plt.yticks(fontproperties=font_prop, fontsize=9)
        plt.xticks(fontproperties=font_prop, fontsize=9)
        ax.legend(prop=font_prop, fontsize=10)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=False)

    except Exception as e:
        st.error(f"인구수 그래프를 불러오는 중 오류가 발생했습니다: {e}")

    # 출생자수·사망자수 5년 단위 그래프
    try:
        df_bd = pd.read_csv(BIRTH_DEATH_DATA_PATH, encoding="cp949")
        df_bd['행정구역별'] = df_bd['행정구역별'].astype(str).str.strip()
        df_yg_bd = df_bd[df_bd['행정구역별'] == "양주시"].reset_index(drop=True)

        colnames = list(df_yg_bd.columns)
        birth_cols = [col for col in colnames if col != "행정구역별" and "." not in col]
        death_cols = [col for col in colnames if col != "행정구역별" and "." in col]

        birth_years = []
        births = []
        for col in birth_cols:
            year_match = re.match(r"(\d{4})", col)
            if year_match:
                y = int(year_match.group(1))
                if y >= 2005 and (y % 5 == 0 or y == int(birth_cols[-1][:4])):
                    birth_years.append(y)
                    try:
                        val = int(str(df_yg_bd.iloc[0][col]).replace(",", "").strip())
                    except:
                        val = 0
                    births.append(val)

        death_years = []
        deaths = []
        for col in death_cols:
            year_match = re.match(r"(\d{4})", col)
            if year_match:
                y = int(year_match.group(1))
                if y >= 2005 and (y % 5 == 0 or y == int(death_cols[-1][:4])):
                    death_years.append(y)
                    try:
                        val = int(float(str(df_yg_bd.iloc[0][col]).replace(",", "").strip()))
                    except:
                        val = 0
                    deaths.append(val)

        common_years = sorted(list(set(birth_years) & set(death_years)))
        births_aligned = [births[birth_years.index(y)] for y in common_years]
        deaths_aligned = [deaths[death_years.index(y)] for y in common_years]

        fig2, ax2 = plt.subplots(figsize=(4.5,2.7))
        ax2.plot(common_years, births_aligned, marker='o', color='tab:blue', label='출생자수')
        ax2.plot(common_years, deaths_aligned, marker='o', color='tab:orange', label='사망자수')
        ax2.set_title("양주시 5년 단위 출생자수·사망자수 변화", fontproperties=font_prop, fontsize=12)
        ax2.set_xlabel("연도", fontproperties=font_prop, fontsize=10)
        ax2.set_ylabel("명", fontproperties=font_prop, fontsize=10)
        ax2.set_xticks(common_years)
        ax2.set_xticklabels(common_years, fontproperties=font_prop, fontsize=9)
        plt.yticks(fontproperties=font_prop, fontsize=9)
        plt.xticks(fontproperties=font_prop, fontsize=9)
        ax2.legend(prop=font_prop, fontsize=10)
        plt.tight_layout()
        st.pyplot(fig2, use_container_width=False)

    except Exception as e:
        st.error(f"출생자수·사망자수 그래프를 불러오는 중 오류가 발생했습니다: {e}")
