import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import re

# 0. 폰트(한글 플롯) 세팅
FONT_PATH = os.path.join("fonts", "NanumGothicCoding.ttf")
if os.path.exists(FONT_PATH):
    font_prop = fm.FontProperties(fname=FONT_PATH)
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False
else:
    font_prop = None

st.set_page_config(page_title="양주시 아카이브 GAMEBOY ADVANCE", layout="centered")

# 1. 게임보이 스타일 CSS
st.markdown("""
<style>
body, .stApp { background: #2f3042; }
.gba-outer {
    margin: 55px auto 0 auto;
    width: 950px; height: 500px;
    border-radius: 110px;
    background: #757cf7;
    box-shadow: 0 0 70px #131743;
    position: relative;
}
.gba-inner {
    position: absolute;
    left: 50%; top: 54%;
    transform: translate(-50%, -50%);
    width: 660px; height: 340px;
    border-radius: 44px;
    background: #10192e;
    box-shadow: 0 0 44px #32e2fd90, 0 0 0 #000;
    border: 7px solid #5cdefa;
    display: flex; align-items: center; justify-content: center;
}
.gba-screen-content {
    width: 97%; min-height: 220px; max-height: 290px; overflow-y: auto;
    color: #aef5ff;
    font-size: 19px;
    font-family: 'Press Start 2P', monospace, 'NanumGothicCoding', 'Malgun Gothic';
    line-height: 1.7em;
    text-align: left;
    padding: 20px 16px 20px 24px;
    margin: 0 auto;
    word-break: keep-all;
    white-space: pre-line;
}
.gba-btn {
    position: absolute;
    width: 60px; height: 35px;
    background: #42dbfa;
    border: 2.5px solid #fff;
    border-radius: 14px;
    font-family: 'Press Start 2P', monospace;
    color: #222; font-size: 23px;
    box-shadow: 0 4px 18px #0beaf455;
    cursor: pointer;
    z-index:2;
}
.gba-btn:active { background:#51e3ff; color:#d22; }
.gba-btn.left  { left: 65px;  top: 205px;}
.gba-btn.right { right: 65px; top: 205px;}
.gba-btn.start { left:50%; bottom:40px; transform:translateX(-50%);}
.gba-title {
    position: absolute; top: 32px; width: 100%;
    text-align: center; font-family: 'Press Start 2P', monospace;
    font-size: 2.3rem; color: #fff;
    text-shadow: 0 0 18px #72d9fd;
    letter-spacing: 2px;
}
.gba-footer {
    position: absolute; bottom: 22px; left: 0; width: 100%;
    text-align: center; font-family: 'Press Start 2P', monospace;
    color: #fff; font-size: 1.1rem;
    text-shadow: 0 0 9px #88e0fd;
    letter-spacing: 2px;
    opacity: 0.87;
}
</style>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# 2. 세션 상태
sections = ["📜 과거", "🏙️ 현재", "🌐 미래", "📊 인구 변화"]
if "section_idx" not in st.session_state: st.session_state.section_idx = 0
if "started" not in st.session_state: st.session_state.started = False

# 3. 시작 화면
def render_start_screen():
    st.markdown("""
    <div style="width:950px;height:500px;margin:60px auto 0 auto;position:relative;">
      <div class="gba-title">YANGJU ARCHIVE GAME</div>
      <div style="position:absolute;left:50%;top:52%;transform:translate(-50%,-50%);
        width:500px;height:180px;background:#10192e;border-radius:28px;border:5px solid #36deff;
        color:#aef5ff;font-family:'Press Start 2P',monospace;font-size:20px;line-height:1.7em;
        display:flex;align-items:center;justify-content:center;flex-direction:column;
        text-align:center;box-shadow:0 0 18px #36e6ff77;">
        <div style='margin-bottom:22px;'>
            <b>양주시 아카이브</b><br>
            경기도 양주시의 역사와 미래 비전을<br>
            <span style='color:#42e4ff;'>게임보이 어드밴스</span> 화면에서 구경하세요!
        </div>
        <span style="color:#fff;background:#111a2e;padding:8px 28px;border-radius:13px;">
            ⬇️ <b>START</b> 버튼을 누르세요!
        </span>
      </div>
      <button class="gba-btn start" onclick="window.location.reload();"
        style="font-size:20px;width:110px;left:50%;transform:translateX(-50%);bottom:38px;">START</button>
    </div>
    """, unsafe_allow_html=True)
    if st.button("START", key="start_btn", help="게임 시작!"):
        st.session_state.started = True
        st.experimental_rerun()
    st.stop()

# 4. 본문/탭 화면
def render_gba_ui():
    st.markdown('<div class="gba-outer">', unsafe_allow_html=True)
    # 타이틀
    st.markdown('<div class="gba-title">YANGJU ARCHIVE GAME</div>', unsafe_allow_html=True)
    # 게임기 화면
    st.markdown('<div class="gba-inner"><div class="gba-screen-content">', unsafe_allow_html=True)
    render_section_content()
    st.markdown('</div></div>', unsafe_allow_html=True)

    # 버튼 - 좌/우/스타트
    left, center, right = st.columns([1, 6, 1])
    with left:
        if st.button("⬅️", key="btn_left", help="이전", use_container_width=True):
            st.session_state.section_idx = (st.session_state.section_idx - 1) % len(sections)
            st.experimental_rerun()
    with center:
        if st.button("START", key="btn_start", help="처음으로"):
            st.session_state.started = False
            st.session_state.section_idx = 0
            st.experimental_rerun()
    with right:
        if st.button("➡️", key="btn_right", help="다음", use_container_width=True):
            st.session_state.section_idx = (st.session_state.section_idx + 1) % len(sections)
            st.experimental_rerun()

    # 하단
    st.markdown('<div class="gba-footer">GAMEBOY ADVANCE</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 5. 각 섹션
def render_section_content():
    idx = st.session_state.section_idx
    if idx == 0:
        st.markdown(f"""
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

    elif idx == 1:
        st.markdown(f"""
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

    elif idx == 2:
        st.markdown(f"""
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

    elif idx == 3:
        # 인구 변화 시각화
        st.markdown("**양주시 인구 구조 변화를 5년 단위로 시각화합니다.**<br>데이터 출처: KOSIS 국가통계포털", unsafe_allow_html=True)
        try:
            POP_DATA_PATH = "양주시_연도별_인구수.csv"
            df_pop = pd.read_csv(POP_DATA_PATH, encoding="cp949", header=[0,1])
            df_pop = df_pop[df_pop.iloc[:, 0].str.contains("양주시")].reset_index(drop=True)
            year_cols = {}
            for col in df_pop.columns[1:]:
                year = col[0][:4]
                if year not in year_cols: year_cols[year] = []
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
                ax.set_title("양주시 연평균 인구수 변화", fontproperties=font_prop, fontsize=13)
                ax.set_xlabel("연도", fontproperties=font_prop, fontsize=10)
                ax.set_ylabel("명", fontproperties=font_prop, fontsize=10)
                ax.set_xticklabels(years_5yr, fontproperties=font_prop, fontsize=9)
                plt.yticks(fontproperties=font_prop, fontsize=9)
                plt.xticks(fontproperties=font_prop, fontsize=9)
                ax.legend(prop=font_prop, fontsize=10)
            else:
                ax.set_title("양주시 연평균 인구수 변화", fontsize=13)
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

        # 출생/사망
        try:
            BIRTH_DEATH_DATA_PATH = "양주시_연도별_출생자수_사망자수.csv"
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

# 6. 실행
if not st.session_state.started:
    render_start_screen()
else:
    render_gba_ui()
