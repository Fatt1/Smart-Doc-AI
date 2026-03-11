import streamlit as st

from modules.chat_history import display_chat_history_sidebar, clear_history

def render_sidebar():
    """
    Hiển thị sidebar với hướng dẫn và thông tin.

    Giải thích cho người mới:
        st.sidebar.xxx() = hiển thị component ở thanh bên trái
        st.sidebar.title() = tiêu đề
        st.sidebar.markdown() = text với Markdown formatting
    """
    with st.sidebar:
        st.title("📚 SmartDoc AI")
        st.markdown("---")
        st.subheader("📖Hướng dẫn sử dụng")
        st.markdown("""
            1. **Upload** file PDF hoặc DOCX
            2. **Chờ** hệ thống xử lý tài liệu
            3. **Đặt câu hỏi** về nội dung tài liệu
            4. **Nhận câu trả lời** từ AI
            """)
        st.markdown("---")
        st.subheader("⚙️ Cấu hình")
        st.markdown(f"""
            - **Model**: qwen2.5:14b
            - **Embedding**: Multilingual MPNet
            - **Vector DB**: FAISS (GPU)
            - **Ngôn ngữ**: Tiếng Việt & English
            """)
        st.markdown("---")
        st.caption("SmartDoc AI v1.0 | OSSD 2026")
        st.markdown("----")
        st.subheader("Chunk Settings")
        chunk_size = st.select_slider("Chunk Size (Ký tự)", options=[500, 1000, 1500, 2000], value=1000, help="Nhỏ→chính xác hơn nhưng ít context. Lớn→nhiều context nhưng noise.")
        chunk__overlap = st.select_slider("Chunk Overlap (Ký tự)", options=[50, 100, 150, 200], value=100, help="Số ký tự chồng lặp giữa các chunk. Giúp giữ ngữ cảnh liên tục.")
        st.session_state.chunk_size = chunk_size
        st.session_state.chunk_overlap = chunk__overlap
        # --- NÚT XÓA ---
        st.markdown("---")
        st.subheader("🗑️ Quản lý")

        # Nút xóa lịch sử chat
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🗑️ Xóa Chat", use_container_width=True):
                st.session_state.confirm_clear_chat = True

        with col2:
            if st.button("🗑️ Xóa Docs", use_container_width=True):
                st.session_state.confirm_clear_docs = True

        # Confirmation dialog cho xóa chat
        if st.session_state.get("confirm_clear_chat", False):
            st.warning("⚠️ Bạn có chắc muốn xóa lịch sử chat?")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Xác nhận", key="confirm_chat"):
                    clear_history()
                    st.session_state.confirm_clear_chat = False
                    st.rerun()  # Reload trang
            with c2:
                if st.button("❌ Hủy", key="cancel_chat"):
                    st.session_state.confirm_clear_chat = False
                    st.rerun()

        # Confirmation dialog cho xóa vector store
        if st.session_state.get("confirm_clear_docs", False):
            st.warning("⚠️ Bạn có chắc muốn xóa tài liệu đã upload?")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Xác nhận", key="confirm_docs"):
                    # Xóa vector store và file đã xử lý
                    for key in ["vector_store", "retriever", "processed_file"]:
                        st.session_state.pop(key, None)
                    st.session_state.confirm_clear_docs = False
                    st.rerun()
            with c2:
                if st.button("❌ Hủy", key="cancel_docs"):
                    st.session_state.confirm_clear_docs = False
                    st.rerun()

        display_chat_history_sidebar()

