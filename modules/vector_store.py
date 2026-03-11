# Module này quản lý FAISS Vector Database
# Lưu trữ vectors và tìm kiếm các chunks liên quan

from langchain_community.vectorstores import FAISS
from config.settings import SEARCH_TYPE, TOP_K

def create_vector_store(chunks, embedder):
    """
    Tạo FAISS vector store từ các chunks đã embedding.

    Tham số:
        chunks: List[Document] — các đoạn text đã chia nhỏ
        embedder: HuggingFaceEmbeddings — model tạo vector

    Giải thích cho người mới:
        FAISS.from_documents() làm 2 việc:
        1. Chuyển mỗi chunk thành vector (dùng embedder)
        2. Lưu tất cả vectors vào database FAISS

        Hình dung: Bạn có 100 đoạn văn → 100 vectors → lưu vào "kho"
    """
    vector_store = FAISS.from_documents(chunks, embedder)
  
    return vector_store

def get_retriever(vector_store: FAISS, search_type=None, top_k=None):
    """
    Tạo retriever từ vector store.

    Giải thích cho người mới:
        Retriever = "người tìm kiếm"
        Khi có câu hỏi, retriever sẽ:
        1. Chuyển câu hỏi thành vector
        2. Tìm trong FAISS những vector gần nhất
        3. Trả về top_k chunks liên quan nhất

        search_type="similarity": So sánh khoảng cách vector đơn thuần
        search_type="mmr": Maximum Marginal Relevance
            → Trả về kết quả vừa liên quan vừa đa dạng (không bị trùng lặp)
    """
    retriever = vector_store.as_retriever(search_type=search_type or SEARCH_TYPE, 
                                          search_kwargs={"k": top_k or TOP_K})
    return retriever

