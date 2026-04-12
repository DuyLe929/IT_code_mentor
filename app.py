import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# 1. Tải các biến môi trường từ file .env
load_dotenv()

# 2. Lấy API Key từ biến môi trường
api_key = os.getenv("GROQ_API_KEY")

# 3. Khởi tạo Client (Sử dụng biến api_key đã lấy)
client = Groq(api_key=api_key)

st.set_page_config(page_title="IT code mentor", page_icon="🦙",layout = "wide")
st.title("🦙 Llama 3.3: Hệ thống Tối ưu Code")
st.write("Dành cho sinh viên AIT - Chấm điểm & Gợi ý code chuyên sâu")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📥 Input Code")
    lang = st.selectbox("Ngôn ngữ", ["Python", "C++", "Java"])
    code_input = st.text_area("Dán code vào đây:", height=450)
    analyze_btn = st.button("Phân tích với Llama 3.3")

with col2:
    st.markdown("### 💡 Kết quả từ Mentor AI")
    if analyze_btn and code_input:
        with st.spinner("Llama 3.3 đang suy luận..."):
            try:
                # Gọi API Groq với model Llama 3.3
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "Bạn là một chuyên gia tối ưu hóa mã nguồn. Hãy phân tích code của sinh viên và phản hồi bằng tiếng Việt: 1. Lỗi logic, 2. Đánh giá Clean Code, 3. Phiên bản tối ưu (kèm giải thích O(n))."
                        },
                        {
                            "role": "user",
                            "content": f"Ngôn ngữ {lang}. Code: \n{code_input}"
                        }
                    ],
                    model="llama-3.3-70b-versatile",
                )
                
                result = chat_completion.choices[0].message.content
                st.markdown(result)
            except Exception as e:
                st.error(f"Lỗi: {e}")
    else:
        st.info("Đang chờ code đầu vào...")