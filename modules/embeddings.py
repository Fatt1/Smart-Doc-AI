# Module này chuyển văn bản thành vector số (embedding)
# Để máy tính có thể "so sánh" độ giống nhau giữa các đoạn text
from langchain_community.embeddings import HuggingFaceEmbeddings
from config.settings import EMBEDDING_DEVICE, EMBEDDING_MODEL

def create_embedder():
    """
    Tạo embedding model.

    Giải thích cho người mới:
        Model "paraphrase-multilingual-mpnet-base-v2":
        - "multilingual" = hỗ trợ 50+ ngôn ngữ (bao gồm tiếng Việt)
        - "mpnet" = kiến trúc mạng neural (tốt hơn BERT)
        - "base" = kích thước trung bình (cân bằng tốc độ & chất lượng)
        - Mỗi đoạn text → vector 768 chiều (768 con số)

        device="cuda": Dùng GPU NVIDIA để tính toán
        → Nhanh hơn CPU 5-10 lần cho embedding!

        normalize_embeddings=True: Chuẩn hóa vector
        → Giúp so sánh cosine similarity chính xác hơn
    """
    embedder = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": EMBEDDING_DEVICE},
        encode_kwargs={"normalize_embeddings": True}
     )
    return embedder