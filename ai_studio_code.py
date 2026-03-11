import streamlit as st
from google import genai

# Cấu hình trang (Tiêu đề, icon, layout)
st.set_page_config(page_title="CTU Text Generator", page_icon="🎓", layout="centered")

# CSS tùy chỉnh để có màu xanh đặc trưng của CTU
st.markdown("""
    <style>
    .stButton>button {
        background-color: #00529c;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #004080;
        color: white;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-color: #00529c;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# Giao diện Header
col1, col2 = st.columns([1, 5])
with col1:
    # Logo CTU (sử dụng link ảnh public)
    st.image("https://upload.wikimedia.org/wikipedia/vi/6/64/Logo_Đại_học_Cần_Thơ.svg", width=80)
with col2:
    st.title("CTU Text Generator")
    st.write("Công cụ hỗ trợ sinh viên Đại học Cần Thơ viết email và đơn từ học tập.")

st.divider()

# Form nhập liệu
st.subheader("📝 Thông tin yêu cầu")
col_mssv, col_khoa = st.columns(2)
with col_mssv:
    mssv = st.text_input("Mã số sinh viên (MSSV):", placeholder="VD: B1234567")
with col_khoa:
    khoa = st.text_input("Khoa / Viện:", placeholder="VD: CNTT & TT")

yeu_cau = st.text_area("Nội dung cần viết (*):", placeholder="VD: Viết email xin phép thầy cho vắng thi giữa kỳ môn Cấu trúc dữ liệu vì bị ốm...", height=100)

api_key = st.text_input("Nhập Gemini API Key của bạn:", type="password", help="Lấy API Key miễn phí tại Google AI Studio")

# Xử lý khi bấm nút
if st.button("Tạo văn bản 🚀"):
    if not yeu_cau:
        st.warning("Vui lòng nhập nội dung yêu cầu của bạn!")
    elif not api_key:
        st.warning("Vui lòng nhập Gemini API Key!")
    else:
        try:
            # Khởi tạo client Gemini
            client = genai.Client(api_key=api_key)
            
            # Xây dựng Prompt
            prompt = f"""
            Bạn là trợ lý hỗ trợ sinh viên Đại học Cần Thơ (CTU).
            Hãy viết một email/đơn từ dựa trên yêu cầu sau: {yeu_cau}

            Thông tin sinh viên:
            - MSSV: {mssv if mssv else '[Điền MSSV]'}
            - Khoa: {khoa if khoa else '[Điền Khoa]'}

            Yêu cầu bắt buộc:
            - Văn phong trang trọng, cực kỳ lịch sự, tôn sư trọng đạo.
            - Bắt đầu bằng "Kính gửi Thầy/Cô,".
            - Xưng "em".
            - Nêu rõ thông tin sinh viên (MSSV, Khoa).
            - Kết thúc bằng lời cảm ơn và trân trọng.
            """
            
            with st.spinner("Đang tạo văn bản..."):
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
            
            st.success("Tạo văn bản thành công!")
            st.subheader("✨ Kết quả")
            st.text_area("Bạn có thể copy đoạn văn bản dưới đây:", value=response.text, height=300)
            
        except Exception as e:
            st.error(f"Đã có lỗi xảy ra. Vui lòng kiểm tra lại API Key. Chi tiết lỗi: {e}")