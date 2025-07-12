import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 1. 폰트 설정 (NanumGothicCoding.ttf는 fonts 폴더에 있어야 함)
FONT_PATH = os.path.join("fonts", "NanumGothicCoding.ttf")
if os.path.exists(FONT_PATH):
    font_prop = fm.FontProperties(fname=FONT_PATH)
else:
    font_prop = None

st.set_page_config(page_title="양주시 아카이브", layout="wide")

# 사용자 정의 CSS로 문단 간격 조정
st.markdown("""
    <style>
        .markdown-text-container {
            line-height: 1.8;  /* 줄 간격 */
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        h1, h2, h3 {
            margin-top: 1.2em;
            margin-bottom: 0.6em;
        }
        p {
            margin-bottom: 1.2em;  /* 문단 간격 */
        }
    </style>
""", unsafe_allow_html=True)

st.title("🏙️ 양주시 아카이브: 과거, 현재, 미래")
st.markdown("경기도 양주시의 역사와 미래 비전을 살펴보는 디지털 아카이브입니다.")

tabs = st.tabs(["📜 과거", "🏙️ 현재", "🌐 미래"])

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

with tabs[1]:
    st.header("🏙️ 양주시의 현재")
    st.subheader("1. 인구와 행정")
    st.markdown("""
    - 2025년 인구 약 29만 명, 면적 310.4㎢, 1읍 4면 7동.
    - 초중고대학 67교, 약 2,800여 개의 공장 및 산업시설이 위치.
    """)
    st.subheader("2. 신도시 개발 및 교통")
    st.markdown("""
    - 옥정·회천 신도시 개발로 수도권 내 인구 급증(최근 수도권 증가율 1위).
    - 7호선 연장, GTX-C 개통 등 서울 접근성 높은 광역교통망 빠르게 확장.
    """)
    st.subheader("3. 산업기반 확충")
    st.markdown("""
    - 양주테크노밸리, 첨단산업단지 개발
    - 의료·바이오·IT 기업 유치 및 고용 창출, 세수 확대
    """)
    st.subheader("4. 문화·관광 자원 리브랜딩")
    st.markdown("""
    - 장흥 조각공원, 송암천문대, 나리농원, 회암사지 등 관광자원 리브랜딩
    - 전통+현대예술 융합, 청년예술가 지원
    """)
    st.subheader("5. 도시·농촌 복합형 구조")
    st.markdown("""
    - 도심은 아파트 중심, 외곽은 농촌·산림지  
    - 다양한 커뮤니티와 라이프스타일 공존
    """)

    # 🔥 여기에 최신 출생·사망자수 시각화 그래프 추가
    st.markdown("---")
    st.subheader("📊 양주시 연도별 출생자수·사망자수 (2003~2024)")
    st.markdown("양주시의 인구 구조 변화를 확인할 수 있는 통계 그래프입니다. 데이터 출처: KOSIS 국가통계포털")

    # 데이터 불러오기 및 그래프 시각화
    DATA_PATH = "양주시_연도별_출생자수_사망자수.csv"
    try:
        df = pd.read_csv(DATA_PATH, encoding="cp949")
        # '행정구역별'이 있으면 '양주시'만 추출
        if '행정구역별' in df.columns:
            df = df[df['행정구역별'] == '양주시']

        # 연도/출생/사망 추출
        data = []
        for col in df.columns:
            if '출생건수' in col:
                year = col.split()[0]
                birth = int(df[col].values[0])
                death_col = f"{year} 사망건수 (명)"
                if death_col in df.columns:
                    death = int(df[death_col].values[0])
                    data.append([int(year), birth, death])
        df_plt = pd.DataFrame(data, columns=['연도', '출생자수', '사망자수'])
        df_plt = df_plt.sort_values('연도')

        # 그래프
        fig, ax = plt.subplots(figsize=(10,5))
        ax.plot(df_plt['연도'], df_plt['출생자수'], marker='o', label='출생자수')
        ax.plot(df_plt['연도'], df_plt['사망자수'], marker='o', label='사망자수')
        ax.set_title("양주시 연도별 출생자수·사망자수", fontproperties=font_prop, fontsize=18)
        ax.set_xlabel("연도", fontproperties=font_prop, fontsize=14)
        ax.set_ylabel("명", fontproperties=font_prop, fontsize=14)
        ax.legend(prop=font_prop, fontsize=12)
        ax.set_xticks(df_plt['연도'])
        ax.set_xticklabels(df_plt['연도'], fontproperties=font_prop, rotation=45)
        ax.tick_params(axis='y', labelsize=12)
        plt.yticks(fontproperties=font_prop)
        plt.tight_layout()
        st.pyplot(fig)
    except Exception as e:
        st.warning(f"그래프를 불러오는 중 오류가 발생했습니다: {e}")

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

