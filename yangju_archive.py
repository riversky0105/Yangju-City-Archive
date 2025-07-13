import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import re
import numpy as np
from streamlit_keyup import keyup   # ★ 핵심: 키입력용 컴포넌트 임포트

# ===== 1. 게임기 스타일 CSS+픽셀폰트 =====
st.markdown("""
<style>
body, .stApp { background: #232946; }
.main-title {
    font-family: 'Press Start 2P', 'NanumGothicCoding', monospace;
    color: #a6e3e9;
    font-size: 2.7rem;
    text-shadow: 0 0 10px #00f2fe, 0 0 15px #232946;
    letter-spacing: 2px;
    padding: 18px;
    text-align: center;
    border-radius: 18px;
    margin-bottom: 12px;
    background: #232946ee;
    border: 4px solid #393e46;
    box-shadow: 0 0 15px #00f2fe80;
}
.pixel-box {
    border: 5px solid #393e46;
    border-radius: 18px;
    background: #232946ee;
    box-shadow: 0 0 17px #00f2fe77;
    padding: 18px 30px 22px 30px;
    margin-bottom: 20px;
}
.section-label {
    font-family: 'Press Start 2P', monospace;
    font-size: 1.2rem;
    color: #e0fcff;
    text-align: center;
    margin-bottom: 16px;
    letter-spacing: 1.5px;
    text-shadow: 0 0 10px #00f2fe90;
}
.wasd-tip {
    font-family: 'Press Start 2P', monospace;
    color: #fdadad;
    text-align: center;
    font-size: 1.04rem;
    margin: 0 0 9px 0;
}
.game-start-btn {
    font-family: 'Press Start 2P', monospace;
    font-size: 1.45rem;
    background: #f44336;
    color: #fff;
    border-radius: 15px;
    border: 3px solid #232946;
    box-shadow: 0 0 8px #ffadad;
    margin: 24px 0 30px 0;
    padding: 17px 44px;
    transition: background 0.17s;
}
.game-start-btn:hover { background: #232946; color: #fdadad; border: 3px solid #f44336; }
.arrow-btn {
    font-family: 'Press Start 2P', monospace;
    background: #222a41;
    color: #e0fcff;
    font-size: 2.1rem !important;
    border-radius: 18px;
    border: 3px solid #00f2fe;
    margin: 7px 20px 7px 20px;
    padding: 9px 26px 9px 26px;
    box-shadow: 0 0 11px #00f2fe99;
    transition: background 0.13s;
}
.arrow-btn:hover { background: #181c2b; color:#fdadad; border-color:#fdadad; }
</style>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ===== 2. 한글 플롯 폰트 =====
FONT_PATH = os.path.join("fonts", "NanumGothicCoding.ttf")
if os.path.exists(FONT_PATH):
    font_prop = fm.FontProperties(fname=FONT_PATH)
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False
else:
    font_prop = None

st.set_page_config(page_title="양주시 아카이브 GAME", layout="wide")

# ===== 3. 섹션/페이지 상태 =====
sections = [
    "📜 과거", "🏙️ 현재", "🌐 미래", "📊 인구 변화"
]
if "section_idx" not in st.session_state:
    st.session_state["section_idx"] = 0
if "started" not in st.session_state:
    st.session_state["started"] = False

# ===== 4. 아카이브 타이틀(게임 시작) 화면 =====
if not st.session_state["started"]:
    st.markdown('<div class="main-title">양주시 아카이브 GAME</div>', unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align:center;'><span style='font-family: Press Start 2P, monospace; font-size:15pt; color:#fff; background:#232946cc; padding:7px 18px; border-radius:12px;'>경기도 양주시의 역사와 미래 비전을 게임처럼 구경하세요!</span></div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div style='text-align:center;padding-top:10px;padding-bottom:3px;'>"
        "<img src='https://cdn-icons-png.flaticon.com/128/2736/2736127.png' height='80' style='margin-right:13px;filter:drop-shadow(0 0 7px #00f2fe77);'><img src='https://cdn-icons-png.flaticon.com/128/1404/1404945.png' height='80' style='filter:drop-shadow(0 0 7px #00f2fe77);'>"
        "</div>", unsafe_allow_html=True
    )
    st.markdown("<div class='wasd-tip'>⬅️➡️ 화살표나 W/A/S/D 키로 탭을 이동할 수 있습니다!<br>GAME START를 클릭하세요!</div>", unsafe_allow_html=True)
    if st.button("🎮 GAME START", key="gamestart1", help="아카이브 시작!", type="primary"):
        st.session_state["started"] = True
        st.session_state["section_idx"] = 0
        st.rerun()
    st.stop()

# 🚩 WASD/화살표 입력 지원 (streamlit-keyup 사용)
key = keyup("", debounce=0, key="keyinput", auto_focus=True, placeholder="")
if key and isinstance(key, str):
    if key.lower() in ["arrowright", "d"]:
        st.session_state.section_idx = (st.session_state.section_idx + 1) % len(sections)
        st.rerun()
    elif key.lower() in ["arrowleft", "a"]:
        st.session_state.section_idx = (st.session_state.section_idx - 1) % len(sections)
        st.rerun()

# ===== 5. 게임패드 네비게이션 (⬅️/➡️ 버튼) =====
st.markdown(f"<div class='section-label'>🕹️ {sections[st.session_state.section_idx]}</div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,6,1])
with col1:
    if st.button("⬅️", key="left_btn", help="이전", use_container_width=True):
        st.session_state.section_idx = (st.session_state.section_idx - 1) % len(sections)
        st.rerun()
with col3:
    if st.button("➡️", key="right_btn", help="다음", use_container_width=True):
        st.session_state.section_idx = (st.session_state.section_idx + 1) % len(sections)
        st.rerun()
st.markdown(
    "<div style='text-align:center;margin-bottom:18px;'><span style='background:#181c2b;border-radius:10px;padding:5px 14px 5px 10px;box-shadow:0 0 9px #00f2fe55;letter-spacing:1.5px;'><b style='color:#00f2fe;'>⬅️ ➡️</b> 또는 <b style='color:#fdadad;'>W/A/S/D</b>로 이동!</span></div>",
    unsafe_allow_html=True
)

# ===== 6. 각 섹션별 콘텐츠 (이전 답변 전체 붙이면 됨) =====
# ... 아래는 예시로 한 섹션만 첨부, 실제론 이전 답변의 전체 섹션을 모두 붙여야 완성!
if st.session_state.section_idx == 0:
    st.markdown('<div class="pixel-box">', unsafe_allow_html=True)
    st.header("📜 양주시의 과거")
    st.markdown("""
    <div style='font-size:14pt; color:#fff;'>
    <b>1. 고려~조선 시대, 북방의 행정·군사 중심지</b><br>
    - 양주목 설치: 경기 북부 광역 행정 단위<br>
    - 조선시대 서울 외곽 방어선 역할<br>
    - 현재의 의정부, 동두천, 포천, 남양주 일대가 관할 지역<br>
    </div>
    """, unsafe_allow_html=True)
    # (이하 생략, 전체 코드는 위 답변 참조해서 모두 붙이면 됩니다!)
