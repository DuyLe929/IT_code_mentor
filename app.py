import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
import json
from datetime import datetime

# Tải các biến môi trường từ file .env
load_dotenv()

# Lấy API Key từ biến môi trường
api_key = os.getenv("GROQ_API_KEY")

# Kiểm tra xem api_key có null hay không
if api_key is None:
    st.error("❌ API Key chưa được thiết lập. Vui lòng kiểm tra file .env")
    st.stop()  # ✅ Dùng st.stop() thay cho exit()

# Khởi tạo Client
client = Groq(api_key=api_key)

# ─────────────────────────────────────────────
# Khởi tạo Session State
# ─────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

if "result" not in st.session_state:
    st.session_state.result = None

if "score" not in st.session_state:
    st.session_state.score = None


# ─────────────────────────────────────────────
# Hàm gọi API phân tích code
# ─────────────────────────────────────────────
def call_api(lang, code_input):
    system_prompt = f"""Bạn là một giáo viên chấm bài lập trình chuyên nghiệp dành cho sinh viên IT.
Nhiệm vụ: Phân tích đoạn code {lang} của sinh viên một cách chi tiết và có cấu trúc.

Trả lời CHÍNH XÁC theo cấu trúc sau (dùng Markdown):

## 1. 🐛 Lỗi Logic & Runtime
Liệt kê từng lỗi cụ thể, giải thích tại sao sai và ảnh hưởng như thế nào.
Nếu không có lỗi, ghi: ✅ Không phát hiện lỗi logic.

## 2. 📏 Đánh giá Clean Code
Nhận xét về: đặt tên biến/hàm, cấu trúc code, comment, tuân thủ chuẩn ngôn ngữ (PEP8 với Python, Google Style với Java/C++...).

## 3. ⏱️ Phân tích Độ phức tạp
- **Time Complexity**: O(?) — giải thích lý do
- **Space Complexity**: O(?) — giải thích lý do

## 4. ✅ Code Tối ưu
```{lang.lower()}
# Dán code đã tối ưu vào đây
```
Giải thích ngắn gọn tại sao phiên bản này tốt hơn.

## 5. 🏆 Điểm số tổng thể: X/10
**Breakdown điểm:**
- Tính đúng đắn: X/4
- Clean Code: X/3
- Hiệu suất: X/3

**Nhận xét tổng thể:** (2-3 câu nhận xét & lời khuyên cho sinh viên)
"""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Ngôn ngữ: {lang}\n\nCode của sinh viên:\n```\n{code_input}\n```"}
            ],
            model="llama-3.3-70b-versatile",
        )
        result = chat_completion.choices[0].message.content
        return result
    except Exception as e:
        st.error(f"❌ Lỗi khi gọi API: {e}")
        return None


# ─────────────────────────────────────────────
# Hàm trích xuất điểm số từ kết quả
# ─────────────────────────────────────────────
def extract_score(result_text):
    """Trích xuất điểm số từ phần '🏆 Điểm số tổng thể: X/10'"""
    try:
        import re
        match = re.search(r'Điểm số tổng thể[:\s]*(\d+(?:\.\d+)?)/10', result_text, re.IGNORECASE)
        if match:
            return float(match.group(1))
    except Exception:
        pass
    return None


# ─────────────────────────────────────────────
# Hàm màu điểm số
# ─────────────────────────────────────────────
def score_color(score):
    if score is None:
        return "gray"
    if score >= 8:
        return "green"
    elif score >= 6:
        return "orange"
    else:
        return "red"


def score_label(score):
    if score is None:
        return "—"
    if score >= 9:
        return "Xuất sắc 🏆"
    elif score >= 8:
        return "Tốt 🥇"
    elif score >= 6:
        return "Khá 👍"
    elif score >= 5:
        return "Trung bình ⚠️"
    else:
        return "Cần cải thiện ❗"


