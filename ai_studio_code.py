import streamlit as st
import google.generativeai as genai

# ... (Giữ nguyên phần CSS và Header ở trên) ...

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
