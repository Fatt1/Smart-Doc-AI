# Module này chịu trách nhiệm ĐỌC nội dung từ file
# Hỗ trợ: PDF (pdfplumber), PDF scan (OCR), DOCX (python-docx)
# Chế độ OCR do user chọn trên giao diện (không auto-detect)
import os
import tempfile
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.document_loaders import Docx2txtLoader
from modules.orc_processor import ocr_pdf, ocr_pdf_with_preprocessing

def load_document(uploaded_file, use_ocr=False):
    """
    Đọc nội dung từ file upload (PDF hoặc DOCX).

    Tham số:
        uploaded_file: File từ st.file_uploader() của Streamlit
        use_ocr: True nếu user chọn tab OCR trên giao diện
                 False nếu user chọn tab đọc thường (mặc định)

    Trả về:
        List[Document]: Danh sách các trang/đoạn văn bản

    Giải thích cho người mới:
        - use_ocr=False (mặc định): Dùng PDFPlumber đọc text trực tiếp
          → Nhanh, chính xác cho PDF tạo từ Word/LaTeX
        - use_ocr=True (user bật OCR): Dùng Tesseract OCR
          → Chậm hơn nhưng đọc được PDF toàn hình ảnh (scan)

        User tự chọn trên giao diện, code KHÔNG tự detect.
        Lý do: User biết rõ file của mình là PDF text hay scan,
        việc auto-detect đôi khi sai (PDF có cả text + hình).
    """
    # Lấy file mở rộng (pdf, docx)
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    #  Lưu file tạm trên ổ cứng
    # tempfile sẽ lưu vào thư mục tạm của hệ thống (C:\Users\...\AppData\Local\Temp trên Windows)
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        tmp_path = tmp_file.name # Lưu đường dẫn file tạm
    # File đã được đóng sau khi thoát khỏi with block
    try:
        if(file_extension == ".pdf"):
            if use_ocr:
                # Dùng OCR để đọc PDF scan
                documents = ocr_pdf_with_preprocessing(tmp_path)
            else:
                # Dùng PDFPlumber để đọc PDF text
                loader = PDFPlumberLoader(tmp_path)
                documents = loader.load()
        elif(file_extension == ".docx"):
            # Dùng Docx2txt để đọc DOCX
            loader = Docx2txtLoader(tmp_path)
            documents = loader.load()
            for i, doc in enumerate(documents):
                doc.metadata["source"] = f"{uploaded_file.name} - DOCX"
                doc.metadata["page"] =  {i+1}  # Đánh số trang từ 1
        else:
            raise ValueError("Định dạng file không được hỗ trợ. Vui lòng tải lên file PDF hoặc DOCX.")
        return documents
    finally:
        os.unlink(tmp_path) # Xóa file tạm sau khi đọc xong