# 🦙 IT Code Mentor - Intelligent Programming Assistant

**IT Code Mentor** là một hệ thống hỗ trợ học tập thông minh dành riêng cho sinh viên ngành Công nghệ thông tin (đặc biệt là sinh viên AIT - VNU-IS). Hệ thống ứng dụng mô hình ngôn ngữ lớn **Llama 3.3 (70B)** kết hợp với hạ tầng siêu máy tính **Groq LPU** để cung cấp các giải pháp tối ưu hóa mã nguồn tức thì.

## 🎯 Mục tiêu dự án
Dự án được xây dựng nhằm giải quyết bài toán "hỗ trợ giáo dục cá nhân hóa", đóng vai trò như một Mentor ảo 24/7 giúp sinh viên:
- Sửa lỗi logic và cú pháp trong mã nguồn.
- Tiếp cận các tiêu chuẩn viết code sạch (**Clean Code**).
- Hiểu sâu về tối ưu thuật toán thông qua phân tích độ phức tạp thời gian **Big O ($O(n)$)**.

## 🚀 Tính năng chính
- **Logic Debugging:** Phát hiện và sửa lỗi thực thi nhanh chóng.
- **Code Refactoring:** Tái cấu trúc mã nguồn để tăng tính dễ đọc và bảo trì.
- **Performance Analysis:** Phân tích và đề xuất thuật toán tối ưu hơn (ví dụ: chuyển từ $O(n^2)$ sang $O(n \log n)$).
- **Multi-language Support:** Hỗ trợ tốt nhất cho Python, C++, và Java.

## 🛠️ Công nghệ sử dụng
- **Backend:** Python & Streamlit.
- **AI Engine:** Llama-3.3-70b-versatile (via Groq API).
- **Security:** Quản lý mã khóa qua biến môi trường (.env) và bảo vệ mã nguồn (.gitignore).

### 📦 Hướng dẫn cài đặt

## Cách 1: Sử dụng Git Clone
1. Clone repository:
   ```bash
   git clone [https://github.com/DuyLe929/IT_code_mentor.git](https://github.com/DuyLe929/IT_code_mentor.git)
   cd IT_code_mentor
   ```
2. Tạo và kích hoạt môi trường ảo:
    Windows: python -m venv venv sau đó .\venv\Scripts\activate
    macOS/Linux: python3 -m venv venv sau đó source venv/bin/activate

## Cách 2: Tải thủ công 
    Truy cập vào Repository này, nhấn Code -> Download ZIP.
    Giải nén và mở Terminal tại thư mục vừa giải nén. 

### 🚀 Cách sử dụng 
1. Cài đặt thư viện:

    pip install -r requirements.txt

2. Cấu hình API Key:

    Tạo file .env tại thư mục gốc.

    Thêm dòng: GROQ_API_KEY=your_key_here (Lấy key tại console.groq.com).

3. Chạy ứng dụng:

    python -m streamlit run app.py