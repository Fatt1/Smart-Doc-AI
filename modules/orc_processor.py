import pytesseract
from pdf2image import convert_from_path
from langchain.schema import Document
from PIL import ImageFilter, ImageEnhance
def ocr_pdf(pdf_path:str, lang="viet+eng"):
    """
    Dùng OCR để đọc chữ từ file PDF dạng hình ảnh
    Args:
        pdf_path (str): Đường dẫn đến file PDF
        lang (str): Ngôn ngữ để nhận diện, mặc định là tiếng Việt và tiếng Anh
     Trả về:
        List[Document]: Danh sách Document objects (giống PDFPlumberLoader)
         Giải thích cho người mới:
        Bước 1: pdf2image chuyển mỗi TRANG PDF → 1 ảnh PNG
                (giống chụp screenshot từng trang)

        Bước 2: pytesseract đọc chữ từ mỗi ảnh
                (giống Google Lens đọc chữ từ ảnh)

        Bước 3: Gom text lại thành Document objects
                (giống format của PDFPlumberLoader để code phía sau không cần thay đổi)

        dpi=300: Độ phân giải ảnh. 300 = rõ nét, OCR chính xác
                 Tăng lên 400 nếu chữ nhỏ/mờ, nhưng sẽ chậm hơn
    """
    documents = []
    # Bước 1: Chuyển PDF → Ảnh
    images = convert_from_path(pdf_path, dpi=300)
    for page_num, image in enumerate(images):
        # Bước 2: OCR đọc chữ từ ảnh
        text = pytesseract.image_to_string(image, lang=lang)
        if text.strip(): # Chỉ thêm nếu có chữ (tránh trang trắng)
             # Bước 3: Gom text thành Document object
            doc = Document(page_content=text,
                           metadata={
                               "source": pdf_path,
                               "page": page_num,
                               "loader": "OCR (Tesseract)" # Đánh dấu đã dùng OCR
                           })
            documents.append(doc)
    return documents

def ocr_pdf_with_preprocessing(pdf_path:str, lang="viet+eng") -> list[Document]:
    """
    OCR nâng cao: tiền xử lý ảnh trước khi OCR để tăng độ chính xác.

    Giải thích cho người mới:
        Ảnh scan thường bị:
        - Mờ, nhòe → OCR đọc sai
        - Nghiêng → OCR đọc lộn xộn
        - Nền xám/vàng → OCR lẫn chữ với nền

        Tiền xử lý = "chỉnh sửa ảnh" trước khi OCR đọc:
        - Chuyển sang đen trắng (grayscale) → dễ phân biệt chữ và nền
        - Tăng contrast → chữ rõ hơn
        - Binarization → pixel chỉ có đen/trắng, không có xám
    """
    documents = []
    images = convert_from_path(pdf_path, dpi=300)
    for page_num, image in enumerate(images):
        # Tiền xử lý ảnh
        # 1. Chuyển sang grayscale (đen trắng)
        image = image.convert("L")
        # 2. Tăng contrast (Độ tương phản)
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2)  # Tăng gấp đôi contrast

        # 3. Sharpen (Làm nét)
        image = image.filter(ImageFilter.SHARPEN)

        #OCR đọc chữ từ ảnh đã được xử lý
        text = pytesseract.image_to_string(image, lang=lang)
        if(text.strip()):
            doc = Document(page_content=text,
                           metadata={
                               "source": pdf_path,
                               "page": page_num,
                               "loader": "OCR with Preprocessing (Tesseract)"
                           })
            documents.append(doc)
    return documents
    