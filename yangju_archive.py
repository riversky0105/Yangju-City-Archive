import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import re

# 1. 한글 폰트 설정
FONT_PATH = os.path.join("fonts", "NanumGothicCoding.ttf")
if os.path.exists(FONT_PATH):
    font_prop = fm.FontProperties(fname=FONT_PATH)
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False
else:
    font_prop = None

# 2. Streamlit 기본 세팅
st.set_page_config(page_title="양주시 아카이브: 과거, 현재, 미래", layout="wide")
st.title("🏙️ 양주시 아카이브: 과거, 현재, 미래")
st.markdown("경기도 양주시의 역사와 미래 비전을 살펴보는 디지털 아카이브입니다.")

# 3. 탭 메뉴 구성
tabs = st.tabs(["📜 과거", "🏙️ 현재", "🌐 미래"])

# 4. 과거 탭
with tabs[0]:
    st.header("📜 양주시의 과거")
    st.subheader("1. 고려~조선 시대, 북방의 행정·군사 중심지")
    st.markdown("""
    - 양주목 설치: 경기 북부 광역 행정 단위  
    - 조선시대 서울 외곽 방어선 역할  
    - 현재의 의정부, 동두천, 포천, 남양주 일대가 관할 지역
    """)
    st.subheader("2. 회암사: 왕실의 불교 수행처")
    st.markdown("""
    - 태조 이성계 퇴위 후 회암사 중건  
    - 세종 시대까지 국가 불교 중심지로 기능  
    - 승과(僧科) 시행 장소  
    - 현재는 회암사지 및 국립 회암사지박물관으로 보존
    """)
    st.subheader("3. 조선 후기 천주교 박해의 현장")
    st.markdown("""
    - 신유박해(1801) 시기 여성 신자 다수 순교  
    - 강완숙, 이순이 등 순교자 기록  
    - 장흥면에 순교 기념비, 성지 조성
    """)
    st.subheader("4. 한국전쟁과 양주")
    st.markdown("""
    - 1·4 후퇴 시 주요 격전지  
    - 1951년 대규모 민간인 피해  
    - 전쟁 후 장기 복구 과정
    """)
    st.subheader("5. 농업과 장터")
    st.markdown("""
    - 장흥, 은현, 남면은 조선시대 곡창지대  
    - 읍내 장터는 한양 상인과의 활발한 교역지
    """)

# 5. 현재 탭
with tabs[1]:
    st.header("🏙️ 양주시의 현재")
    st.markdown("""
1. **인구와 행정**
    - 2025년 인구 약 29만 명, 면적 310.4㎢, 1읍 4면 7동.
    - 초중고대학 67교, 약 2,800여 개의 공장 및 산업시설이 위치.
2. **신도시 개발 및 교통**
    - 옥정·회천 신도시 개발로 수도권 내 인구 급증(최근 수도권 증가율 1위).
    - 7호선 연장, GTX-C 개통 등 서울 접근성 좋은 광역교통망 빠르게 확장.
3. **산업기반 확충**
    - 양주테크노밸리, 첨단산업단지 개발
    - 의료·바이오·IT 기업 유치 및 고용 창출, 세수 확대
4. **문화·관광 자원 리브랜딩**
    - 장흥 조각공원, 송암천문대, 나리농원, 회암사지 등 관광자원 리브랜딩
    - 전통+현대예술 융합, 청년예술가 지원
5. **도시·농촌 복합형 구조**
    - 도심은 아파트 중심, 외곽은 농촌·산림지
    - 다양한 커뮤니티와 라이프스타일 공존
    """)
    st.markdown("---")

    st.subheader("📊 양주시 5년 단위 연도별 출생자수·사망자수 (2005~최신)")

    DATA_PATH = "양주시_연도별_출생자수_사망자수.csv"
    try:
        # 데이터 불러오기 (cp949로 인코딩)
        df = pd.read_csv(DATA_PATH, encoding="cp949")
        df['행정구역별'] = df['행정구역별'].astype(str).str.strip()
        df_yg = df[df['행정구역별'] == "양주시"]

        # 연도 추출 (헤더에서 4자리 연도만 추출)
        year_pattern = re.compile(r"(\d{4})\s*출생건수")
        years = []
        for col in df_yg.columns:
            m = year_pattern.match(col)
            if m:
                years.append(int(m.group(1)))

        # 2005년 이상, 5년 단위, 마지막 연도(최신) 포함
        base_years = [y for y in years if y >= 2005 and y % 5 == 0]
        if years and years[-1] not in base_years:
            base_years.append(years[-1])

        births = []
        deaths = []
        for y in base_years:
            birth_col = f"{y} 출생건수 (명)"
            death_col = f"{y} 사망건수 (명)"
            # 혹시 컬럼명이 미묘하게 다를 수 있으니 정규식 보조
            if birth_col not in df_yg.columns:
                for c in df_yg.columns:
                    if re.fullmatch(f"{y}\s*출생건수.*", c): birth_col = c
            if death_col not in df_yg.columns:
                for c in df_yg.columns:
                    if re.fullmatch(f"{y}\s*사망건수.*", c): death_col = c
            births.append(int(df_yg[birth_col].values[0]))
            deaths.append(int(df_yg[death_col].values[0]))

        # 시각화 (크기 축소 & 가독성 개선)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(base_years, births, marker='o', label='출생자수')
        ax.plot(base_years, deaths, marker='o', label='사망자수')
        ax.set_title("양주시 5년 단위 출생자수·사망자수 변화", fontproperties=font_prop, fontsize=14)
        ax.set_xlabel("연도", fontproperties=font_prop, fontsize=11)
        ax.set_ylabel("명", fontproperties=font_prop, fontsize=11)
        ax.set_xticks(base_years)
        ax.set_xticklabels(base_years, fontproperties=font_prop, fontsize=10)
        ax.legend(prop=font_prop, fontsize=11)
        plt.yticks(fontproperties=font_prop, fontsize=10)
        plt.tight_layout()
        st.pyplot(fig)
        st.caption("양주시 인구 구조 변화를 5년 단위로 시각화. 데이터 출처: KOSIS 국가통계포털")
    except Exception as e:
        st.warning(f"그래프를 불러오는 중 오류가 발생했습니다: {e}")

# 6. 미래 탭
with tabs[2]:
    st.header("🌐 양주시의 미래")
    st.subheader("1. 경기북부 중심도시 성장")
    st.markdown("""
    - 수도권 동북부 거점도시로 발전  
    - 주거 중심에서 산업·문화·교육 복합도시로 전환  
    - 광역교통망 중심축으로 기대
    """)
    st.subheader("2. 첨단산업과 창업도시")
    st.markdown("""
    - 테크노밸리, 산업단지 중심 개발  
    - 청년 창업 및 스타트업 인큐베이팅  
    - 4차 산업 기반의 경제 체질 개선
    """)
    st.subheader("3. 문화예술 중심도시")
    st.markdown("""
    - 장흥문화예술촌 레지던시 확대  
    - 청년 예술가 정착 유도  
    - 회암사지 등 역사와 콘텐츠 결합한 스토리텔링
    """)
    st.subheader("4. 탄소중립 스마트시티")
    st.markdown("""
    - 스마트 교통, AI 행정 도입  
    - 공공건물 태양광 등 에너지 절감 도시계획  
    - 생태공원, 도시숲, 스마트팜 확장
    """)
    st.subheader("5. 교육·복지 인프라")
    st.markdown("""
    - 국공립 유치원 및 학교 확충  
    - 지역 대학 및 평생학습 거점 마련  
    - 맞춤형 복지 설계: 고령자, 청년, 다문화 가정 대상
    """)
