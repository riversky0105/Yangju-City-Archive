좋아!
LEVEL UP/XP/도감 문구와 "처음으로" 버튼 사이에 \*\*약간의 공백(16px)\*\*을 추가해서 시각적으로 조금 더 여유 있게 띄워줄게.

아래는 **전체 코드**야.
(`show_back_button()`에서 버튼 위에 `margin-bottom:16px;`을 추가)

---

```python
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import re
import numpy as np

# --------- 스타일/폰트 ---------
st.markdown("""
<style>
body, .stApp { background: #232946; }
.main-title {
    font-family: 'Press Start 2P', 'NanumGothicCoding', monospace;
    color: #a6e3e9;
    font-size: 2.8rem;
    text-shadow: 0 0 10px #00f2fe, 0 0 15px #232946;
    letter-spacing: 2px;
    padding: 20px;
    text-align: center;
    border-radius: 20px;
    margin-bottom: 10px;
    background: #232946ee;
    border: 4px solid #393e46;
    box-shadow: 0 0 15px #00f2fe80;
}
.arcade-frame {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(35, 41, 70, 0.92);
    border: 6px solid #00f2fe;
    border-radius: 32px;
    box-shadow: 0 0 40px #00f2fe44, 0 0 2px #232946;
    padding: 60px 48px 36px 48px;
    margin: 70px auto 40px auto;
    max-width: 540px;
    min-width: 330px;
    z-index: 2;
}
.arcade-frame .subtitle {
    font-family: 'Press Start 2P', monospace;
    color: #ffd6e0;
    font-size: 15pt;
    background: #232946f2;
    padding: 15px 24px 13px 24px;
    border-radius: 18px;
    margin-bottom: 36px;
    margin-top: 12px;
    text-align: center;
    box-shadow: 0 0 18px #00f2fe50;
    letter-spacing: 1px;
    border: 3px solid #393e46;
}
.blink {
    animation: blink 1.15s steps(1) infinite;
    font-family: 'Press Start 2P', monospace;
    color: #ffd6e0;
    font-size: 1.10rem;
    margin-bottom: 8px;
    margin-top: 18px;
    text-shadow: 0 0 8px #00f2fe;
}
@keyframes blink {
    0%, 55% { opacity: 1; }
    56%, 100% { opacity: 0.22; }
}
.pixel-stars {
    text-align: center;
    font-size: 1.3rem;
    color: #ffd6e0;
    letter-spacing: 9px;
    margin-top: 0px;
    margin-bottom: 13px;
    text-shadow: 0 0 8px #00f2fe70;
    font-family: 'Press Start 2P', monospace;
}
.pixel-border {
    border: 4px dashed #00f2fe;
    border-radius: 18px;
    padding: 24px 12px 6px 12px;
    margin-bottom: 18px;
    background: rgba(35,41,70,0.6);
    box-shadow: 0 0 18px #00f2fe30;
}
.game-item {
    display: inline-block;
    background: #a6e3e9;
    color: #232946;
    font-family: 'Press Start 2P', monospace;
    border-radius: 9px;
    padding: 3px 12px;
    margin: 3px 4px;
    font-size: 0.94rem;
    box-shadow: 0 0 9px #00f2fe55;
}
.back-btn {
    font-family: 'Press Start 2P', monospace;
    background: linear-gradient(90deg, #00f2fe 60%, #232946 100%);
    color: #232946;
    font-size: 1.09rem;
    border: 3px solid #393e46;
    border-radius: 18px;
    padding: 12px 0;
    margin-top: 12px;
    margin-bottom: 4px;
    width: 100%;
    box-shadow: 0 0 16px #00f2fe50;
}
@media (max-width: 600px) {
    .arcade-frame { padding: 13vw 3vw 6vw 3vw; min-width: 0; }
    .main-title { font-size: 1.6rem; }
    .pixel-border { padding: 6vw 1vw 2vw 1vw;}
    .back-btn { font-size: 0.95rem;}
}
</style>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# --------- 폰트(플롯용) ----------
FONT_PATH = os.path.join("fonts", "NanumGothicCoding.ttf")
if os.path.exists(FONT_PATH):
    font_prop = fm.FontProperties(fname=FONT_PATH)
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False
else:
    font_prop = None

st.set_page_config(page_title="양주시 아카이브 GAME", layout="wide")

# --------- 항상 상단에 타이틀 고정 ---------
st.markdown('<div class="main-title">양주시 아카이브 GAME</div>', unsafe_allow_html=True)

# --------- 세션 상태로 시작화면/본문 분기 ---------
if "archive_started" not in st.session_state:
    st.session_state.archive_started = False

def reset_to_start():
    st.session_state.archive_started = False
    st.session_state.current_tab = 0

# --------- [스타트 화면] ---------
if not st.session_state.archive_started:
    with st.container():
        st.markdown(
            """
            <div class="arcade-frame">
                <div class="pixel-stars">★&nbsp;◀&nbsp;WELCOME&nbsp;▶&nbsp;★</div>
                <div class="subtitle">
                    경기도 양주시의<br>역사와 미래 비전을<br>구경하세요!
                </div>
                <div class="blink">PRESS START</div>
            </div>
            """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2,3,2])
        with col2:
            if st.button("🎮 GAME START", key="gamestart", help="아카이브 시작!", use_container_width=True):
                st.session_state.archive_started = True
        st.stop()

# --------- [본문] ---------
tabs = st.tabs(["📜 과거", "🏙️ 현재", "🌐 미래", "📊 인구 변화"])

# 각 탭 하단에 "처음으로" 버튼
def show_back_button():
    # 버튼 위에 레벨업/도감 문구 + 간격 추가
    st.markdown(
        """
        <div style="text-align:center; margin-top:26px; margin-bottom:16px;">
            <span class="game-item">LEVEL UP!</span>
            <span class="game-item">+50 XP</span>
            <span class="game-item">🗂️ 아카이브 도감 달성!</span>
        </div>
        """, unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns([2,3,2])
    with col2:
        if st.button("⏪ 처음으로", key=f"backtohome_{st.session_state.get('current_tab',0)}", help="아카이브 시작화면으로", use_container_width=True):
            reset_to_start()

with tabs[0]:
    st.session_state.current_tab = 0
    st.markdown('<div class="pixel-border">', unsafe_allow_html=True)
    st.header("📜 양주시의 과거")
    st.markdown("""
    <div style='font-size:14pt; color:#fff;'>
    <b>1. 고려~조선 시대, 북방의 행정·군사 중심지</b><br>
    - 양주목 설치: 경기 북부 광역 행정 단위<br>
    - 조선시대 서울 외곽 방어선 역할<br>
    - 현재의 의정부, 동두천, 포천, 남양주 일대가 관할 지역<br>
    </div>
    """, unsafe_allow_html=True)
    st.image("양주 관야지.jpg", caption="양주 관아지(양주목 관아터)", width=700)
    st.markdown("""
    <div style='font-size:14pt; color:#fff;'>
    <b>2. 회암사: 왕실의 불교 수행처</b><br>
    - 태조 이성계 퇴위 후 회암사 중건<br>
    - 세종 시대까지 국가 불교 중심지로 기능<br>
    - 승과(僧科) 시행 장소<br>
    - 현재는 회암사지 및 국립 회암사지박물관으로 보존
    </div>
    """, unsafe_allow_html=True)
    st.image("회암사지.jpg", caption="회암사지 터", width=700)
    st.image("회암사지 복원도.jpg", caption="회암사지 추정 복원도", width=700)
    st.markdown("""
    <div style='font-size:14pt; color:#fff;'>
    <b>3. 조선 후기 천주교 박해의 현장</b><br>
    - 신유박해(1801) 시기 여성 신자 다수 순교<br>
    - 강완숙, 이순이 등 순교자 기록<br>
    - 장흥면에 순교 기념비, 성지 조성<br>
    </div>
    """, unsafe_allow_html=True)
    st.image("양주 장흥 순교성지.jpg", caption="양주 장흥 순교성지", width=700)
    st.markdown("""
    <div style='font-size:14pt; color:#fff;'>
    <b>4. 농업과 장터</b><br>
    - 장흥, 은현, 남면은 조선시대 곡창지대<br>
    - 읍내 장터는 한양 상인과의 활발한 교역지
    </div>
    """, unsafe_allow_html=True)
    st.image("양주 농촌.jpg", caption="1950~1980년대 논 모내기 풍경(경기북부, 양주 일대)", width=700)
    st.image("양주 장터.jpg", caption="1970~1980년대 시골 장터(경기북부, 양주 일대)", width=700)
    st.markdown("""
    <div style='font-size:14pt; color:#fff;'>
    <b>5. 한국전쟁과 양주</b><br>
    - 1·4 후퇴 시 주요 격전지<br>
    - 1951년 대규모 민간인 피해<br>
    - 전쟁 후 장기 복구 과정<br>
    </div>
    """, unsafe_allow_html=True)
    st.image("양주 1.4후퇴.jpg", caption="1951년 1.4후퇴 당시 경기북부(양주 일대) 피난민 행렬", width=700)
    show_back_button()
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[1]:
    st.session_state.current_tab = 1
    st.markdown('<div class="pixel-border">', unsafe_allow_html=True)
    st.header("🏙️ 양주시의 현재")
    st.markdown("""
    <div style='font-size:14pt; color:#fff;'>
    <b>1. 인구와 행정</b><br>
    - 2025년 인구 약 29만 명, 면적 310.4㎢, 1읍 4면 7동.<br>
    - 초중고대학 67교, 약 2,800여 개의 공장 및 산업시설이 위치.<br>
    </div>
    """, unsafe_allow_html=True)
    st.image("양주시 면적.jpg", caption="양주시 행정구역도", width=700)
    st.markdown("""
    <div style='font-size:14pt; color:#fff;'>
    <b>2. 신도시 개발 및 교통</b><br>
    - 옥정·회천 신도시 개발로 수도권 내 인구 급증(최근 수도권 증가율 1위).<br>
    - 7호선 연장, GTX-C 개통 등 서울 접근성 좋은 광역교통망 빠르게 확장.<br>
    </div>
    """, unsafe_allow_html=True)
    st.image("양주 옥정신도시.jpg", caption="양주 옥정 신도시 전경", width=700)
    st.markdown("""
    <div style='font-size:14pt; color:#fff;'>
    <b>3. 산업기반 확충</b><br>
    - 양주테크노밸리, 첨단산업단지 개발<br>
    - 의료·바이오·IT 기업 유치 및 고용 창출, 세수 확대<br>
    </div>
    """, unsafe_allow_html=True)
    st.image("양주 산업단지.jpg", caption="양주 은남일반산업단지(조감도)", width=700)
    st.markdown("""
    <div style='font-size:14pt; color:#fff;'>
    <b>4. 문화·관광 자원 리브랜딩</b><br>
    - 장흥 조각공원, 송암천문대, 나리농원, 회암사지 등 관광자원 리브랜딩<br>
    - 전통+현대예술 융합, 청년예술가 지원<br>
    </div>
    """, unsafe_allow_html=True)
    st.image("양주시 나리농원 천일홍 축제.jpg", caption="양주시 나리농원 천일홍 축제", width=700)
    st.markdown("""
    <div style='font-size:14pt; color:#fff;'>
    <b>5. 삶의 질을 높이는 복지와 생활환경</b><br>
    - 광역 복지관, 문화센터, 체육시설 등 생활 인프라 대폭 확충<br>
    - 청년·고령자·다문화가정 등 맞춤 복지 정책 강화<br>
    - 쾌적한 공원, 녹지, 생활체육 환경 조성
    </div>
    """, unsafe_allow_html=True)
    st.image("양주 옥정 호수공원.jpg", caption="양주 옥정 호수공원", width=700)
    show_back_button()
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[2]:
    st.session_state.current_tab = 2
    st.markdown('<div class="pixel-border">', unsafe_allow_html=True)
    st.header("🌐 양주시의 미래")
    st.markdown("""
    <div style='font-size:14pt; color:#fff;'>
    <b>1. 경기북부 중심도시 성장</b><br>
    - 수도권 동북부 거점도시로 발전<br>
    - 주거 중심에서 산업·문화·교육 복합도시로 전환<br>
    - 광역교통망 중심축으로 기대<br>
    </div>
    """, unsafe_allow_html=True)
    st.image("양주 GTX 노선도.jpg", caption="양주를 지나는 GTX-C(예정) 노선", width=700)
    st.markdown("""
    <div style='font-size:14pt; color:#fff;'>
    <b>2. 첨단산업과 창업도시</b><br>
    - 테크노밸리, 산업단지 중심 개발<br>
    - 청년 창업 및 스타트업 인큐베이팅<br>
    - 4차 산업 기반의 경제 체질 개선<br>
    </div>
    """, unsafe_allow_html=True)
    st.image("양주 테크노벨리.png", caption="양주 테크노밸리(조감도)", width=700)
    st.markdown("""
    <div style='font-size:14pt; color:#fff;'>
    <b>3. 문화예술 중심도시</b><br>
    - 장흥문화예술촌 레지던시 확대<br>
    - 청년 예술가 정착 유도<br>
    - 회암사지 등 역사와 콘텐츠 결합한 스토리텔링<br>
    </div>
    """, unsafe_allow_html=True)
    st.image("양주 문화 예술.jpg", caption="양주 장흥문화예술촌(실내/전시)", width=700)
    st.markdown("""
    <div style='font-size:14pt; color:#fff;'>
    <b>4. 탄소중립 스마트시티</b><br>
    - 스마트 교통, AI 행정 도입<br>
    - 공공건물 태양광 등 에너지 절감 도시계획<br>
    - 생태공원, 도시숲, 스마트팜 확장<br>
    </div>
    """, unsafe_allow_html=True)
    st.image("양주 탄소중립 스마트시티.jpg", caption="양주 생태공원 및 친환경 스마트시티", width=700)
    st.markdown("""
    <div style='font-size:14pt; color:#fff;'>
    <b>5. 교육·복지 인프라</b><br>
    - 국공립 유치원 및 학교 확충<br>
    - 지역 대학 및 평생학습 거점 마련<br>
    - 맞춤형 복지 설계: 고령자, 청년, 다문화 가정 대상
```


