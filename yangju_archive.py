import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 🔵 스타일
st.markdown("""
    <style>
    html, body, [class*="css"]  { font-size: 16px !important; }
    .stMarkdown, .stText, .stSubheader, .stHeader, .stTitle { font-size: 18px !important; line-height: 1.7 !important; }
    .stApp { font-size: 16px !important; }
    </style>
""", unsafe_allow_html=True)

# 한글 폰트
FONT_PATH = os.path.join("fonts", "NanumGothicCoding.ttf")
font_prop = None
if os.path.exists(FONT_PATH):
    font_prop = fm.FontProperties(fname=FONT_PATH)
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="양주시 아카이브: 과거, 현재, 미래", layout="wide")
st.title("🏙️ 양주시 아카이브: 과거, 현재, 미래")
st.markdown("<span style='font-size:15pt;'>경기도 양주시의 역사와 미래 비전을 살펴보는 디지털 아카이브입니다.</span>", unsafe_allow_html=True)

tabs = st.tabs(["📜 과거", "🏙️ 현재", "🌐 미래"])

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

    st.subheader("양주시 5년 단위 연도별 출생자수·사망자수 (2005~최신)")

    DATA_PATH = "양주시_연도별_출생자수_사망자수.csv"
    try:
        df = pd.read_csv(DATA_PATH, encoding="cp949")
        df = df[df['행정구역별'] == '양주시'].reset_index(drop=True)

        # 출생자수/사망자수 컬럼명 추출
        cols = df.columns.tolist()
        birth_years, birth_vals = [], []
        death_years, death_vals = [], []
        for c in cols:
            if "출생건수" in c and c != "출생건수":
                year = c.split()[0].replace('.1', '')
                if year.isdigit() and int(year) >= 2005 and (int(year)-2005)%5 == 0:
                    birth_years.append(int(year))
                    birth_vals.append(int(str(df[c].values[0]).replace(",", "").strip()))
            if "사망건수" in c and c != "사망건수":
                year = c.split()[0].replace('.1', '')
                if year.isdigit() and int(year) >= 2005 and (int(year)-2005)%5 == 0:
                    death_years.append(int(year))
                    death_vals.append(int(str(df[c].values[0]).replace(",", "").strip()))

        # 혹시 마지막(최신) 연도가 포함 안 되어있으면 추가
        last_birth_col = [c for c in cols if "출생건수" in c and c != "출생건수"][-1]
        last_birth_year = int(last_birth_col.split()[0].replace('.1',''))
        if last_birth_year not in birth_years:
            birth_years.append(last_birth_year)
            birth_vals.append(int(str(df[last_birth_col].values[0]).replace(",", "").strip()))
        last_death_col = [c for c in cols if "사망건수" in c and c != "사망건수"][-1]
        last_death_year = int(last_death_col.split()[0].replace('.1',''))
        if last_death_year not in death_years:
            death_years.append(last_death_year)
            death_vals.append(int(str(df[last_death_col].values[0]).replace(",", "").strip()))

        # 표로 먼저 확인
        st.markdown("#### ▶️ 출생자수 Raw 데이터")
        st.dataframe(pd.DataFrame({"연도": birth_years, "출생자수": birth_vals}))
        st.markdown("#### ▶️ 사망자수 Raw 데이터")
        st.dataframe(pd.DataFrame({"연도": death_years, "사망자수": death_vals}))

        # 출생자수 그래프
        fig1, ax1 = plt.subplots(figsize=(4,2.5))
        ax1.plot(birth_years, birth_vals, marker='o', color='royalblue')
        ax1.set_title("양주시 5년 단위 출생자수 변화", fontproperties=font_prop, fontsize=13)
        ax1.set_xlabel("연도", fontproperties=font_prop, fontsize=11)
        ax1.set_ylabel("명", fontproperties=font_prop, fontsize=11)
        ax1.set_xticks(birth_years)
        plt.yticks(fontproperties=font_prop, fontsize=10)
        plt.xticks(fontproperties=font_prop, fontsize=10)
        plt.tight_layout()
        st.pyplot(fig1)

        # 사망자수 그래프
        fig2, ax2 = plt.subplots(figsize=(4,2.5))
        ax2.plot(death_years, death_vals, marker='o', color='orange')
        ax2.set_title("양주시 5년 단위 사망자수 변화", fontproperties=font_prop, fontsize=13)
        ax2.set_xlabel("연도", fontproperties=font_prop, fontsize=11)
        ax2.set_ylabel("명", fontproperties=font_prop, fontsize=11)
        ax2.set_xticks(death_years)
        plt.yticks(fontproperties=font_prop, fontsize=10)
        plt.xticks(fontproperties=font_prop, fontsize=10)
        plt.tight_layout()
        st.pyplot(fig2)

        st.caption("양주시 인구 구조 변화를 5년 단위로 시각화. 데이터 출처: KOSIS 국가통계포털")
    except Exception as e:
        st.warning(f"그래프 오류: {e}")

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























DATA_PATH = "양주시_연도별_출생자수_사망자수.csv"

df = pd.read_csv(DATA_PATH, encoding="cp949")
st.write("전체 데이터 미리보기:")
st.dataframe(df)

st.write("컬럼명:")
st.write(df.columns.tolist())

# 양주시만 추출
df_yg = df[df['행정구역별'] == '양주시']
st.write("양주시 데이터만 추출:")
st.dataframe(df_yg)

if df_yg.empty:
    st.error("⚠️ '양주시' 데이터가 없습니다. 행정구역별 컬럼명과 값을 다시 확인하세요.")
else:
    st.success("'양주시' 행 추출 성공!")
    st.write("양주시 데이터의 컬럼(헤더):", df_yg.columns.tolist())
    st.write("양주시 데이터의 값:", df_yg.values.tolist())

