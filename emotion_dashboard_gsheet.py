
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import matplotlib.pyplot as plt

# 구글 서비스 계정 인증 정보
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Streamlit secrets에서 키 불러오기
creds_dict = st.secrets["gcp_service_account"]
credentials = Credentials.from_service_account_info(creds_dict, scopes=scope)

# gspread 인증
gc = gspread.authorize(credentials)

# 구글 시트에서 데이터 불러오기
spreadsheet = gc.open("감정 수치 시트")  # 여기에 정확한 시트 이름을 넣으세요.
worksheet = spreadsheet.sheet1  # 또는 시트 이름으로 가져올 수 있습니다.
data = worksheet.get_all_records()

# 데이터 확인
df = pd.DataFrame(data)
st.write(df)  # 데이터 확인용

# 선택된 플레이어 기준 데이터 필터링 및 시각화
players = df["From"].unique()
selected_player = st.selectbox("플레이어 선택", players)

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