```
</div>
""", unsafe_allow_html=True)
st.image("양주시 청년센터.jpg", caption="양주시 청년센터(옥정동)", width=700)
show_back_button()
st.markdown('</div>', unsafe_allow_html=True)
```

with tabs\[3]:
st.session\_state.current\_tab = 3
st.markdown('<div class="pixel-border">', unsafe\_allow\_html=True)
st.header("📊 양주시 인구 변화")
st.markdown(""" <span style='color:#fff;'>양주시 인구 구조 변화를 월별/연도별 및 5년 단위 출생자수·사망자수와 함께 시각화합니다. 데이터 출처: KOSIS 국가통계포털</span>
""", unsafe\_allow\_html=True)
\# --------- 인구수 변화 그래프 ---------
POP\_DATA\_PATH = "양주시\_연도별\_인구수.csv"
try:
df\_pop = pd.read\_csv(POP\_DATA\_PATH, encoding="cp949", header=\[0,1])
df\_pop = df\_pop\[df\_pop.iloc\[:, 0].str.contains("양주시")].reset\_index(drop=True)
year\_cols = {}
for col in df\_pop.columns\[1:]:
year = col\[0]\[:4]
if year not in year\_cols:
year\_cols\[year] = \[]
year\_cols\[year].append(col)
year\_avg = {}
for y, cols in year\_cols.items():
vals = df\_pop.loc\[0, cols].values.astype(float)
year\_avg\[int(y)] = np.mean(vals)
years = sorted(year\_avg.keys())
years\_5yr = \[y for y in years if y >= 2005 and (y % 5 == 0 or y == years\[-1])]
pop\_5yr\_avg = \[year\_avg\[y] for y in years\_5yr]
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.plot(years\_5yr, pop\_5yr\_avg, marker='o', color='tab\:green', label='인구수 (연평균)')
ax.set\_xticks(years\_5yr)
if font\_prop:
ax.set\_title("양주시 연평균 인구수 변화", fontproperties=font\_prop, fontsize=12)
ax.set\_xlabel("연도", fontproperties=font\_prop, fontsize=10)
ax.set\_ylabel("명", fontproperties=font\_prop, fontsize=10)
ax.set\_xticklabels(\[str(x) for x in years\_5yr], fontproperties=font\_prop, fontsize=9)
plt.yticks(fontproperties=font\_prop, fontsize=9)
plt.xticks(fontproperties=font\_prop, fontsize=9)
ax.legend(prop=font\_prop, fontsize=10)
else:
ax.set\_title("양주시 연평균 인구수 변화", fontsize=12)
ax.set\_xlabel("연도", fontsize=10)
ax.set\_ylabel("명", fontsize=10)
ax.set\_xticklabels(\[str(x) for x in years\_5yr], fontsize=9)
plt.yticks(fontsize=9)
plt.xticks(fontsize=9)
ax.legend(fontsize=10)
plt.tight\_layout()
st.pyplot(fig, use\_container\_width=False)
except Exception as e:
st.error(f"인구수 그래프 로드 중 오류가 발생했습니다: {e}")

