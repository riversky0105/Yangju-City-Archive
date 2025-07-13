import streamlit as st
import streamlit as st
st.set_page_config(page_title="Test", layout="centered")
st.write("✅ 여기는 출력 테스트용 입니다.")

# 이후 코드 주석 처리
# import pandas as pd
# ... (모든 아래 코드 주석)

st.set_page_config(page_title="양주시 아카이브 - GAMEBOY ADVANCE 스타일", layout="centered")

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import re
import numpy as np

# --- 이후 나머지 코드 계속 ---


# ---------- 1. CSS: GBA 본체+화면+버튼 ----------
st.markdown("""
<style>
body, .stApp { background: #222635; margin: 0; padding: 0; }
.gba-wrap {
    width: 100vw;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.gba-body {
    width: 950px; height: 510px;
    background: #6969c6;
    border-radius: 110px 110px 100px 100px / 180px 180px 110px 110px;
    box-shadow: 0 20px 80px #1a1a2c99, 0 1px 0 #fff5 inset;
    border: 12px solid #d0d7f7;
    position: relative;
    margin: 60px 0 18px 0;
}
.gba-title {
    position: absolute;
    left: 195px; top: 44px;
    font-family: 'Press Start 2P', monospace;
    color: #e7ffff;
    font-size: 2.10rem;
    letter-spacing: 2.2px;
    text-shadow: 0 0 12px #1de5fe, 0 0 17px #232946;
    z-index: 20;
    width: 540px;
    text-align: center;
    font-weight: bold;
    user-select: none;
}
.gba-screen {
    position: absolute;
    left: 155px; top: 120px;
    width: 640px; height: 320px;
    background: #151e2d;
    border-radius: 30px;
    border: 7px solid #202c48;
    box-shadow: 0 0 44px #00f2fe77 inset, 0 0 22px #151e2d;
    padding: 26px 36px 28px 36px;
    color: #b8f7f8;
    font-family: 'NanumGothicCoding', 'Press Start 2P', monospace;
    font-size: 18.5px;
    line-height: 1.65em;
    overflow-y: auto;
    z-index: 10;
    text-align: left;
    font-weight: 400;
}
.gba-btn {
    position: absolute;
    background: #232946cc;
    color: #fff;
    border-radius: 50%;
    border: 5.5px solid #a5faff;
    width: 68px; height: 68px;
    font-family: 'Press Start 2P', monospace;
    font-size: 2.15rem;
    text-align: center;
    line-height: 60px;
    cursor: pointer;
    box-shadow: 0 0 17px #00f2fecc, 0 0 2px #222;
    user-select:none;
    transition: background 0.16s, color 0.13s;
}
.gba-btn.left  { left: 45px;  top: 220px; }
.gba-btn.right { left: 837px; top: 220px; }
.gba-btn:active, .gba-btn:hover { background: #0d141f; color: #32e9f7; border-color: #fff;}
.gba-btn.start {
    left: 427px; top: 430px;
    border-radius: 19px;
    width: 120px; height: 44px;
    font-size: 1.15rem;
    line-height: 41px;
    background: #54f7fe;
    color: #232946;
    border: 3.5px solid #222946;
    font-weight: 700;
    box-shadow: 0 0 9px #fff, 0 0 6px #00e6ef;
}
.gba-btn.start:hover, .gba-btn.start:active { background: #232946; color: #54f7fe;}
.gba-logo {
    position: absolute;
    left: 320px; top: 480px;
    color: #fff;
    font-family: 'Press Start 2P', monospace;
    font-size: 1.25rem;
    letter-spacing: 2.2px;
    text-shadow: 0 0 9px #e9faff, 0 0 3px #232946;
}
@media (max-width:1050px) {
    .gba-body { width:98vw; }
    .gba-title { width:86vw; }
    .gba-screen { width:78vw; }
}
</style>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ---------- 2. 한글 플롯 폰트 적용 ----------
FONT_PATH = os.path.join("fonts", "NanumGothicCoding.ttf")
if os.path.exists(FONT_PATH):
    font_prop = fm.FontProperties(fname=FONT_PATH)
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False
else:
    font_prop = None

# ---------- 3. 섹션 내용 ----------
sections = ["📜 과거", "🏙️ 현재", "🌐 미래", "📊 인구 변화"]

section_texts = [
    """
    <b>1. 고려~조선 시대, 북방의 행정·군사 중심지</b><br>
    - 양주목 설치: 경기 북부 광역 행정 단위<br>
    - 조선시대 서울 외곽 방어선 역할<br>
    - 현재의 의정부, 동두천, 포천, 남양주 일대가 관할 지역<br><br>
    <b>2. 회암사: 왕실의 불교 수행처</b><br>
    - 태조 이성계 퇴위 후 회암사 중건, 세종 시대까지 국가 불교 중심지<br>
    - 승과(僧科) 시행 장소, 현재는 회암사지/국립 회암사지박물관<br><br>
    <b>3. 조선 후기 천주교 박해의 현장</b><br>
    - 신유박해(1801) 여성 신자 다수 순교, 강완숙·이순이 등<br>
    - 장흥면에 순교 기념비와 성지 조성<br><br>
    <b>4. 농업과 장터</b><br>
    - 장흥, 은현, 남면은 곡창지대, 읍내 장터는 한양 상인 교역<br><br>
    <b>5. 한국전쟁과 양주</b><br>
    - 1·4 후퇴 시 주요 격전지, 1951년 대규모 민간인 피해<br>
    - 전쟁 후 장기 복구 과정
    """,
    """
    <b>1. 인구와 행정</b><br>
    - 2025년 인구 약 29만 명, 면적 310.4㎢, 1읍 4면 7동<br>
    - 초중고대학 67교, 약 2,800여 개 공장·산업시설<br><br>
    <b>2. 신도시 개발 및 교통</b><br>
    - 옥정·회천 신도시 개발로 인구 급증(수도권 증가율 1위)<br>
    - 7호선 연장, GTX-C 등 광역교통망 확장<br><br>
    <b>3. 산업기반 확충</b><br>
    - 양주테크노밸리, 첨단산업단지 개발, 바이오/IT 기업 유치<br><br>
    <b>4. 문화·관광 자원 리브랜딩</b><br>
    - 장흥 조각공원, 송암천문대, 나리농원, 회암사지 등 관광 리브랜딩<br>
    - 전통+현대예술 융합, 청년예술가 지원<br><br>
    <b>5. 삶의 질과 복지</b><br>
    - 광역 복지관·체육시설 등 인프라 확충, 공원·녹지 조성
    """,
    """
    <b>1. 경기북부 중심도시 성장</b><br>
    - 수도권 동북부 거점도시, 주거→산업·문화·교육 복합도시<br>
    - 광역교통망 중심축<br><br>
    <b>2. 첨단산업·창업도시</b><br>
    - 테크노밸리·산업단지 중심, 청년 창업 및 스타트업 확대<br>
    - 4차산업 기반 경제 체질 개선<br><br>
    <b>3. 문화예술 중심도시</b><br>
    - 장흥문화예술촌, 청년 예술가, 회암사지 등 역사+콘텐츠 결합<br><br>
    <b>4. 탄소중립 스마트시티</b><br>
    - 스마트 교통, AI행정, 에너지 절감 도시계획, 도시숲·스마트팜<br><br>
    <b>5. 교육·복지 인프라</b><br>
    - 국공립 유치원·학교 확충, 대학/평생학습, 맞춤 복지
    """,
    """
    <b>양주시 인구 변화</b><br>
    - 인구수 변화/출생자수/사망자수(5년 단위, KOSIS)<br><br>
    <span style="font-size:17px;color:#fcf7ba;">아래에 그래프 시각화</span>
    """
]

# ---------- 4. 상태 관리 ----------
if "section_idx" not in st.session_state:
    st.session_state.section_idx = 0

# ---------- 5. 본체+버튼+화면+네비 ----------

st.markdown('<div class="gba-wrap">', unsafe_allow_html=True)
st.markdown('<div class="gba-body">', unsafe_allow_html=True)
st.markdown('<div class="gba-title">YANGJU ARCHIVE GAME</div>', unsafe_allow_html=True)

# 버튼 (왼/오/스타트)
left, right, start = False, False, False
colA, colB, colC = st.columns([2.6,1,2.6])
with colA: left = st.button("⬅️", key="left_gba", help="이전", use_container_width=True)
with colC: right = st.button("➡️", key="right_gba", help="다음", use_container_width=True)
with colB: start = st.button("START", key="start_gba", help="처음으로", use_container_width=True)

# 버튼 클릭에 따른 섹션 이동
if left:
    st.session_state.section_idx = (st.session_state.section_idx - 1) % len(sections)
if right:
    st.session_state.section_idx = (st.session_state.section_idx + 1) % len(sections)
if start:
    st.session_state.section_idx = 0

# ---------- 6. 아카이브 실제 화면 ----------
idx = st.session_state.section_idx
st.markdown(f'<div class="gba-screen">{section_texts[idx]}</div>', unsafe_allow_html=True)

# ---------- 7. 인구변화 그래프 (섹션4에서만) ----------
if idx == 3:
    POP_DATA_PATH = "양주시_연도별_인구수.csv"
    try:
        df_pop = pd.read_csv(POP_DATA_PATH, encoding="cp949", header=[0,1])
        df_pop = df_pop[df_pop.iloc[:, 0].str.contains("양주시")].reset_index(drop=True)
        year_cols = {}
        for col in df_pop.columns[1:]:
            year = col[0][:4]
            if year not in year_cols:
                year_cols[year] = []
            year_cols[year].append(col)
        year_avg = {}
        for y, cols in year_cols.items():
            vals = df_pop.loc[0, cols].values.astype(float)
            year_avg[int(y)] = np.mean(vals)
        years = sorted(year_avg.keys())
        years_5yr = [y for y in years if y >= 2005 and (y % 5 == 0 or y == years[-1])]
        pop_5yr_avg = [year_avg[y] for y in years_5yr]
        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.plot(years_5yr, pop_5yr_avg, marker='o', color='tab:green', label='인구수 (연평균)')
        if font_prop:
            ax.set_title("양주시 연평균 인구수 변화", fontproperties=font_prop, fontsize=12)
            ax.set_xlabel("연도", fontproperties=font_prop, fontsize=10)
            ax.set_ylabel("명", fontproperties=font_prop, fontsize=10)
            ax.set_xticklabels(years_5yr, fontproperties=font_prop, fontsize=9)
            plt.yticks(fontproperties=font_prop, fontsize=9)
            plt.xticks(fontproperties=font_prop, fontsize=9)
            ax.legend(prop=font_prop, fontsize=10)
        else:
            ax.set_title("양주시 연평균 인구수 변화", fontsize=12)
            ax.set_xlabel("연도", fontsize=10)
            ax.set_ylabel("명", fontsize=10)
            ax.set_xticklabels(years_5yr, fontsize=9)
            plt.yticks(fontsize=9)
            plt.xticks(fontsize=9)
            ax.legend(fontsize=10)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=False)
    except Exception as e:
        st.error(f"인구수 그래프 로드 중 오류: {e}")

    st.markdown("---")

    # 출생/사망 그래프
    BIRTH_DEATH_DATA_PATH = "양주시_연도별_출생자수_사망자수.csv"
    try:
        df = pd.read_csv(BIRTH_DEATH_DATA_PATH, encoding="cp949")
        df['행정구역별'] = df['행정구역별'].astype(str).str.strip()
        df_yg = df[df['행정구역별'] == "양주시"].reset_index(drop=True)
        colnames = list(df_yg.columns)
        birth_cols = [col for col in colnames if col != "행정구역별" and "." not in col]
        death_cols = [col for col in colnames if col != "행정구역별" and "." in col]
        birth_years, births = [], []
        for col in birth_cols:
            m = re.match(r"(\d{4})", col)
            if m:
                y = int(m.group(1))
                if y >= 2005 and (y % 5 == 0 or y == int(birth_cols[-1][:4])):
                    birth_years.append(y)
                    try: births.append(int(str(df_yg.iloc[0][col]).replace(",", "").strip()))
                    except: births.append(0)
        death_years, deaths = [], []
        for col in death_cols:
            m = re.match(r"(\d{4})", col)
            if m:
                y = int(m.group(1))
                if y >= 2005 and (y % 5 == 0 or y == int(death_cols[-1][:4])):
                    death_years.append(y)
                    try: deaths.append(int(float(str(df_yg.iloc[0][col]).replace(",", "").strip())))
                    except: deaths.append(0)
        common_years = sorted(set(birth_years) & set(death_years))
        births_aligned = [births[birth_years.index(y)] for y in common_years]
        deaths_aligned = [deaths[death_years.index(y)] for y in common_years]
        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.plot(common_years, births_aligned, marker='o', color='tab:blue', label='출생자수')
        ax.plot(common_years, deaths_aligned, marker='o', color='tab:orange', label='사망자수')
        if font_prop:
            ax.set_title("양주시 출생자수·사망자수 변화", fontproperties=font_prop, fontsize=12)
            ax.set_xlabel("연도", fontproperties=font_prop, fontsize=10)
            ax.set_ylabel("명", fontproperties=font_prop, fontsize=10)
            ax.set_xticklabels(common_years, fontproperties=font_prop, fontsize=9)
            plt.yticks(fontproperties=font_prop, fontsize=9)
            plt.xticks(fontproperties=font_prop, fontsize=9)
            ax.legend(prop=font_prop, fontsize=10)
        else:
            ax.set_title("양주시 출생자수·사망자수 변화", fontsize=12)
            ax.set_xlabel("연도", fontsize=10)
            ax.set_ylabel("명", fontsize=10)
            ax.set_xticklabels(common_years, fontsize=9)
            plt.yticks(fontsize=9)
            plt.xticks(fontsize=9)
            ax.legend(fontsize=10)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=False)
        st.caption("양주시 인구 구조 변화를 5년 단위로 시각화. 데이터 출처: KOSIS 국가통계포털")
    except Exception as e:
        st.error(f"출생/사망 그래프 로드 중 오류: {e}")

st.markdown('<div class="gba-logo">GAMEBOY ADVANCE</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)   # .gba-body
st.markdown('</div>', unsafe_allow_html=True)   # .gba-wrap
