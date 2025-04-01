
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 구글 시트 인증
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("your_credentials.json", scope)
gc = gspread.authorize(credentials)

# 구글 시트에서 데이터 불러오기
spreadsheet = gc.open("감정 수치 시트")  # 시트 이름을 여기에
worksheet = spreadsheet.worksheet("시트1")
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# 플레이어 선택
players = df["From"].unique()
selected_player = st.selectbox("플레이어 선택", players)

# 선택된 플레이어 기준 데이터 필터링
filtered_df = df[df["From"] == selected_player].sort_values("감정 수치")
bar_colors = ['blue' if val < 0 else 'red' for val in filtered_df["감정 수치"]]

# 시각화
fig, ax = plt.subplots(figsize=(10, 5))
x = range(len(filtered_df))
ax.bar(x, filtered_df["감정 수치"], color=bar_colors, width=0.35)
ax.set_xticks(x)
ax.set_xticklabels(filtered_df["To"], rotation=90)
ax.axhline(0, color='gray', linestyle='--')
ax.set_title(f"{selected_player}의 감정 수치")
ax.set_ylabel("감정 수치")
st.pyplot(fig)
