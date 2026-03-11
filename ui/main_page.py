import streamlit as st
from modules.document_loader import load_document
from modules.text_splitter import split_documents
from modules.embeddings import create_embedder
from modules.vector_store import create_vector_store, get_retriever
from modules.llm_chain import create_llm, create_rag_chain, ask_question
from config.settings import SUPPORTED_EXTENSIONS
from modules.chat_history import (init_chat_history, add_to_chat_history, display_chat_history_sidebar)
from modules.citation import extract_sources, display_sources


def render_main_page():
    
    """Hiển thị giao diện trang chính."""
    init_chat_history()

    st.title("🤖 SmartDoc AI")
    st.subheader("Intelligent Document Q&A System")
    st.markdown("Upload tài liệu và đặt câu hỏi — AI sẽ trả lời dựa trên nội dung!")

    st.markdown("---")

    # --- PHẦN 1: UPLOAD FILE + CHỌN CHẾ ĐỘ ĐỌC ---
    st.subheader("📁 Upload Tài Liệu")

    # st.tabs tạo các tab cho user lựa chọn chế độ đọc
    # Tab 1: Đọc thường (PDFPlumber) — cho PDF text bình thường
    # Tab 2: OCR Mode (Tesseract) — cho PDF toàn hình ảnh/scan
    tab_normal, tab_ocr = st.tabs(["📄 Đọc thường", "📸 OCR Mode"])

    with tab_normal:
        st.caption("Dùng cho PDF/DOCX có text bình thường (copy được chữ)")
        uploaded_file_normal = st.file_uploader(
            "Chọn file PDF hoặc DOCX",
            type=["pdf", "docx"],
            help="Kéo thả file vào đây hoặc click để chọn",
            key="upload_normal"  # key riêng để không xung đột với tab OCR
        )

    with tab_ocr:
        st.caption("⚠️ Dùng cho PDF dạng hình ảnh/scan (không copy được chữ)")
        st.info("💡 OCR sẽ chuyển mỗi trang PDF → ảnh → nhận diện chữ. "
                "Quá trình này chậm hơn đọc thường.")
        uploaded_file_ocr = st.file_uploader(
            "Chọn file PDF (scan/hình ảnh)",
            type=["pdf"],  # OCR chỉ hỗ trợ PDF
            help="File PDF mà bạn không thể copy chữ được",
            key="upload_ocr"  # key riêng
        )

    # Xác định file nào được upload và chế độ đọc
    # Ưu tiên: nếu cả 2 tab đều có file, dùng file được upload gần nhất
    uploaded_file = None
    use_ocr = False

    if uploaded_file_ocr is not None:
        uploaded_file = uploaded_file_ocr
        use_ocr = True
    if uploaded_file_normal is not None:
        uploaded_file = uploaded_file_normal
        use_ocr = False

    # --- PHẦN 2: XỬ LÝ FILE ---
    if uploaded_file is not None:
        # Tạo cache key bao gồm tên file + chế độ đọc
        # → Nếu cùng file nhưng đổi chế độ → xử lý lại
        cache_key = f"{uploaded_file.name}_{'ocr' if use_ocr else 'normal'}"

        if "processed_file" not in st.session_state or \
           st.session_state.processed_file != cache_key:

            if use_ocr:
                with st.spinner("📸 Đang OCR tài liệu (chuyển ảnh → chữ)..."):
                    docs = load_document(uploaded_file, use_ocr=True)
                st.warning(f"📸 Đã dùng OCR để đọc: {uploaded_file.name}")
            else:
                with st.spinner("📄 Đang đọc tài liệu..."):
                    docs = load_document(uploaded_file, use_ocr=False)

            with st.spinner("✂️ Đang chia nhỏ văn bản..."):
                chunks = split_documents(docs, chunk_size=st.session_state.chunk_size,
                                          chunk_overlap=st.session_state.chunk_overlap)
                st.info(f"📊 Đã chia thành {len(chunks)} chunks")

            with st.spinner("🔢 Đang tạo embeddings (dùng GPU)..."):
                embedder = create_embedder()
                vector_store = create_vector_store(chunks, embedder)
                retriever = get_retriever(vector_store)

            # Lưu vào session_state để không phải xử lý lại
            st.session_state.retriever = retriever
            st.session_state.vector_store = vector_store
            st.session_state.processed_file = cache_key
            st.session_state.llm = create_llm()

            method_text = "OCR (Tesseract)" if use_ocr else "PDFPlumber"
            st.success(f"✅ Đã xử lý thành công: {uploaded_file.name} [{method_text}]")

    # --- PHẦN 3: HỎI ĐÁP ---
    if "retriever" in st.session_state:
        st.markdown("---")
        st.subheader("❓ Đặt Câu Hỏi")

        user_input = st.text_input(
            "Nhập câu hỏi về tài liệu:",
            placeholder="Ví dụ: Nội dung chính của tài liệu là gì?"
        )

        if user_input:
            with st.spinner("🔍 Đang tìm câu trả lời..."):
                rag_chain = create_rag_chain(
                    st.session_state.llm,
                    st.session_state.retriever,
                    user_input
                )
                response = ask_question(rag_chain, user_input)
            # Trích xuất nguồn thông tin từ response
            sources = extract_sources(response)
            display_sources(sources)
            # Hiển thị câu trả lời
            st.markdown("### 💬 Câu Trả Lời")
            st.markdown(f"""
            <div class="response-box">
                {response["answer"]}
            </div>
            """, unsafe_allow_html=True)
            add_to_chat_history(user_input, response["answer"])
    else:
        st.info("👆 Hãy upload tài liệu trước khi đặt câu hỏi.")

    