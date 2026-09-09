import os
import pandas as pd
import streamlit as st

st.title("🔍 사내 상품 상세페이지 조회 시스템")
st.write("자체상품코드를 입력하면 상세페이지 링크를 바로 확인할 수 있습니다.")

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "product_list.xlsx")

try:
  # sheet_name=None을 주면 엑셀 파일의 모든 시트를 한 번에 사전(dict) 형태로 읽어옵니다.
  excel_file = pd.ExcelFile(file_path)
  dfs = []
  for sheet_name in excel_file.sheet_names:
    temp_df = pd.read_excel(file_path, sheet_name=sheet_name)
    dfs.append(temp_df)

  # 모든 시트의 데이터를 하나로 합칩니다.
  df = pd.concat(dfs, ignore_index=True)

  # '자체상품코드', '상품명', '상세페이지 URL' 이라는 글자가 들어간 쓸모없는 행(헤더 중복 등)은 걸러냅니다.
  df = df[
      ~df["자체상품코드"]
      .astype(str)
      .str.contains("자체상품코드|nan|None", na=False)
  ]

except Exception as e:
  st.error(
      f"엑셀 파일을 읽는 중 오류가 발생했습니다. 파일 경로와 형식을"
      f" 확인해주세요. (에러: {e})"
  )
  st.stop()

# 2. 검색창 만들기
search_code = st.text_input("자체상품코드를 입력하거나 붙여넣으세요:")

# 3. 검색 결과 표시
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