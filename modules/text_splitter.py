# Module này chia văn bản dài thành các đoạn nhỏ (chunks)
# Tại sao? Vì LLM có giới hạn token, không thể đọc cả quyển sách trong một lần.
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP
from langchain_core.documents import Document
def split_documents(documents, chunk_size=None, chunk_overlap=None) -> list[Document]:
    """
    Chia documents thành các chunks nhỏ hơn.

    Tham số:
        documents: List[Document] từ document_loader
        chunk_size: Kích thước mỗi chunk (mặc định từ settings)
        chunk_overlap: Độ trùng lặp giữa chunks

    Giải thích cho người mới:
        Tưởng tượng bạn có 1 bài văn 10 trang.
        chunk_size=1000 → chia mỗi đoạn ~1000 ký tự
        chunk_overlap=100 → 100 ký tự cuối đoạn 1 = 100 ký tự đầu đoạn 2

        Tại sao cần overlap?
        Ví dụ: "Hà Nội là thủ đô | của Việt Nam" (chia ở dấu |)
        Không overlap → đoạn 1: "Hà Nội là thủ đô", đoạn 2: "của Việt Nam"
        Có overlap → đoạn 1: "Hà Nội là thủ đô của", đoạn 2: "thủ đô của Việt Nam"
        → Không mất nghĩa!
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size or CHUNK_SIZE,
        chunk_overlap=chunk_overlap or CHUNK_OVERLAP
        # RecursiveCharacterTextSplitter chia theo thứ tự ưu tiên:
        # 1. Chia theo "\n\n" (paragraph) trước
        # 2. Nếu vẫn quá dài, chia theo "\n" (dòng)
        # 3. Nếu vẫn quá dài, chia theo " " (khoảng trắng)
        # 4. Cuối cùng mới chia theo ký tự
        # → Giữ được cấu trúc văn bản tốt nhất!
    )
    chunks = text_splitter.split_documents(documents)
    return chunks
