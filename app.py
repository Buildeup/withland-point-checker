import streamlit as st
import pandas as pd
from gsheet_utils import load_data_from_gsheet

st.set_page_config(page_title="위드랜드 포인트 계산기", page_icon="🏝️")

st.title("위드랜드 포인트 계산기")
st.markdown(
    """
    리조트, 객실, 시즌, 날짜를 선택하면 해당 기간의 총 포인트와 날짜별 포인트 내역을 확인할 수 있습니다.
    """
)

@st.cache_data
def load_data():
    return load_data_from_gsheet()

df = load_data()

# 선택 영역을 2컬럼으로 분리
col1, col2 = st.columns(2)

with col1:
    resort_list = sorted(df['resort'].unique())
    selected_resort = st.selectbox("🏝️ 리조트", resort_list)

    room_list = sorted(df[df['resort'] == selected_resort]['room'].unique())
    selected_room = st.selectbox("🛏️ 객실", room_list)

with col2:
    season_list = sorted(df[
        (df['resort'] == selected_resort) &
        (df['room'] == selected_room)
    ]['season'].unique())
    selected_season = st.selectbox("📅 시즌", season_list)

    today = pd.Timestamp.today().date()
    checkin_date = st.date_input("체크인 날짜", value=today)
    checkout_date = st.date_input("체크아웃 날짜", value=today + pd.Timedelta(days=1))

# 유효성 검사 및 결과
if checkin_date >= checkout_date:
    st.error("❗ 체크아웃 날짜는 체크인 날짜 이후여야 합니다.")
else:
    stay_dates = pd.date_range(checkin_date, checkout_date - pd.Timedelta(days=1))
    total_points = 0
    daily_points = []

    for date in stay_dates:
        weekday = date.weekday()
        daytype = "주말" if weekday >= 4 else "주중"

        filtered = df[
            (df['resort'] == selected_resort) &
            (df['room'] == selected_room) &
            (df['season'] == selected_season) &
            (df['daytype'] == daytype)
        ]

        if not filtered.empty:
            point = filtered.iloc[0]['point']
            total_points += point
            daily_points.append({
                "날짜": date.strftime("%Y-%m-%d"),
                "요일": daytype,
                "포인트": point
            })
        else:
            daily_points.append({
                "날짜": date.strftime("%Y-%m-%d"),
                "요일": daytype,
                "포인트": "정보 없음"
            })

    st.success(f" {selected_resort} / {selected_room} [{selected_season}] {len(stay_dates)}박: 총 {total_points:,} 포인트")
    st.markdown("### 🗓️ 날짜별 포인트 내역")
    st.dataframe(pd.DataFrame(daily_points), hide_index=True)
