import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import re
import numpy as np

# 1. GBA 스타일 CSS 및 배경 이미지
GBA_FRAME_IMG = "https://i.imgur.com/6hzvEBK.png"  # 게임보이 어드밴스 투명 배경 PNG

st.set_page_config(page_title="양주시 아카이브 GAME", layout="wide")

st.markdown(f"""
<style>
body, .stApp {{
    background: #232946;
}}

.gba-wrap {{
    position: relative;
    width: 640px;
    height: 420px;
    margin: 40px auto 0 auto;
    background: transparent;
}}

.gba-frame {{
    position: absolute;
    width: 640px;
    height: 420px;
    left: 0; top: 0;
    z-index: 1;
    pointer-events: none;
}}

.gba-screen {{
    position: absolute;
    left: 102px;
    top: 68px;
    width: 434px;
    height: 210px;
    background: #181c2b;
    border-radius: 22px;
    border: 6px solid #262b3a;
    z-index: 2;
    overflow: auto;
    box-shadow: 0 0 24px #00f2fe55;
    padding: 14px 18px 10px 18px;
    color: #e0fcff;
    font-family: 'NanumGothicCoding', monospace;
    font-size: 0.9rem;
}}

.gba-btn {{
    position: absolute;
    z-index: 10;
    background: #fff8;
    border: 2px solid #232946cc;
    border-radius: 50%;
    width: 38px;
    height: 38px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.7rem;
    color: #222a41;
    font-family: 'Press Start 2P', monospace;
    box-shadow: 0 0 5px #00f2fe33;
    cursor: pointer;
    transition: background 0.12s;
}}
.gba-btn:active {{ background: #00f2fe66; }}

.gba-btn-left {{ left: 32px;  top: 178px; }}
.gba-btn-right {{ left: 570px; top: 178px; }}
.gba-btn-start {{
    left: 307px; top: 340px;
    width: 54px;
    border-radius: 18px;
    height: 29px;
    font-size:1.2rem;
    pointer-events:auto;
    color:#00f2fe;
    background: #111a2dcc;
    border: 2px solid #00f2feaa;
    box-shadow: 0 0 15px #00f2fecc;
}}

.gba-logo {{
    font-family: 'Press Start 2P', monospace;
    color: #fff;
    font-size: 1.08rem;
    letter-spacing: 2px;
    position: absolute;
    left: 200px; top: 32px; z-index:12;
    text-shadow: 0 0 8px #000, 0 0 4px #3af2ff;
}}
.gba-tip {{
    position:absolute;
    left:50%;
    transform:translateX(-50%);
    top:395px;
    color:#a6e3e9;
    font-family:'Press Start 2P',monospace;
    font-size:0.9rem;
    z-index:13;
    background:rgba(24,28,43,0.6);
    padding:2px 18px;
    border-radius:13px;
    border:1.5px solid #a6e3e9;
    box-shadow:0 0 4px #00f2fe99;
}}
</style>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# 2. 한글 플롯 폰트 (옵션)
FONT_PATH = os.path.join("fonts", "NanumGothicCoding.ttf")
if os.path.exists(FONT_PATH):
    font_prop = fm.FontProperties(fname=FONT_PATH)
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False
else:
    font_prop = None

# 3. 섹션 상태 관리
sections = ["📜 과거", "🏙️ 현재", "🌐 미래", "📊 인구 변화"]
if "section_idx" not in st.session_state:
    st.session_state["section_idx"] = 0
if "started" not in st.session_state:
    st.session_state["started"] = False

# 4. GBA 프레임 + 화면 구조 시작
st.markdown('<div class="gba-wrap">', unsafe_allow_html=True)
st.markdown(f'<img class="gba-frame" src="{GBA_FRAME_IMG}">', unsafe_allow_html=True)

# 5. 시작 화면
if not st.session_state["started"]:
    st.markdown(f'''
    <div class="gba-logo">YANGJU ARCHIVE GAME</div>
    <div class="gba-screen" style="display:flex;flex-direction:column;align-items:center;justify-content:center; font-size:1.3rem; color:#00f2fe; text-shadow: 0 0 15px #00f2feaa;">
        양주시 아카이브<br>
        경기도 양주시의 역사와 미래 비전을<br>게임보이 어드밴스 화면처럼 구경하세요!
        <br><br><span style="font-size:1.0rem; color:#a6e3e9; text-shadow:none;">START 버튼을 눌러 시작</span>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown(f'''
        <button class="gba-btn gba-btn-start" onclick="window.parent.postMessage({{type:'streamlit:buttonClick', buttonId:'start_btn'}},'*');">START</button>
        <div class="gba-tip">Start 버튼 또는 아래 버튼 클릭!</div>
    ''', unsafe_allow_html=True)
    if st.button("START", key="start_btn", help="게임 시작", type="primary"):
        st.session_state["started"] = True
        st.session_state["section_idx"] = 0
        st.experimental_rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 6. 실제 아카이브 화면 + 좌/우 버튼
st.markdown(f'''
<button class="gba-btn gba-btn-left" onclick="window.parent.postMessage({{type:'streamlit:buttonClick', buttonId:'left_btn'}},'*');">◀</button>
<button class="gba-btn gba-btn-right" onclick="window.parent.postMessage({{type:'streamlit:buttonClick', buttonId:'right_btn'}},'*');">▶</button>
<div class="gba-btn gba-btn-start" style="pointer-events:none;opacity:0.4;">START</div>
<div class="gba-logo">YANGJU ARCHIVE GAME</div>
<div class="gba-tip">{sections[st.session_state.section_idx]} &nbsp;&nbsp; | &nbsp; 좌/우 버튼으로 이동</div>
<div class="gba-screen">
''', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,8,1])
with col1:
    if st.button("◀", key="left_btn"):
        st.session_state.section_idx = (st.session_state.section_idx - 1) % len(sections)
        st.experimental_rerun()
with col3:
    if st.button("▶", key="right_btn"):
        st.session_state.section_idx = (st.session_state.section_idx + 1) % len(sections)
        st.experimental_rerun()

st.markdown(f"<div style='font-family:Press Start 2P, monospace; color:#e0fcff;text-align:center;font-size:1.1rem;margin:7px 0;'>{sections[st.session_state.section_idx]}</div>", unsafe_allow_html=True)

# 7. 섹션별 콘텐츠

if st.session_state.section_idx == 0:
    st.markdown('<div style="color:#fff;font-size:0.85rem;">', unsafe_allow_html=True)
    st.header("📜 양주시의 과거")
    st.markdown("""
    <b>1. 고려~조선 시대, 북방의 행정·군사 중심지</b><br>
    - 양주목 설치: 경기 북부 광역 행정 단위<br>
    - 조선시대 서울 외곽 방어선 역할<br>
    - 현재의 의정부, 동두천, 포천, 남양주 일대가 관할 지역<br><br>
    <b>2. 회암사: 왕실의 불교 수행처</b><br>
    - 태조 이성계 퇴위 후 회암사 중건<br>
    - 세종 시대까지 국가 불교 중심지로 기능<br>
    - 승과(僧科) 시행 장소<br>
    - 현재는 회암사지 및 국립 회암사지박물관으로 보존<br><br>
    <b>3. 조선 후기 천주교 박해의 현장</b><br>
    - 신유박해(1801) 시기 여성 신자 다수 순교<br>
    - 강완숙, 이순이 등 순교자 기록<br>
    - 장흥면에 순교 기념비, 성지 조성<br><br>
    <b>4. 농업과 장터</b><br>
    - 장흥, 은현, 남면은 조선시대 곡창지대<br>
    - 읍내 장터는 한양 상인과의 활발한 교역지<br><br>
    <b>5. 한국전쟁과 양주</b><br>
    - 1·4 후퇴 시 주요 격전지<br>
    - 1951년 대규모 민간인 피해<br>
    - 전쟁 후 장기 복구 과정<br>
    """, unsafe_allow_html=True)
    st.image("양주 관야지.jpg", caption="양주 관아지(양주목 관아터)", width=380)
    st.image("회암사지.jpg", caption="회암사지 터", width=380)
    st.image("회암사지 복원도.jpg", caption="회암사지 추정 복원도", width=380)
    st.image("양주 장흥 순교성지.jpg", caption="양주 장흥 순교성지", width=380)
    st.image("양주 농촌.jpg", caption="1950~1980년대 논 모내기 풍경", width=380)
    st.image("양주 장터.jpg", caption="1970~1980년대 시골 장터", width=380)
    st.image("양주 1.4후퇴.jpg", caption="1951년 1.4후퇴 당시 경기북부 피난민 행렬", width=380)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.section_idx == 1:
    st.markdown('<div style="color:#fff;font-size:0.85rem;">', unsafe_allow_html=True)
    st.header("🏙️ 양주시의 현재")
    st.markdown("""
    <b>1. 인구와 행정</b><br>
    - 2025년 인구 약 29만 명, 면적 310.4㎢, 1읍 4면 7동.<br>
    - 초중고대학 67교, 약 2,800여 개의 공장 및 산업시설이 위치.<br><br>
    <b>2. 신도시 개발 및 교통</b><br>
    - 옥정·회천 신도시 개발로 수도권 내 인구 급증(최근 수도권 증가율 1위).<br>
    - 7호선 연장, GTX-C 개통 등 서울 접근성 좋은 광역교통망 빠르게 확장.<br><br>
    <b>3. 산업기반 확충</b><br>
    - 양주테크노밸리, 첨단산업단지 개발<br>
    - 의료·바이오·IT 기업 유치 및 고용 창출, 세수 확대<br><br>
    <b>4. 문화·관광 자원 리브랜딩</b><br>
    - 장흥 조각공원, 송암천문대, 나리농원, 회암사지 등 관광자원 리브랜딩<br>
    - 전통+현대예술 융합, 청년예술가 지원<br><br>
    <b>5. 삶의 질을 높이는 복지와 생활환경</b><br>
    - 광역 복지관, 문화센터, 체육시설 등 생활 인프라 대폭 확충<br>
    - 청년·고령자·다문화가정 등 맞춤 복지 정책 강화<br>
    - 쾌적한 공원, 녹지, 생활체육 환경 조성<br>
    """, unsafe_allow_html=True)
    st.image("양주시 면적.jpg", caption="양주시 행정구역도", width=380)
    st.image("양주 옥정신도시.jpg", caption="양주 옥정 신도시", width=380)
    st.image("양주 산업단지.jpg", caption="양주 은남일반산업단지", width=380)
    st.image("양주시 나리농원 천일홍 축제.jpg", caption="양주시 나리농원 천일홍 축제", width=380)
    st.image("양주 옥정 호수공원.jpg", caption="양주 옥정 호수공원", width=380)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.section_idx == 2:
    st.markdown('<div style="color:#fff;font-size:0.85rem;">', unsafe_allow_html=True)
    st.header("🌐 양주시의 미래")
    st.markdown("""
    <b>1. 경기북부 중심도시 성장</b><br>
    - 수도권 동북부 거점도시로 발전<br>
    - 주거 중심에서 산업·문화·교육 복합도시로 전환<br>
    - 광역교통망 중심축으로 기대<br><br>
    <b>2. 첨단산업과 창업도시</b><br>
    - 테크노밸리, 산업단지 중심 개발<br>
    - 청년 창업 및 스타트업 인큐베이팅<br>
    - 4차 산업 기반의 경제 체질 개선<br><br>
    <b>3. 문화예술 중심도시</b><br>
    - 장흥문화예술촌 레지던시 확대<br>
    - 청년 예술가 정착 유도<br>
    - 회암사지 등 역사와 콘텐츠 결합한 스토리텔링<br><br>
    <b>4. 탄소중립 스마트시티</b><br>
    - 스마트 교통, AI 행정 도입<br>
    - 공공건물 태양광 등 에너지 절감 도시계획<br>
    - 생태공원, 도시숲, 스마트팜 확장<br><br>
    <b>5. 교육·복지 인프라</b><br>
    - 국공립 유치원 및 학교 확충<br>
    - 지역 대학 및 평생학습 거점 마련<br>
    - 맞춤형 복지 설계: 고령자, 청년, 다문화 가정 대상<br>
    """, unsafe_allow_html=True)
    st.image("양주 GTX 노선도.jpg", caption="양주를 지나는 GTX-C(예정) 노선", width=380)
    st.image("양주 테크노벨리.png", caption="양주 테크노밸리(조감도)", width=380)
    st.image("양주 문화 예술.jpg", caption="양주 장흥문화예술촌(실내/전시)", width=380)
    st.image("양주 탄소중립 스마트시티.jpg", caption="양주 생태공원 및 친환경 스마트시티", width=380)
    st.image("양주시 청년센터.jpg", caption="양주시 청년센터(옥정동)", width=380)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.section_idx == 3:
    st.markdown('<div style="color:#fff;font-size:0.85rem;">', unsafe_allow_html=True)
    st.header("📊 양주시 인구 변화")
    st.markdown("""
    <span style='color:#fff;'>양주시 인구 구조 변화를 월별/연도별 및 5년 단위 출생자수·사망자수와 함께 시각화합니다. 데이터 출처: KOSIS 국가통계포털</span>
    """, unsafe_allow_html=True)
    # 인구수 변화 그래프
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
        st.error(f"인구수 그래프 로드 중 오류가 발생했습니다: {e}")

    st.markdown("---")

    # 출생자수·사망자수 그래프
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
        st.error(f"출생자수·사망자수 그래프 로드 중 오류가 발생했습니다: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# 8. 닫기 div (GBA wrap)
st.markdown('</div>', unsafe_allow_html=True)
