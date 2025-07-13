import streamlit as st

# 페이지 설정
st.set_page_config(page_title="양주시 아카이브 - Gameboy Advance 스타일", layout="centered")

# CSS로 도형 UI
st.markdown("""
<style>
.gba-body {
    width: 600px;
    height: 290px;
    margin: 40px auto 0 auto;
    background: #565cbf;
    border-radius: 80px 80px 90px 90px / 100px 100px 70px 70px;
    box-shadow: 0 12px 60px #23294666, 0 1px 0 #fff inset;
    position: relative;
    border: 8px solid #d0d7f7;
}
.gba-screen {
    position: absolute;
    left: 115px; top: 45px;
    width: 370px; height: 180px;
    background: #131926;
    border-radius: 23px;
    border: 5px solid #222c42;
    box-shadow: 0 0 22px #00f2fe66 inset;
    text-align: left;
    padding: 22px 18px 13px 18px;
    color: #bff6fa;
    font-family: 'Press Start 2P', monospace;
    font-size: 13px;
    overflow-y: auto;
    z-index: 10;
}
.gba-title {
    position: absolute;
    left: 154px; top: 14px;
    font-family: 'Press Start 2P', monospace;
    color: #e8fffe;
    font-size: 1.15rem;
    letter-spacing: 2px;
    text-shadow: 0 0 8px #1de5fe, 0 0 14px #232946;
    z-index: 20;
}
.gba-btn {
    position: absolute;
    background: #222a41;
    color: #fff;
    border-radius: 50%;
    border: 4px solid #8ff3fd;
    width: 48px; height: 48px;
    font-family: 'Press Start 2P', monospace;
    font-size: 1.35rem;
    text-align: center;
    line-height: 44px;
    cursor: pointer;
    box-shadow: 0 0 8px #00f2fe88;
    transition: background 0.2s;
    z-index: 30;
}
.gba-btn.left  { left: 32px;  top: 110px; }
.gba-btn.right { left: 510px; top: 110px; }
.gba-btn.start {
    left: 270px; top: 240px;
    border-radius: 14px;
    width: 72px; height: 34px;
    font-size: 1.05rem;
    line-height: 32px;
    background: #00f2fe;
    color: #232946;
    border: 2.3px solid #232946;
}
.gba-btn:hover { background: #fff8; color: #1de5fe; }
.gba-logo {
    position: absolute;
    left: 195px; top: 234px;
    color: #fff;
    font-family: 'Press Start 2P', monospace;
    font-size: 0.85rem;
    letter-spacing: 1.5px;
    text-shadow: 0 0 7px #fff, 0 0 3px #232946;
}
</style>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# 세션 상태
sections = ["📜 과거", "🏙️ 현재", "🌐 미래", "📊 인구 변화"]
if "section_idx" not in st.session_state:
    st.session_state.section_idx = 0
if "started" not in st.session_state:
    st.session_state.started = False

def gba_body(content):
    st.markdown(f"""
    <div class="gba-body">
        <div class="gba-title">YANGJU ARCHIVE GAME</div>
        <div class="gba-screen">{content}</div>
        <div class="gba-btn left" onclick="window.parent.postMessage({{ type: 'streamlit:buttonClick', buttonId: 'btn_left' }}, '*');">&#8592;</div>
        <div class="gba-btn right" onclick="window.parent.postMessage({{ type: 'streamlit:buttonClick', buttonId: 'btn_right' }}, '*');">&#8594;</div>
        <div class="gba-btn start" onclick="window.parent.postMessage({{ type: 'streamlit:buttonClick', buttonId: 'btn_start' }}, '*');">START</div>
        <div class="gba-logo">GAMEBOY ADVANCE</div>
    </div>
    """, unsafe_allow_html=True)

def section_content(idx):
    if idx == 0:
        return """<b>1. 고려~조선 시대, 북방의 행정·군사 중심지</b><br>
        - 양주목 설치: 경기 북부 광역 행정 단위<br>
        ...<br>
        <i>⬅️/➡️로 이동</i>"""
    elif idx == 1:
        return "<b>🏙️ 양주시의 현재</b><br>...<br><i>⬅️/➡️로 이동</i>"
    elif idx == 2:
        return "<b>🌐 양주시의 미래</b><br>...<br><i>⬅️/➡️로 이동</i>"
    else:
        return "<b>📊 양주시 인구 변화</b><br>...<br><i>⬅️/➡️로 이동</i>"

# 버튼 구현 (Streamlit 버튼 → 상태 변경)
col1, col2, col3 = st.columns([1,5,1])
with col1:
    left = st.button("⬅️", key="btn_left")
with col3:
    right = st.button("➡️", key="btn_right")
with col2:
    start = st.button("START", key="btn_start")

# 상태 변경
if left:
    st.session_state.section_idx = (st.session_state.section_idx - 1) % len(sections)
if right:
    st.session_state.section_idx = (st.session_state.section_idx + 1) % len(sections)
if start:
    st.session_state.section_idx = 0

# 게임기 도형과 화면 출력
gba_body(section_content(st.session_state.section_idx))