```
st.markdown("---")

# --------- 출생자수·사망자수 그래프 ---------
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
    ax.set_xticks(common_years)
    if font_prop:
        ax.set_title("양주시 출생자수·사망자수 변화", fontproperties=font_prop, fontsize=12)
        ax.set_xlabel("연도", fontproperties=font_prop, fontsize=10)
        ax.set_ylabel("명", fontproperties=font_prop, fontsize=10)
        ax.set_xticklabels([str(x) for x in common_years], fontproperties=font_prop, fontsize=9)
        plt.yticks(fontproperties=font_prop, fontsize=9)
        plt.xticks(fontproperties=font_prop, fontsize=9)
        ax.legend(prop=font_prop, fontsize=10)
    else:
        ax.set_title("양주시 출생자수·사망자수 변화", fontsize=12)
        ax.set_xlabel("연도", fontsize=10)
        ax.set_ylabel("명", fontsize=10)
        ax.set_xticklabels([str(x) for x in common_years], fontsize=9)
        plt.yticks(fontsize=9)
        plt.xticks(fontsize=9)
        ax.legend(fontsize=10)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)
    st.caption("양주시 인구 구조 변화를 5년 단위로 시각화. 데이터 출처: KOSIS 국가통계포털")
except Exception as e:
    st.error(f"출생자수·사망자수 그래프 로드 중 오류가 발생했습니다: {e}")

show_back_button()
st.markdown('</div>', unsafe_allow_html=True)
```

```

---

### 포인트
- **margin-bottom:16px;**로 LEVEL UP UI와 버튼 사이 공백 추가!
- 나머지 동작과 UI는 모두 이전과 동일!

마음에 안 드는 간격이면 숫자만 조정하면 돼(예: 8px, 20px 등).  
추가 요청 언제든 환영!
```
