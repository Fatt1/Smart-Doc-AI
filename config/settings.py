LLM_MODEL="qwen2.5:14b" 
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
EMBEDDING_DEVICE = "cuda" 
CHUNK_SIZE = 1000                    # Mỗi chunk tối đa 1000 ký tự
CHUNK_OVERLAP = 100                  # 100 ký tự trùng lặp giữa các chunks

# --- Retriever Configuration ---
SEARCH_TYPE = "similarity"           # Kiểu tìm kiếm (similarity hoặc mmr)
TOP_K = 3                            # Số chunks trả về

# --- LLM Configuration ---
TEMPERATURE = 0.3                    # Giảm để model tuân thủ prompt chặt hơn, ít lẫn ngôn ngữ
TOP_P = 0.9                          # Nucleus sampling

# --- UI Colors ---
PRIMARY_COLOR = "#007BFF"
SECONDARY_COLOR = "#FFC107"
BACKGROUND_COLOR = "#F8F9FA"
SIDEBAR_BG = "#2C2F33"
TEXT_COLOR = "#212529"


# --- Supported File Types ---
SUPPORTED_EXTENSIONS = [".pdf", ".docx"]