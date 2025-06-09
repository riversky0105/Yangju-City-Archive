import streamlit as st

st.set_page_config(page_title="양주시 아카이브", layout="wide")

# CSS 스타일로 문단 간격 및 여백 조정
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
    st.subheader("1. 옥정·회천 신도시 개발")
    st.markdown("""
    - 수도권 주택난 해소 위한 대규모 개발  
    - 아파트, 도로망, 도시철도 확장  
    - 인구 약 25만 명, 서울 접근성 뛰어남
    """)

    st.subheader("2. 산업기반 확충")
    st.markdown("""
    - 양주테크노밸리 등 첨단산업단지 개발  
    - 의료, 바이오, IT 기업 유치  
    - 고용 창출 및 세수 확대 기대
    """)

    st.subheader("3. 문화·관광 자원 리브랜딩")
    st.markdown("""
    - 장흥 조각공원, 송암천문대, 나리농원 운영  
    - 전통+현대예술 융합한 장흥문화예술촌 활성화  
    - 회암사지와 연계한 콘텐츠 기획
    """)

    st.subheader("4. 교통 인프라 개선")
    st.markdown("""
    - 지하철 7호선 연장공사  
    - GTX-C 개통 시 서울 접근성 증가  
    - 수도권 제2순환도로 일부 개통
    """)

    st.subheader("5. 도시·농촌 복합형 구조")
    st.markdown("""
    - 도심은 아파트 중심, 외곽은 농촌·산림지  
    - 다양한 커뮤니티와 라이프스타일 공존
    """)

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

# --- 이미지 예시: 만약 이미지 넣을 때 ---
# st.image("path/to/image.png", use_container_width=True)
st.image("path/to/양주 회암사지.jpg", use_container_width=True)