# ─────────────────────────────────────────────
# Giao diện chính
# ─────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="IT Code Mentor",
        page_icon="🦙",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # CSS tuỳ chỉnh
    st.markdown("""
    <style>
        .score-badge {
            display: inline-block;
            padding: 6px 18px;
            border-radius: 20px;
            font-size: 1.4rem;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .history-card {
            background: #1e1e2e;
            border: 1px solid #313244;
            border-radius: 10px;
            padding: 12px 16px;
            margin-bottom: 10px;
            cursor: pointer;
        }
        .history-card:hover {
            border-color: #89b4fa;
        }
        .stButton > button {
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True)

    # ── SIDEBAR: Lịch sử phân tích ──────────────
    with st.sidebar:
        st.markdown("## 📜 Lịch sử Phân tích")
        st.caption(f"Tổng: {len(st.session_state.history)} lần phân tích")

        if not st.session_state.history:
            st.info("Chưa có lịch sử. Hãy phân tích code đầu tiên!")
        else:
            # Nút xoá lịch sử
            if st.button("🗑️ Xoá toàn bộ lịch sử"):
                st.session_state.history = []
                st.session_state.result = None
                st.session_state.score = None
                st.rerun()

            st.divider()

            # Hiển thị từng mục lịch sử (mới nhất lên đầu)
            for i, h in enumerate(reversed(st.session_state.history)):
                idx = len(st.session_state.history) - i
                score = h.get("score")
                color = score_color(score)
                score_text = f"{score}/10" if score is not None else "N/A"

                with st.expander(f"#{idx} · {h['lang']} · {score_text} · {h['time']}"):
                    st.caption("**File:**" + (f" {h['filename']}" if h.get('filename') else " (dán thủ công)"))
                    st.code(h["code"][:300] + ("..." if len(h["code"]) > 300 else ""), language=h["lang"].lower())

                    if st.button(f"📂 Tải lại phân tích #{idx}", key=f"load_{idx}"):
                        st.session_state.result = h["result"]
                        st.session_state.score = h["score"]
                        st.rerun()

    # ── HEADER ─────────────────────────────────
    st.title("🦙 Llama 3.3 · IT Code Mentor")
    st.write("Hệ thống **chấm điểm & tối ưu code** dành cho sinh viên IT")
    st.divider()

    input_col, output_col = st.columns([1, 1], gap="large")

    # ── CỘT TRÁI: Input ─────────────────────────
    with input_col:
        st.markdown("### 📥 Nhập Code")

        lang = st.selectbox(
            "🌐 Ngôn ngữ lập trình",
            ["Python", "C++", "Java", "JavaScript", "C"],
            index=0
        )

        # Tab: Dán code / Upload file
        tab_paste, tab_upload = st.tabs(["✏️ Dán Code", "📁 Upload File"])

        code_input = ""
        uploaded_filename = None

        with tab_paste:
            code_input_paste = st.text_area(
                "Dán code của bạn vào đây:",
                height=380,
                placeholder="# Paste your code here...",
                key="paste_area"
            )
            code_input = code_input_paste

        with tab_upload:
            uploaded_file = st.file_uploader(
                "Upload file code",
                type=["py", "cpp", "java", "js", "c", "txt"],
                help="Hỗ trợ: .py, .cpp, .java, .js, .c, .txt"
            )
            if uploaded_file is not None:
                try:
                    code_input_upload = uploaded_file.read().decode("utf-8")
                    uploaded_filename = uploaded_file.name
                    st.success(f"✅ Đã đọc file: **{uploaded_filename}** ({len(code_input_upload)} ký tự)")
                    st.code(code_input_upload, language=lang.lower())
                    code_input = code_input_upload
                except Exception as e:
                    st.error(f"❌ Không đọc được file: {e}")

        # Nút phân tích
        analyze_btn = st.button(
            "🚀 Phân tích với Llama 3.3",
            type="primary",
            use_container_width=True
        )

    # ── CỘT PHẢI: Output ────────────────────────
    with output_col:
        st.markdown("### 💡 Kết quả từ Mentor AI")

        if analyze_btn:
            if not code_input.strip():
                st.warning("⚠️ Vui lòng nhập hoặc upload code trước khi phân tích!")
            else:
                with st.spinner("🔄 Llama 3.3 đang phân tích..."):
                    result = call_api(lang, code_input)

                if result:
                    score = extract_score(result)
                    st.session_state.result = result
                    st.session_state.score = score

                    # Lưu vào lịch sử
                    st.session_state.history.append({
                        "lang": lang,
                        "code": code_input,
                        "result": result,
                        "score": score,
                        "filename": uploaded_filename,
                        "time": datetime.now().strftime("%H:%M %d/%m")
                    })

        # Hiển thị kết quả
        if st.session_state.result:
            score = st.session_state.score
            color = score_color(score)
            label = score_label(score)

            # Badge điểm số
            if score is not None:
                st.markdown(
                    f'<div class="score-badge" style="background-color:{color}22; '
                    f'color:{color}; border: 2px solid {color};">'
                    f'🏆 {score}/10 &nbsp;·&nbsp; {label}</div>',
                    unsafe_allow_html=True
                )

            st.markdown(st.session_state.result)

            # Nút tải kết quả
            st.download_button(
                label="💾 Tải kết quả (.md)",
                data=st.session_state.result,
                file_name=f"phan_tich_{lang}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        else:
            st.info("⏳ Đang chờ code đầu vào... Dán code hoặc upload file rồi nhấn **Phân tích**.")

            # Hướng dẫn nhanh
            with st.expander("📖 Hướng dẫn sử dụng"):
                st.markdown("""
1. **Chọn ngôn ngữ** lập trình phù hợp
2. **Dán code** vào ô bên trái hoặc **upload file** code
3. Nhấn **🚀 Phân tích với Llama 3.3**
4. Xem kết quả gồm: lỗi logic, clean code, độ phức tạp, code tối ưu và **điểm số /10**
5. Lịch sử phân tích được lưu ở **thanh bên trái**
                """)


if __name__ == "__main__":
    main()