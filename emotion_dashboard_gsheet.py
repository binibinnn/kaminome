
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import matplotlib.pyplot as plt

# 구글 서비스 계정 JSON 파일 경로
json_file_path = 'google_service_key.json'

# 인증 범위
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
credentials = Credentials.from_service_account_file(json_file_path, scopes=scope)
gc = gspread.authorize(credentials)

# 구글 시트를 시트 ID로 열기
spreadsheet = gc.open_by_key("1KhDx1GdC9y1pPXWFSQG2r9Hnn2_wziymZsfznsQQsd0")
worksheet = spreadsheet.sheet1
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# 열 이름 확인 출력
st.write("🧩 현재 시트 열 목록:", df.columns.tolist())

# 유사한 열 이름 자동 감지
from_col = next((col for col in df.columns if col.lower() == "from"), None)
to_col = next((col for col in df.columns if col.lower() == "to"), None)
score_col = next((col for col in df.columns if "감정" in col), None)

if not from_col or not to_col or not score_col:
    st.error("❌ 'From', 'To', '감정 수치'에 해당하는 열을 시트에서 찾을 수 없습니다.")
    st.stop()

# 선택된 플레이어 기준 데이터 필터링 및 시각화
players = df[from_col].unique()
selected_player = st.selectbox("플레이어 선택", players)
filtered_df = df[df[from_col] == selected_player].sort_values(score_col)
bar_colors = ['blue' if val < 0 else 'red' for val in filtered_df[score_col]]

# 시각화
fig, ax = plt.subplots(figsize=(10, 5))
x = range(len(filtered_df))
ax.bar(x, filtered_df[score_col], color=bar_colors, width=0.35)
ax.set_xticks(x)
ax.set_xticklabels(filtered_df[to_col], rotation=90)
ax.axhline(0, color='gray', linestyle='--')
ax.set_title(f"{selected_player}의 감정 수치")
ax.set_ylabel("감정 수치")
st.pyplot(fig)
