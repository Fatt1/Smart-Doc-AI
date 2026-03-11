
import streamlit as st
from ui.styles import get_custom_css
from ui.sidebar import render_sidebar
from ui.main_page import render_main_page
# Entry point — File chính để chạy ứng dụng
# Chạy bằng: streamlit run app.py
def main():
    """
    Hàm chính của ứng dụng.

    Giải thích cho người mới:
        st.set_page_config(): Cài đặt cấu hình trang web
        - page_title: Tiêu đề trên tab browser
        - page_icon: Icon trên tab browser
        - layout: "wide" = dùng toàn bộ chiều rộng màn hình
    """
    st.set_page_config(
        page_title="SmartDoc AI",
        page_icon="📚",
        layout="wide"
    )
    st.markdown(get_custom_css(), unsafe_allow_html=True)  # Inject CSS
    render_sidebar()  # Hiển thị sidebar
    render_main_page()  # Hiển thị nội dung chính
    

if __name__ == "__main__":
    main()