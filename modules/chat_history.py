# Module quản lý lịch sử chat
# Dùng st.session_state để lưu dữ liệu trong phiên làm việc

import streamlit as st
from datetime import datetime

def init_chat_history():
    """
    Khởi tạo chat history trong session_state.

    Giải thích cho người mới:
        st.session_state = "bộ nhớ tạm" của Streamlit
        - Dữ liệu được giữ lại khi user interact (click, nhập text...)
        - Dữ liệu bị mất khi đóng tab browser
        - Giống biến global nhưng an toàn cho mỗi user riêng
    """
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

def add_to_chat_history(question, answer):
    """Thêm cặp hỏi-đáp vào lịch sử."""
    st.session_state['chat_history'].append({
        'question': question,
        'answer': answer,
        'timestamp': datetime.now().strftime("%H:%M:%S")
    })

def get_history():
    """Lấy toàn bộ lịch sử chat."""
    return st.session_state.get('chat_history', [])

def clear_history():
    """Xóa lịch sử chat."""
    st.session_state['chat_history'] = []

def display_chat_history_sidebar():
    """
    Hiển thị lịch sử chat trong sidebar.

    Giải thích cho người mới:
        st.expander() tạo phần có thể mở/đóng (giống accordion)
        reversed() để hiển thị câu hỏi mới nhất lên đầu
    """
    with st.sidebar:
        st.markdown("---")
        st.subheader("💬 Lịch sử Chat")

        history = get_history()
        if not history:
            st.caption("Chưa có lịch sử chat.")
            return

        for i, chat in enumerate(reversed(history)):
            with st.expander(
                f"🕐 {chat['timestamp']} - {chat['question'][:30]}..."
            ):
                st.markdown(f"**Hỏi:** {chat['question']}")
                st.markdown(f"**Đáp:** {chat['answer']}")