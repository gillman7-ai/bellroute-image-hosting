import os
import pandas as pd
import streamlit as st

# 웹페이지 상단 제목 설정
st.title("🔍 벨루트/옷미녀 상품 조회 시스템")
st.write("자체상품코드를 입력하면 상세페이지 링크를 바로 확인할 수 있습니다.")

# 1. 엑셀 파일 경로 설정 (현재 코드 파일과 같은 폴더에 있다고 명시)
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "product_list.xlsx")

try:
  df = pd.read_excel(file_path)
except FileNotFoundError:
  st.error(
      f"'{file_path}' 경로에서 엑셀 파일을 찾을 수 없습니다. 엑셀 파일이"
      " 'product_search' 폴더 안에 있는지 확인해주세요."
  )
  st.stop()

# 2. 검색창 만들기
search_code = st.text_input("자체상품코드를 입력하거나 붙여넣으세요:")

# 3. 검색 버튼 또는 엔터 입력 시 결과 표시
if search_code:
  df["자체상품코드_str"] = df["자체상품코드"].astype(str).str.strip()
  search_code_clean = str(search_code).strip()

  result = df[df["자체상품코드_str"] == search_code_clean]

  if not result.empty:
    st.success("상품을 찾았습니다! 🎉")

    for index, row in result.iterrows():
      p_name = row["상품명"]
      p_url = row["상세페이지 URL"]

      st.markdown(f"### **상품명:** {p_name}")
      st.link_button("🔗 상세페이지 바로가기", p_url)
      st.divider()
  else:
    st.warning("존재하지 않는 자체상품코드입니다. 코드를 다시 확인해주세요.")