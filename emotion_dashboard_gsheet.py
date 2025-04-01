
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import gspread
from google.oauth2.service_account import Credentials

# 구글 시트 인증 정보
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Streamlit secrets에서 키 불러오기
creds_dict = st.secrets["gcp_service_account"]
credentials = Credentials.from_service_account_info(creds_dict, scopes=scope)

# gspread 인증
gc = gspread.authorize(credentials)

# 구글 시트에서 데이터 불러오기
spreadsheet = gc.open("감정 수치 시트")
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
