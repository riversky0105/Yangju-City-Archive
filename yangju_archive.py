with tabs[3]:
    st.markdown('<div class="pixel-border">', unsafe_allow_html=True)
    st.header("📊 양주시 인구 변화")
    st.markdown("""
    <span style='color:#fff;'>양주시 인구 구조 변화를 월별/연도별 및 5년 단위 출생자수·사망자수와 함께 시각화합니다. 데이터 출처: KOSIS 국가통계포털</span>
    """, unsafe_allow_html=True)

    # --------- 인구수 변화 그래프 ---------
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
        # 제목/라벨/폰트(조건별)
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
