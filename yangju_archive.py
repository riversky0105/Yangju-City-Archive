import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import re
import numpy as np

# 1. 웹사이트 본문 폰트 크기 일괄 적용 (16pt 기본, 일부 제목 18pt)
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

# 2. 한글 폰트 설정 (NanumGothicCoding.ttf)
FONT_PATH = os.path.join("fonts", "NanumGothicCoding.ttf")
if os.path.exists(FONT_PATH):
    font_prop = fm.FontProperties(fname=FONT_PATH)
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False
else:
    font_prop = None

# 3. Streamlit 페이지 설정
st.set_page_config(page_title="양주시 아카이브: 과거, 현재, 미래", layout="wide")
st.title("🏙️ 양주시 아카이브: 과거, 현재, 미래")
st.markdown("<span style='font-size:15pt;'>경기도 양주시의 역사와 미래 비전을 살펴보는 디지털 아카이브입니다.</span>", unsafe_allow_html=True)

tabs = st.tabs(["📜 과거", "🏙️ 현재", "🌐 미래", "📊 인구 변화"])

# 각 탭별 기존 콘텐츠(과거, 현재, 미래) 생략

with tabs[3]:
    st.header("📊 양주시 인구 변화")
    st.markdown("""
    양주시 인구 구조 변화를 월별/연도별 및 5년 단위 출생자수·사망자수와 함께 시각화합니다. 데이터 출처: KOSIS 국가통계포털
    """)

    # --- 인구수 변화 그래프 ---
    POP_DATA_PATH = "양주시_연도별_인구수.csv"

    try:
        # 멀티 헤더로 읽기 (두 줄)
        df_pop = pd.read_csv(POP_DATA_PATH, encoding="cp949", header=[0,1])

        # 첫 번째 컬럼명 '행정구역(시군구)별'
        # 양주시 데이터 필터링 (첫 컬럼, 첫 레벨 이름으로 필터)
        df_pop = df_pop[df_pop.iloc[:,0].str.contains("양주시")].reset_index(drop=True)

        # 두 번째 컬럼부터 인구수(월별) 데이터, 다중 컬럼명 (예: ('2011.01','총인구수 (명)'))
        # 연도별로 그룹핑해서 연평균 계산
        year_cols = {}
        for col in df_pop.columns[1:]:
            year = col[0][:4]
            if year not in year_cols:
                year_cols[year] = []
            year_cols[year].append(col)

        # 연도별 평균 인구수 계산
        year_avg = {}
        for y, cols in year_cols.items():
            # 해당 연도 월별 데이터 평균 (총인구수 (명) 컬럼만)
            vals = df_pop.loc[0, cols].values.astype(float)
            year_avg[int(y)] = np.mean(vals)

        # 5년 단위로 필터링
        years = sorted(year_avg.keys())
        years_5yr = [y for y in years if y >= 2005 and (y % 5 == 0 or y == years[-1])]
        pop_5yr_avg = [year_avg[y] for y in years_5yr]

        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.plot(years_5yr, pop_5yr_avg, marker='o', color='tab:green', label='인구수 (연평균)')
        ax.set_title("양주시 5년 단위 연평균 인구수 변화", fontproperties=font_prop, fontsize=12)
        ax.set_xlabel("연도", fontproperties=font_prop, fontsize=10)
        ax.set_ylabel("명", fontproperties=font_prop, fontsize=10)
        ax.set_xticks(years_5yr)
        ax.set_xticklabels(years_5yr, fontproperties=font_prop, fontsize=9)
        plt.yticks(fontproperties=font_prop, fontsize=9)
        plt.xticks(fontproperties=font_prop, fontsize=9)
        ax.legend(prop=font_prop, fontsize=10)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=False)
    except Exception as e:
        st.error(f"인구수 그래프 로드 중 오류가 발생했습니다: {e}")

    st.markdown("---")

    # --- 출생자수·사망자수 그래프 (기존 코드 재사용) ---
    BIRTH_DEATH_DATA_PATH = "양주시_연도별_출생자수_사망자수.csv"

    try:
        df = pd.read_csv(BIRTH_DEATH_DATA_PATH, encoding="cp949")
        df['행정구역별'] = df['행정구역별'].astype(str).str.strip()
        df_yg = df[df['행정구역별'] == "양주시"].reset_index(drop=True)

        colnames = list(df_yg.columns)
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
                        val = int(str(df_yg.iloc[0][col]).replace(",", "").strip())
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
                        val = int(float(str(df_yg.iloc[0][col]).replace(",", "").strip()))
                    except:
                        val = 0
                    deaths.append(val)

        common_years = sorted(list(set(birth_years) & set(death_years)))
        births_aligned = [births[birth_years.index(y)] for y in common_years]
        deaths_aligned = [deaths[death_years.index(y)] for y in common_years]

        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.plot(common_years, births_aligned, marker='o', color='tab:blue', label='출생자수')
        ax.plot(common_years, deaths_aligned, marker='o', color='tab:orange', label='사망자수')
        ax.set_title("양주시 5년 단위 출생자수·사망자수 변화", fontproperties=font_prop, fontsize=12)
        ax.set_xlabel("연도", fontproperties=font_prop, fontsize=10)
        ax.set_ylabel("명", fontproperties=font_prop, fontsize=10)
        ax.set_xticks(common_years)
        ax.set_xticklabels(common_years, fontproperties=font_prop, fontsize=9)
        plt.yticks(fontproperties=font_prop, fontsize=9)
        plt.xticks(fontproperties=font_prop, fontsize=9)
        ax.legend(prop=font_prop, fontsize=10)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=False)

        st.caption("양주시 인구 구조 변화를 5년 단위로 시각화. 데이터 출처: KOSIS 국가통계포털")
    except Exception as e:
        st.error(f"출생자수·사망자수 그래프 로드 중 오류가 발생했습니다: {e}")
