import pandas as pd
import streamlit as st

# 웹페이지 상단 제목 설정
st.title("🔍 사내 상품 상세페이지 조회 시스템")
st.write("자체상품코드를 입력하면 상세페이지 링크를 바로 확인할 수 있습니다.")

# 1. 엑셀 파일 불러오기 (파일 이름이 다르면 여기를 수정하세요)
file_name = "product_list.xlsx"

try:
  df = pd.read_excel(file_name)
except FileNotFoundError:
  st.error(
      f"'{file_name}' 파일을 찾을 수 없습니다. 파이썬 코드와 같은 폴더에"
      " 엑셀 파일이 있는지 확인해주세요."
  )
  st.stop()

# 2. 검색창 만들기
search_code = st.text_input("자체상품코드를 입력하거나 붙여넣으세요:")

# 3. 검색 버튼 또는 엔터 입력 시 결과 표시
if search_code:
  # 대소문자나 공백 차이로 검색이 안 되는 것을 막기 위해 문자열로 변환 후 비교
  df["자체상품코드_str"] = df["자체상품코드"].astype(str).str.strip()
  search_code_clean = str(search_code).strip()

  result = df[df["자체상품코드_str"] == search_code_clean]

  if not result.empty:
    st.success("상품을 찾았습니다! 🎉")

    # 결과가 여러 개일 수 있으므로 반복문으로 모두 출력
    for index, row in result.iterrows():
      p_name = row["상품명"]
      p_url = row["상세페이지 URL"]

      st.markdown(f"### **상품명:** {p_name}")
      # 커다란 버튼 형태의 링크 제공
      st.link_button("🔗 상세페이지 바로가기", p_url)
      st.divider()
  else:
    st.warning("존재하지 않는 자체상품코드입니다. 코드를 다시 확인해주세요.")