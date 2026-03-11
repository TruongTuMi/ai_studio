import streamlit as st
import google.generativeai as genai

# Cấu hình trang
st.set_page_config(page_title="CTU Text Generator", page_icon="🎓", layout="centered")

# CSS tùy chỉnh màu xanh CTU
st.markdown("""
    <style>
    .stButton>button { background-color: #00529c; color: white; border-radius: 8px; font-weight: bold; width: 100%; }
    .stButton>button:hover { background-color: #004080; color: white; }
    .stTextInput>div>div>input, .stTextArea>div>textarea { border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# Header
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/vi/6/6c/Logo_Dai_hoc_Can_Tho.svg", width=80)
with col2:
    st.title("CTU Text Generator")
    st.write("Công cụ hỗ trợ sinh viên Đại học Cần Thơ viết email và đơn từ học tập.")

st.divider()

# Form nhập liệu
st.subheader("📝 Thông tin yêu cầu")

ho_ten = st.text_input("Họ và tên sinh viên:", placeholder="VD: Dương Chí Trường")

col_mssv, col_khoa = st.columns(2)
with col_mssv:
    mssv = st.text_input("Mã số sinh viên (MSSV):", placeholder="VD: DC25V7X631")
with col_khoa:
    khoa = st.text_input("Khoa / Viện:", placeholder="VD: CNTT & TT")

yeu_cau = st.text_area("Nội dung cần viết (*):", placeholder="VD: Viết email xin phép thầy cho vắng thi giữa kỳ môn Cấu trúc dữ liệu vì bị ốm...", height=100)

api_key = st.text_input("Nhập Gemini API Key của bạn:", type="password", help="Lấy API Key miễn phí tại Google AI Studio")

# Xử lý tạo văn bản
if st.button("Tạo văn bản 🚀"):
    if not yeu_cau:
        st.warning("Vui lòng nhập nội dung yêu cầu của bạn!")
    elif not api_key:
        st.warning("Vui lòng nhập Gemini API Key!")
    else:
        try:
            # 1. Cấu hình API
            genai.configure(api_key=api_key)
            
            # 2. Đổi tên model thành 'gemini-1.5-flash' (Bỏ chữ 'models/') 
            # hoặc dùng 'gemini-1.5-flash-latest' để đảm bảo luôn chạy bản mới nhất
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Bạn là trợ lý hỗ trợ sinh viên Đại học Cần Thơ (CTU).
            Hãy viết một email/đơn từ dựa trên yêu cầu sau: {yeu_cau}

            Thông tin sinh viên:
            - Họ và tên: {ho_ten if ho_ten else '[Điền Họ và tên]'}
            - MSSV: {mssv if mssv else '[Điền MSSV]'}
            - Khoa: {khoa if khoa else '[Điền Khoa]'}

            Yêu cầu bắt buộc:
            - Văn phong trang trọng, cực kỳ lịch sự, tôn sư trọng đạo đúng chất sinh viên miền Tây.
            - Phải nhắc đến các thông tin định danh (Họ tên, MSSV, Khoa) một cách tự nhiên.
            - Kết thúc bằng lời chúc sức khỏe Thầy/Cô và lời cảm ơn trân trọng.
            """
            
            with st.spinner("Đang tạo văn bản..."):
                # Dùng generate_content thay vì các lệnh cũ
                response = model.generate_content(prompt)
            
            if response.text:
                st.success("Tạo văn bản thành công!")
                st.subheader("✨ Kết quả")
                st.text_area("Nội dung tạo ra (Bạn có thể copy trực tiếp):", value=response.text, height=400)
                st.download_button("Tải văn bản về máy (.txt)", response.text, file_name="van_ban_ctu.txt")
            
        except Exception as e:
            # Nếu vẫn lỗi 1.5-flash, thử dùng model 'gemini-pro' (Dòng này để dự phòng)
            st.error(f"Lỗi: {e}. Đang thử kết nối lại với máy chủ dự phòng...")
            try:
                model_backup = genai.GenerativeModel('gemini-pro')
                response = model_backup.generate_content(prompt)
                st.success("Đã kết nối qua máy chủ dự phòng thành công!")
                st.text_area("Kết quả dự phòng:", value=response.text, height=400)
            except:
                st.error("Không thể kết nối với mô hình AI. Vui lòng kiểm tra lại API Key hoặc vùng lãnh thổ.")
