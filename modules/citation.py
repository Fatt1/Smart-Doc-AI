# modules/citation.py
# ====================================================
# Module theo dõi nguồn gốc thông tin
# Hiển thị "Trích từ trang X" dưới câu trả lời
# ====================================================

import streamlit as st


def extract_sources(response):
    """
    Trích xuất thông tin nguồn từ response.

    Giải thích cho người mới:
        Khi RAG chain trả về kết quả, nó cũng trả về "context" —
        tức là các chunks đã dùng để trả lời.
        Mỗi chunk có metadata chứa thông tin nguồn (trang, file...).
    """
    source = []
    context_docs = response.get("context", [])
    for i, doc in enumerate(context_docs):
        source_info = {
            "index": i + 1,  # Đánh số nguồn từ 1
            "content": doc.page_content[:200] + "...",  # Hiển thị 200 ký tự đầu của chunk
            "page": doc.metadata.get("page", "N/A"),  # Lấy số trang nếu có
            "source": doc.metadata.get("source", "N/A")  # Lấy tên
        }
        source.append(source_info)
    return source

def display_sources(sources):
    """
    Hiển thị nguồn dưới câu trả lời.

    Giải thích cho người mới:
        st.expander() = tạo phần mở/đóng được
        Khi click vào "📄 Nguồn 1: Trang X", nó mở ra hiện đoạn text gốc
    """
    if not sources:
        return
    st.markdown("### 📚 Nguồn tham khảo:") 
    for src in sources:
        with st.expander(f"📄 Nguồn {src['index']}"):
             st.markdown(f"**File** {src['source']}")
             st.markdown(f"**Trang** {src['page']}")
             st.markdown(f"**Nội dung trích**")
             st.code(src['content'], language="none")
            
           
            
