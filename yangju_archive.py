import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import re
import numpy as np

# --------- Arcade 스타일 CSS ---------
st.markdown("""
<style>
body, .stApp { background: #141a22 !important; }
.arcade-cabinet {
    width: 930px;
    margin: 38px auto 24px auto;
    border-radius: 48px 48px 68px 68px;
    background: linear-gradient(180deg, #232946 80%, #151921 100%);
    box-shadow: 0 0 80px #00f2fe88, 0 10px 60px #111;
    padding: 0 0 56px 0;
    border: 9px solid #0dfcff;
    position: relative;
    overflow: visible;
}
.arcade-top {
    width: 100%;
    height: 92px;
    background: linear-gradient(90deg, #00f2fe 10%, #42e1e1 60%, #00f2fe 100%);
    border-radius: 40px 40px 16px 16px;
    text-align: center;
    padding: 24px 0 10px 0;
    font-family: 'Press Start 2P', monospace;
    font-size: 2.6rem;
    letter-spacing: 8px;
    color: #232946;
    text-shadow: 0 0 24px #fff, 0 0 20px #00f2fe;
    border-bottom: 5px solid #17181c;
    margin-bottom: -13px;
    box-shadow: 0 0 32px #00f2fe44;
}
.arcade-screen {
    margin: 0 auto;
    width: 860px;
    min-height: 740px;
    border-radius: 28px;
    background: linear-gradient(180deg,#151a24 85%,#232946 100%);
    box-shadow: 0 0 48px #00f2fe88, 0 0 44px #232946cc;
    border: 8px solid #0dfcff;
    padding: 34px 40px 38px 40px;
    position: relative;
    z-index: 2;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
}
.arcade-buttons {
    display: flex;
    justify-content: center;
    gap: 44px;
    margin-top: 38px;
    margin-bottom: -32px;
}
.arcade-btn {
    width: 62px;
    height: 62px;
    border-radius: 50%;
    background: radial-gradient(circle at 33% 33%, #ff5f7f 70%, #b01532 100%);
    box-shadow: 0 0 22px #ff6f91cc, 0 4px 9px #222;
    border: 5px solid #800910;
    display: inline-block;
}
.arcade-btn.blue {
    background: radial-gradient(circle at 33% 33%, #5fd8ff 70%, #156680 100%);
    box-shadow: 0 0 22px #50e6ffcc, 0 4px 9px #222;
    border: 5px solid #0973a6;
}
.arcade-btn.yellow {
    background: radial-gradient(circle at 33% 33%, #ffe95f 70%, #948012 100%);
    box-shadow: 0 0 20px #fffa6fcc, 0 4px 9px #222;
    border: 5px solid #807109;
}
.stTabs [role="tab"] {
    font-family: 'Press Start 2P', monospace;
    font-size: 1.16rem;
    background: #181d29;
    color: #fff;
    border: 2px solid #0dfcff;
    border-radius: 14px 14px 0 0;
    margin-right: 4px;
    padding: 12px 30px 12px 30px;
    box-shadow: 0 0 5px #00f2fe44;
    transition: background 0.18s, color 0.18s;
}
.stTabs [role="tab"][aria-selected="true"] {
    background: #202c39;
    color: #ff77b0;
    border-bottom: 5px solid #0dfcff;
    text-shadow: 0 0 10px #00f2fe80;
}
.pixel-border {
    border: 5px solid #232946;
    border-radius: 20px;
    background: #232946ee;
    box-shadow: 0 0 20px #00f2fe99;
    padding: 20px 38px 25px 38px;
    margin-bottom: 34px;
    max-width: 740px;
    margin-left: auto;
    margin-right: auto;
}
[data-testid="stImage"] img {
    border-radius: 15px;
    box-shadow: 0 0 18px #00f2fe33;
    margin-bottom: 7px;
    max-width: 730px;
}
.arcade-caption {
    color: #aaa;
    text-align: center;
    font-family: 'NanumGothicCoding', monospace;
    margin-top: 5px;
    margin-bottom: 15px;
    font-size: 13.5pt;
}
</style>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# --------- 폰트 세팅(그래프용) ---------
FONT_PATH = os.path.join("fonts", "NanumGothicCoding.ttf")
if os.path.exists(FONT_PATH):
    font_prop = fm.FontProperties(fname=FONT_PATH)
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False
else:
    font_prop = None

# --------- PAGE 설정 ---------
st.set_page_config(page_title="양주시 아카이브 GAME", layout="wide")

# --------- Arcade 프레임 시작 ---------
st.markdown('<div class="arcade-cabinet">', unsafe_allow_html=True)
st.markdown('<div class="arcade-top">양주시 아카이브</div>', unsafe_allow_html=True)
st.markdown('<div class="arcade-screen">', unsafe_allow_html=True)

# =============== 컨텐츠는 arcade-screen 내부 st.container로 래핑! ==============
with st.container():
    tabs = st.tabs(["📜 과거", "🏙️ 현재", "🌐 미래", "📊 인구 변화"])

    with tabs[0]:
        st.markdown('<div class="pixel-border">', unsafe_allow_html=True)
        st.header("📜 양주시의 과거")
        st.markdown("""
        <div style='font-size:15pt; color:#fff; font-family: NanumGothicCoding, monospace;'>
        <b>1. 고려~조선 시대, 북방의 행정·군사 중심지</b><br>
        - 양주목 설치: 경기 북부 광역 행정 단위<br>
        - 조선시대 서울 외곽 방어선 역할<br>
        - 현재의 의정부, 동두천, 포천, 남양주 일대가 관할 지역<br>
        </div>
        """, unsafe_allow_html=True)
        st.image("양주 관야지.jpg", caption="양주 관아지(양주목 관아터)", width=730)
        st.markdown("""
        <div style='font-size:15pt; color:#fff; font-family: NanumGothicCoding, monospace; margin-top:15px;'>
        <b>2. 회암사: 왕실의 불교 수행처</b><br>
        - 태조 이성계 퇴위 후 회암사 중건<br>
        - 세종 시대까지 국가 불교 중심지로 기능<br>
        - 승과(僧科) 시행 장소<br>
        - 현재는 회암사지 및 국립 회암사지박물관으로 보존
        </div>
        """, unsafe_allow_html=True)
        st.image("회암사지.jpg", caption="회암사지 터", width=730)
        st.image("회암사지 복원도.jpg", caption="회암사지 추정 복원도", width=730)
        st.markdown("""
        <div style='font-size:15pt; color:#fff; font-family: NanumGothicCoding, monospace; margin-top:15px;'>
        <b>3. 조선 후기 천주교 박해의 현장</b><br>
        - 신유박해(1801) 시기 여성 신자 다수 순교<br>
        - 강완숙, 이순이 등 순교자 기록<br>
        - 장흥면에 순교 기념비, 성지 조성<br>
        </div>
        """, unsafe_allow_html=True)
        st.image("양주 장흥 순교성지.jpg", caption="양주 장흥 순교성지", width=730)
        st.markdown("""
        <div style='font-size:15pt; color:#fff; font-family: NanumGothicCoding, monospace; margin-top:15px;'>
        <b>4. 농업과 장터</b><br>
        - 장흥, 은현, 남면은 조선시대 곡창지대<br>
        - 읍내 장터는 한양 상인과의 활발한 교역지
        </div>
        """, unsafe_allow_html=True)
        st.image("양주 농촌.jpg", caption="1950~1980년대 논 모내기 풍경(경기북부, 양주 일대)", width=730)
        st.image("양주 장터.jpg", caption="1970~1980년대 시골 장터(경기북부, 양주 일대)", width=730)
        st.markdown("""
        <div style='font-size:15pt; color:#fff; font-family: NanumGothicCoding, monospace; margin-top:15px;'>
        <b>5. 한국전쟁과 양주</b><br>
        - 1·4 후퇴 시 주요 격전지<br>
        - 1951년 대규모 민간인 피해<br>
        - 전쟁 후 장기 복구 과정<br>
        </div>
        """, unsafe_allow_html=True)
        st.image("양주 1.4후퇴.jpg", caption="1951년 1.4후퇴 당시 경기북부(양주 일대) 피난민 행렬", width=730)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[1]:
        st.markdown('<div class="pixel-border">', unsafe_allow_html=True)
        st.header("🏙️ 양주시의 현재")
        st.markdown("""
        <div style='font-size:15pt; color:#fff; font-family: NanumGothicCoding, monospace;'>
        <b>1. 인구와 행정</b><br>
        - 2025년 인구 약 29만 명, 면적 310.4㎢, 1읍 4면 7동.<br>
        - 초중고대학 67교, 약 2,800여 개의 공장 및 산업시설이 위치.<br>
        </div>
        """, unsafe_allow_html=True)
        st.image("양주시 면적.jpg", caption="양주시 행정구역도", width=730)
        st.markdown("""
        <div style='font-size:15pt; color:#fff; font-family: NanumGothicCoding, monospace; margin-top:15px;'>
        <b>2. 신도시 개발 및 교통</b><br>
        - 옥정·회천 신도시 개발로 수도권 내 인구 급증(최근 수도권 증가율 1위).<br>
        - 7호선 연장, GTX-C 개통 등 서울 접근성 좋은 광역교통망 빠르게 확장.<br>
        </div>
        """, unsafe_allow_html=True)
        st.image("양주 옥정신도시.jpg", caption="양주 옥정 신도시 전경", width=730)
        st.markdown("""
        <div style='font-size:15pt; color:#fff; font-family: NanumGothicCoding, monospace; margin-top:15px;'>
        <b>3. 산업기반 확충</b><br>
        - 양주테크노밸리, 첨단산업단지 개발<br>
        - 의료·바이오·IT 기업 유치 및 고용 창출, 세수 확대<br>
        </div>
        """, unsafe_allow_html=True)
        st.image("양주 산업단지.jpg", caption="양주 은남일반산업단지(조감도)", width=730)
        st.markdown("""
        <div style='font-size:15pt; color:#fff; font-family: NanumGothicCoding, monospace; margin-top:15px;'>
        <b>4. 문화·관광 자원 리브랜딩</b><br>
        - 장흥 조각공원, 송암천문대, 나리농원, 회암사지 등 관광자원 리브랜딩<br>
        - 전통+현대예술 융합, 청년예술가 지원<br>
        </div>
        """, unsafe_allow_html=True)
        st.image("양주시 나리농원 천일홍 축제.jpg", caption="양주시 나리농원 천일홍 축제", width=730)
        st.markdown("""
        <div style='font-size:15pt; color:#fff; font-family: NanumGothicCoding, monospace; margin-top:15px;'>
        <b>5. 삶의 질을 높이는 복지와 생활환경</b><br>
        - 광역 복지관, 문화센터, 체육시설 등 생활 인프라 대폭 확충<br>
        - 청년·고령자·다문화가정 등 맞춤 복지 정책 강화<br>
        - 쾌적한 공원, 녹지, 생활체육 환경 조성
        </div>
        """, unsafe_allow_html=True)
        st.image("양주 옥정 호수공원.jpg", caption="양주 옥정 호수공원", width=730)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[2]:
        st.markdown('<div class="pixel-border">', unsafe_allow_html=True)
        st.header("🌐 양주시의 미래")
        st.markdown("""
        <div style='font-size:15pt; color:#fff; font-family: NanumGothicCoding, monospace;'>
        <b>1. 경기북부 중심도시 성장</b><br>
        - 수도권 동북부 거점도시로 발전<br>
        - 주거 중심에서 산업·문화·교육 복합도시로 전환<br>
        - 광역교통망 중심축으로 기대<br>
        </div>
        """, unsafe_allow_html=True)
        st.image("양주 GTX 노선도.jpg", caption="양주를 지나는 GTX-C(예정) 노선", width=730)
        st.markdown("""
        <div style='font-size:15pt; color:#fff; font-family: NanumGothicCoding, monospace; margin-top:15px;'>
        <b>2. 첨단산업과 창업도시</b><br>
        - 테크노밸리, 산업단지 중심 개발<br>
        - 청년 창업 및 스타트업 인큐베이팅<br>
        - 4차 산업 기반의 경제 체질 개선<br>
        </div>
        """, unsafe_allow_html=True)
        st.image("양주 테크노벨리.png", caption="양주 테크노밸리(조감도)", width=730)
        st.markdown("""
        <div style='font-size:15pt; color:#fff; font-family: NanumGothicCoding, monospace; margin-top:15px;'>
        <b>3. 문화예술 중심도시</b><br>
        - 장흥문화예술촌 레지던시 확대<br>
        - 청년 예술가 정착 유도<br>
        - 회암사지 등 역사와 콘텐츠 결합한 스토리텔링<br>
        </div>
        """, unsafe_allow_html=True)
        st.image("양주 문화 예술.jpg", caption="양주 장흥문화예술촌(실내/전시)", width=730)
        st.markdown("""
        <div style='font-size:15pt; color:#fff; font-family: NanumGothicCoding, monospace; margin-top:15px;'>
        <b>4. 탄소중립 스마트시티</b><br>
        - 스마트 교통, AI 행정 도입<br>
        - 공공건물 태양광 등 에너지 절감 도시계획<br>
        - 생태공원, 도시숲, 스마트팜 확장<br>
        </div>
        """, unsafe_allow_html=True)
        st.image("양주 탄소중립 스마트시티.jpg", caption="양주 생태공원 및 친환경 스마트시티", width=730)
        st.markdown("""
        <div style='font-size:15pt; color:#fff; font-family: NanumGothicCoding, monospace; margin-top:15px;'>
        <b>5. 교육·복지 인프라</b><br>
        - 국공립 유치원 및 학교 확충<br>
        - 지역 대학 및 평생학습 거점 마련<br>
        - 맞춤형 복지 설계: 고령자, 청년, 다문화 가정 대상
        </div>
        """, unsafe_allow_html=True)
        st.image("양주시 청년센터.jpg", caption="양주시 청년센터(옥정동)", width=730)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[3]:
        st.markdown('<div class="pixel-border">', unsafe_allow_html=True)
        st.header("📊 양주시 인구 변화")
        st.markdown("""
        <div style='font-size:17pt; color:#ff77b0; font-family: Press Start 2P, monospace; margin-bottom: 14px;'>
        양주시 인구 변화
        </div>
        <div style='color:#fff; font-size:14.3pt; font-family: NanumGothicCoding, monospace; margin-bottom:7px;'>
        양주시 인구 구조 변화를 월별/연도별 및 5년 단위 출생자수·사망자수와 함께 시각화합니다. <b>데이터 출처: KOSIS 국가통계포털</b>
        </div>
        """, unsafe_allow_html=True)
        # 인구 변화 그래프 코드 ... (생략없이 기존 그래프코드 그대로!)
        # 위에서 제공한 전체 코드 참고해서 인구 변화, 출생자/사망자수 그래프 코드를 넣어줘!
        st.markdown('</div>', unsafe_allow_html=True)

# ============== arcade-screen 닫기 ==============
st.markdown('</div>', unsafe_allow_html=True)

# --------- 하단 Arcade 버튼 장식 ---------
st.markdown("""
<div class="arcade-buttons">
    <div class="arcade-btn"></div>
    <div class="arcade-btn blue"></div>
    <div class="arcade-btn yellow"></div>
    <div class="arcade-btn"></div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)  # arcade-cabinet 끝
