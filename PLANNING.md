
## Plan: SmartDoc AI - Hướng dẫn từng bước cho người mới

Xây dựng hệ thống RAG (Retrieval-Augmented Generation) từ zero, vừa học Python vừa làm, chia thành 6 phase từ dễ đến khó. Mỗi bước có giải thích lý thuyết, code mẫu kèm chú thích, và giải thích thư viện.

---

### Phase 0: Chuẩn bị môi trường & Kiến thức nền tảng (2 ngày)

1. **Cài đặt công cụ cần thiết**
   - Cài Python 3.8+, VS Code, Git
   - Cài Ollama từ https://ollama.ai → pull model `qwen2.5:7b`
   - Tạo virtual environment (`python -m venv venv`)
   - Cài dependencies: `pip install streamlit langchain langchain-community faiss-cpu sentence-transformers pdfplumber`

2. **Học Python cơ bản cần thiết** (giải thích trong file .md)
   - List, Dictionary, Function, Class
   - `import` thư viện, `pip install`
   - File I/O, `with` statement
   - f-string formatting

3. **Hiểu các thư viện sẽ dùng** (giải thích vai trò từng thư viện)
   - `streamlit`: Tạo giao diện web nhanh bằng Python (thay thế HTML/CSS/JS)
   - `langchain`: Framework kết nối các bước từ load document → embedding → search → LLM
   - `faiss-cpu`: Thư viện tìm kiếm vector tốc độ cao của Facebook
   - `sentence-transformers`: Chuyển văn bản thành vector số (embedding)
   - `pdfplumber`: Đọc nội dung từ file PDF
   - `ollama`: Chạy model AI (Qwen2.5) trên máy local, không cần internet

---

### Phase 1: Xây dựng ứng dụng base (3-4 ngày)

4. **Tạo cấu trúc thư mục project**
   ```
   SmartDocAI/
   ├── app.py              # File chính
   ├── requirements.txt    # Danh sách thư viện
   ├── data/               # Thư mục chứa PDF mẫu
   └── README.md
   ```

5. **Viết `app.py` - Phần 1: Upload PDF & đọc nội dung**
   - Dùng `streamlit` tạo giao diện upload file
   - Dùng `PDFPlumberLoader` đọc text từ PDF
   - Giải thích: Document Loader là gì, tại sao cần extract text

6. **Viết `app.py` - Phần 2: Chia text thành chunks (Text Splitting)**
   - Dùng `RecursiveCharacterTextSplitter` với `chunk_size=1000`, `chunk_overlap=100`
   - Giải thích: Tại sao phải chia nhỏ (LLM có giới hạn token), overlap để không mất ngữ cảnh

7. **Viết `app.py` - Phần 3: Tạo Embedding & Vector Store**
   - Dùng `HuggingFaceEmbeddings` với model `paraphrase-multilingual-mpnet-base-v2`
   - Dùng `FAISS.from_documents()` tạo vector database
   - Giải thích: Embedding là gì (chuyển chữ → số), Vector DB là gì (kho chứa vector để tìm kiếm)

8. **Viết `app.py` - Phần 4: Kết nối LLM & RAG Chain**
   - Dùng `Ollama(model="qwen2.5:7b")` kết nối model
   - Tạo retriever, prompt template, RAG chain
   - Giải thích: RAG pipeline hoạt động thế nào (Query → Search → Context → LLM → Answer)

9. **Viết `app.py` - Phần 5: UI hoàn chỉnh với Streamlit**
   - Sidebar với hướng dẫn, màu sắc theo yêu cầu
   - Khu vực hỏi đáp chính
   - Spinner loading, error messages

10. **Kiểm tra base app hoạt động**
    - Upload PDF mẫu, đặt câu hỏi tiếng Việt & tiếng Anh
    - Verify: PDF load đúng, embedding tạo được, LLM trả lời đúng ngữ cảnh

---

### Phase 2: Câu hỏi 1-3 - Tính năng cơ bản (3-4 ngày)

11. **Câu hỏi 1: Hỗ trợ file DOCX** *(parallel với step 12)*
    - Cài thêm `python-docx` hoặc dùng `Docx2txtLoader` từ LangChain
    - Sửa phần upload để chấp nhận cả `.pdf` và `.docx`
    - Thêm logic phân nhánh: nếu PDF → `PDFPlumberLoader`, nếu DOCX → `Docx2txtLoader`
    - Giải thích: `python-docx` đọc file Word, `Docx2txtLoader` là wrapper LangChain cho nó

12. **Câu hỏi 2: Lưu trữ lịch sử hội thoại** *(parallel với step 11)*
    - Dùng `st.session_state` của Streamlit để lưu list `[{"question": ..., "answer": ...}]`
    - Hiển thị lịch sử dưới dạng chat bubbles trong sidebar
    - Giải thích: `session_state` là biến lưu trữ dữ liệu giữa các lần interact trên Streamlit

13. **Câu hỏi 3: Thêm nút xóa lịch sử** *(depends on step 12)*
    - Thêm `st.button("Clear History")` → xóa `st.session_state.chat_history`
    - Thêm `st.button("Clear Vector Store")` → xóa vector & reset
    - Dùng `st.dialog` hoặc `st.warning` làm confirmation dialog
    - Giải thích: Event handling trong Streamlit (mỗi lần click, app re-run)

---

### Phase 3: Câu hỏi 4-6 - Tính năng trung bình (5-6 ngày)

14. **Câu hỏi 4: Cải thiện chunk strategy**
    - Tạo UI cho phép chọn `chunk_size` (500/1000/1500/2000) và `chunk_overlap` (50/100/200)
    - Viết hàm test thử các tổ hợp, đo thời gian & chất lượng trả lời
    - Tạo bảng so sánh kết quả
    - Giải thích: Chunk nhỏ → chính xác hơn nhưng thiếu context; chunk lớn → nhiều context nhưng noise

15. **Câu hỏi 5: Citation/Source tracking** *(depends on step 14)*
    - Khi retriever trả về documents, lấy `metadata` (page number, source)
    - Hiển thị dưới câu trả lời: "Nguồn: Trang X, đoạn Y"
    - Dùng `st.expander` để show context gốc khi click
    - Giải thích: Mỗi document chunk trong LangChain có `.metadata` chứa thông tin nguồn

16. **Câu hỏi 6: Conversational RAG** *(depends on step 12)*
    - Dùng `ConversationBufferMemory` hoặc `ChatMessageHistory` từ LangChain
    - Tạo `ConversationalRetrievalChain` thay cho chain thường
    - LLM sẽ nhận cả lịch sử chat + context mới
    - Giải thích: Memory cho phép LLM nhớ câu hỏi trước → xử lý "nó" "cái đó" (follow-up questions)

---

### Phase 4: Câu hỏi 7-8 - Tìm kiếm nâng cao (4-5 ngày)

17. **Câu hỏi 7: Hybrid Search**
    - Cài thêm `rank-bm25`
    - Tạo `BM25Retriever` (keyword search) bên cạnh FAISS retriever (semantic search)
    - Dùng `EnsembleRetriever` kết hợp cả hai với trọng số (weights)
    - Giải thích: BM25 = tìm theo từ khóa chính xác; Vector = tìm theo nghĩa. Kết hợp cho kết quả tốt hơn

18. **Câu hỏi 8: Multi-document RAG** *(depends on step 17)*
    - Cho phép upload nhiều file cùng lúc (`st.file_uploader` với `accept_multiple_files=True`)
    - Thêm metadata cho mỗi document: `{"source": filename, "upload_date": ..., "type": ...}`
    - Tạo filter UI với `st.multiselect` để chọn document nào muốn search
    - Hiển thị câu trả lời kèm "Từ file: X"
    - Giải thích: Metadata filtering cho phép tìm kiếm theo điều kiện, không chỉ theo nội dung

---

### Phase 5: Câu hỏi 9-10 - Tính năng chuyên sâu (5-7 ngày)

19. **Câu hỏi 9: Re-ranking với Cross-Encoder**
    - Cài thêm `sentence-transformers` (đã có) với cross-encoder model
    - Sau khi FAISS trả về top-k results, dùng Cross-Encoder đánh giá lại relevance score
    - Sắp xếp lại kết quả theo score mới
    - Giải thích: Bi-encoder (hiện tại) encode riêng query & doc → nhanh nhưng kém chính xác; Cross-encoder encode cùng lúc → chậm hơn nhưng chính xác hơn

20. **Câu hỏi 10: Self-RAG**
    - Query Rewriting: LLM tự viết lại câu hỏi cho rõ ràng hơn trước khi search
    - Self-evaluation: LLM tự đánh giá câu trả lời (relevant? factual? complete?)
    - Multi-hop: Nếu 1 lần search chưa đủ, tự search lại với query mới
    - Confidence scoring: Hiển thị mức độ tin cậy của câu trả lời
    - Giải thích: Self-RAG là kỹ thuật LLM tự kiểm tra và cải thiện output

---

### Phase 6: Hoàn thiện & Nộp bài (2-3 ngày)

21. **Viết documentation**
    - README.md với hướng dẫn cài đặt, sử dụng
    - Comment code đầy đủ
    - Viết báo cáo theo template yêu cầu

22. **Testing**
    - Test tất cả 10 tính năng
    - Test edge cases: file rỗng, câu hỏi ngoài nội dung, file quá lớn
    - Ghi lại test cases và kết quả

23. **UI/UX Polish**
    - Áp dụng color palette theo yêu cầu
    - Error handling đầy đủ
    - Loading states, success/error notifications

---

### Relevant files cần tạo/sửa
- `SmartDocAI/app.py` — File chính chứa toàn bộ logic (base app + 10 câu hỏi)
- `SmartDocAI/requirements.txt` — Danh sách thư viện: `streamlit`, `langchain`, `langchain-community`, `faiss-cpu`, `sentence-transformers`, `pdfplumber`, `python-docx`, `rank-bm25`
- `SmartDocAI/README.md` — Documentation
- `SmartDocAI/data/` — Thư mục chứa PDF/DOCX mẫu để test

### Verification
1. **Base app**: Upload PDF → đặt câu hỏi → nhận câu trả lời đúng ngữ cảnh
2. **Q1**: Upload file `.docx` → hệ thống đọc được nội dung
3. **Q2**: Hỏi nhiều câu → lịch sử hiện trong sidebar
4. **Q3**: Click "Clear History" → lịch sử bị xóa (có confirm dialog)
5. **Q4**: Thay đổi chunk_size/overlap trên UI → kết quả thay đổi
6. **Q5**: Câu trả lời hiển thị "Nguồn: Trang X" + click expand xem context gốc
7. **Q6**: Hỏi "nó là gì?" sau câu hỏi trước → LLM hiểu ngữ cảnh
8. **Q7**: So sánh kết quả hybrid vs pure vector → hybrid tốt hơn cho keyword queries
9. **Q8**: Upload 2+ files → filter theo file → trả lời đúng nguồn
10. **Q9**: Kết quả re-ranking chính xác hơn khi so sánh với không re-ranking
11. **Q10**: Query rewriting cải thiện kết quả, có confidence score hiển thị
12. **Chạy `streamlit run app.py`** không có lỗi, tất cả features hoạt động

### Decisions
- Dùng **1 file `app.py`** cho đơn giản (có thể tách module sau nếu cần)
- Ưu tiên hoàn thành **Q1-Q6 trước** (chiếm phần lớn điểm, dễ hơn)
- Q7-Q10 là nâng cao, làm sau khi đã vững base
- File `.md` output sẽ chứa code mẫu kèm comment giải thích bằng tiếng Việt

### Further Considerations
1. **Máy tính cần đủ mạnh** để chạy Qwen2.5:7b (RAM >= 8GB, recommend 16GB). Nếu máy yếu, có thể dùng `qwen2.5:3b` thay thế.
2. **Thời gian**: ~25-30 ngày làm việc. Với deadline April 19, 2026 (còn ~43 ngày), cần bắt đầu ngay Phase 0-1.
3. **Có thể tách `app.py` thành modules** (`document_loader.py`, `rag_chain.py`, `ui.py`) để code sạch hơn — nhưng không bắt buộc, tùy bạn quyết định.

---

Bạn review plan này và cho tôi biết:
- Có muốn thêm/bớt nội dung gì không?
- Có muốn tập trung vào một số câu hỏi cụ thể (không làm hết 10)?
- Máy tính của bạn có đủ RAM (>= 8GB) để chạy model Qwen2.5:7b không?

Sau khi bạn approve, tôi sẽ tạo file `.md` hoàn chỉnh với đầy đủ code mẫu, giải thích lý thuyết, và hướng dẫn từng bước.

User: có thể tách module thành các module nhỏ hơn để dễ quản lý. 
Máy tính của tôi đủ RAM 40gb ram thì nên chạy model nào
Máy tôi có card màn hình nvia để có thể chạy cuda
Sau khi nhận câu trả lời của tôi thì bắt đầu viết file md đi

GitHub Copilot: Read [](file:///e%3A/PTMNM)

Read [](file:///e%3A/PTMNM/Project-LLMs-Rag-Agent)

Tôi không có công cụ tạo file trực tiếp trong workspace. Tôi sẽ in ra toàn bộ nội dung file `.md` để bạn copy và tạo file. Với cấu hình 40GB RAM + NVIDIA GPU:

- **Nên chạy `qwen2.5:14b`** — chất lượng tiếng Việt tốt hơn hẳn 7b, máy bạn dư sức chạy
- Dùng `device='cuda'` cho embedding để tăng tốc

Cập nhật plan với module tách nhỏ và tạo file .md ngay: 

Updated memory file [](file:///c%3A/Users/phat3/AppData/Roaming/Code/User/workspaceStorage/7e43ec77a8314cdb4bcbd94986641461/GitHub.copilot-chat/memory-tool/memories/MGExNDQ4OTUtNDkzMi00ZGI5LWEyNmYtZDBmZDUwYTUxZGQ2/plan.md)

Dưới đây là toàn bộ nội dung file `.md`. Hãy tạo file `e:\PTMNM\Project-LLMs-Rag-Agent\PLANNING.md` và paste nội dung này vào:

```markdown
# 📘 SmartDoc AI - Kế Hoạch Phát Triển & Hướng Dẫn Học

> **Dành cho**: Người mới học Python, vừa học vừa làm project
> **Deadline**: April 19, 2026
> **Cấu hình máy**: 40GB RAM, NVIDIA GPU (CUDA)
> **Model khuyến nghị**: `qwen2.5:14b` (chất lượng tiếng Việt xuất sắc, máy dư sức chạy)

---

## Mục Lục

- [Tổng Quan Project](#tổng-quan-project)
- [Giải Thích Các Thư Viện](#giải-thích-các-thư-viện)
- [Cấu Trúc Thư Mục (Tách Module)](#cấu-trúc-thư-mục-tách-module)
- [Phase 0: Chuẩn Bị Môi Trường](#phase-0-chuẩn-bị-môi-trường-2-ngày)
- [Phase 1: Xây Dựng Base App](#phase-1-xây-dựng-base-app-4-5-ngày)
- [Phase 2: Câu Hỏi 1-3 (Cơ bản)](#phase-2-câu-hỏi-1-3--tính-năng-cơ-bản-3-4-ngày)
- [Phase 3: Câu Hỏi 4-6 (Trung bình)](#phase-3-câu-hỏi-4-6--tính-năng-trung-bình-5-6-ngày)
- [Phase 4: Câu Hỏi 7-8 (Nâng cao)](#phase-4-câu-hỏi-7-8--tìm-kiếm-nâng-cao-4-5-ngày)
- [Phase 5: Câu Hỏi 9-10 (Chuyên sâu)](#phase-5-câu-hỏi-9-10--tính-năng-chuyên-sâu-5-7-ngày)
- [Phase 6: Hoàn Thiện & Nộp Bài](#phase-6-hoàn-thiện--nộp-bài-2-3-ngày)
- [Checklist Kiểm Tra](#checklist-kiểm-tra)

---

## Tổng Quan Project

**SmartDoc AI** là hệ thống hỏi đáp tài liệu thông minh dựa trên kỹ thuật **RAG (Retrieval-Augmented Generation)**:

```
Người dùng upload PDF/DOCX
        ↓
Hệ thống đọc & chia nhỏ văn bản (chunks)
        ↓
Chuyển chunks thành vector số (embedding)
        ↓
Lưu vào Vector Database (FAISS)
        ↓
Người dùng đặt câu hỏi
        ↓
Tìm chunks liên quan nhất (similarity search)
        ↓
Gửi context + câu hỏi cho LLM (Qwen2.5:14b)
        ↓
LLM sinh câu trả lời → hiển thị cho người dùng
```

### RAG là gì? (Giải thích đơn giản)

Hãy tưởng tượng bạn đang thi mở sách:
- **Retrieval** = Mở sách tìm trang liên quan đến câu hỏi
- **Generation** = Đọc trang đó rồi viết câu trả lời bằng lời của mình

```python
# Công thức RAG đơn giản:
def rag(cau_hoi):
    # Bước 1: Tìm thông tin liên quan từ tài liệu
    thong_tin = tim_kiem(cau_hoi)  # Retrieval

    # Bước 2: Dùng AI sinh câu trả lời dựa trên thông tin tìm được
    cau_tra_loi = ai_tra_loi(cau_hoi, thong_tin)  # Generation

    return cau_tra_loi
```

---

## Giải Thích Các Thư Viện

### Thư viện chính

| Thư viện | Vai trò | Ví dụ dễ hiểu |
|----------|---------|----------------|
| `streamlit` | Tạo giao diện web bằng Python | Thay vì viết HTML/CSS/JS, bạn chỉ cần `st.button("Click")` |
| `langchain` | Framework kết nối tất cả bước RAG | Như "ống nước" nối các bước lại với nhau |
| `faiss-cpu` / `faiss-gpu` | Tìm kiếm vector siêu nhanh (Facebook) | Như Google Search nhưng cho vector số |
| `sentence-transformers` | Chuyển văn bản → vector số | Như dịch tiếng Việt → "ngôn ngữ toán học" |
| `pdfplumber` | Đọc nội dung từ file PDF | Như mở PDF và copy text ra |
| `ollama` | Chạy model AI trên máy local | Như cài ChatGPT trên máy mình |
| `pytesseract` | OCR — nhận diện chữ từ ảnh | Như người đọc chữ từ ảnh chụp tài liệu |
| `pdf2image` | Chuyển trang PDF thành ảnh | Như chụp ảnh từng trang PDF để OCR đọc |
### Thư viện bổ sung (cho các câu hỏi nâng cao)

| Thư viện | Câu hỏi | Vai trò |
|----------|---------|---------|
| `python-docx` | Q1 | Đọc file Word (.docx) |
| `rank-bm25` | Q7 | Tìm kiếm theo từ khóa (keyword search) |
| `sentence-transformers` (cross-encoder) | Q9 | Đánh giá lại mức độ liên quan chính xác hơn |

### Embedding là gì? (Giải thích cho người mới)

```python
# Embedding = chuyển chữ thành số để máy tính "hiểu" được

# Ví dụ đơn giản (thực tế phức tạp hơn nhiều):
"con mèo"  → [0.2, 0.8, 0.1, ...]   # vector 768 số
"con chó"  → [0.3, 0.7, 0.2, ...]   # gần với "con mèo" vì cùng là động vật
"chiếc xe" → [0.9, 0.1, 0.8, ...]   # xa với "con mèo" vì khác nghĩa

# Khoảng cách giữa các vector cho biết mức độ liên quan:
# "con mèo" và "con chó" → khoảng cách NHỎ (liên quan)
# "con mèo" và "chiếc xe" → khoảng cách LỚN (không liên quan)
```

### FAISS là gì?

```python
# FAISS = Facebook AI Similarity Search
# Là "kho chứa" vector và công cụ tìm kiếm cực nhanh

# Hình dung: Bạn có 1000 đoạn văn, mỗi đoạn được chuyển thành vector
# Khi có câu hỏi, FAISS tìm ra đoạn nào "gần" nhất với câu hỏi
# → Đó là đoạn liên quan nhất để trả lời

# Tìm top 3 đoạn liên quan nhất
retriever = vector_store.as_retriever(search_kwargs={"k": 3})
```

### LangChain là gì?

```python
# LangChain = Framework kết nối các bước
# Giống như lắp ráp LEGO: mỗi mảnh là 1 bước, LangChain nối chúng lại

# Không có LangChain (phải tự viết từng bước):
text = doc_nuoc_pdf(file)
chunks = chia_nho(text)
vectors = tao_embedding(chunks)
ket_qua = tim_kiem(vectors, cau_hoi)
tra_loi = goi_llm(ket_qua, cau_hoi)

# Có LangChain (tự động nối các bước):
chain = load_doc | split | embed | retrieve | llm
tra_loi = chain.invoke(cau_hoi)  # 1 dòng code!
```

---

## Cấu Trúc Thư Mục (Tách Module)

```
Project-LLMs-Rag-Agent/
│
├── app.py                     # Entry point - chạy Streamlit app
├── requirements.txt           # Danh sách thư viện
├── README.md                  # Hướng dẫn sử dụng
├── PLANNING.md                # File này
│
├── config/
│   └── settings.py            # Cấu hình: model name, chunk size, colors...
│
├── modules/
│   ├── __init__.py            # File rỗng, đánh dấu đây là Python package
│   ├── ocr_processor.py       # OCR cho PDF dạng hình ảnh (scanned PDF)
│   ├── document_loader.py     # Load PDF, DOCX
│   ├── text_splitter.py       # Chia text thành chunks
│   ├── embeddings.py          # Tạo embedding vectors
│   ├── vector_store.py        # Quản lý FAISS vector database
│   ├── llm_chain.py           # Kết nối LLM và RAG chain
│   ├── prompt_templates.py    # Các prompt template
│   ├── chat_history.py        # Quản lý lịch sử chat (Q2, Q3)
│   ├── citation.py            # Source tracking (Q5)
│   ├── hybrid_search.py       # Hybrid search (Q7)
│   ├── reranker.py            # Cross-encoder re-ranking (Q9)
│   └── self_rag.py            # Self-RAG logic (Q10)
│
├── ui/
│   ├── __init__.py
│   ├── sidebar.py             # Giao diện sidebar
│   ├── main_page.py           # Giao diện trang chính
│   ├── styles.py              # CSS custom styles
│   └── components.py          # UI components tái sử dụng
│
├── data/                      # Thư mục chứa file mẫu
│   └── sample.pdf
│
└── tests/                     # Test cases
    ├── test_loader.py
    ├── test_splitter.py
    └── test_rag.py
```

### Tại sao tách module?

```python
# KHÔNG tách module (app.py dài 500+ dòng — khó đọc, khó sửa):
# app.py chứa TẤT CẢ: UI + load PDF + embedding + LLM + ...

# CÓ tách module (mỗi file 50-100 dòng — dễ hiểu, dễ sửa):
# Muốn sửa cách load PDF? → Vào document_loader.py
# Muốn đổi model? → Vào settings.py
# Muốn sửa giao diện? → Vào ui/

# Cách import module trong Python:
from modules.document_loader import load_document
from modules.embeddings import create_embedder
from config.settings import CHUNK_SIZE, MODEL_NAME
```

---

## Phase 0: Chuẩn Bị Môi Trường (2 ngày)

### Bước 0.1: Cài đặt Python & công cụ

```bash
# Kiểm tra Python đã cài chưa
python --version
# Cần Python 3.8+ (khuyên dùng 3.10 hoặc 3.11)

# Kiểm tra pip
pip --version
```

### Bước 0.2: Cài đặt Ollama & Model

```bash
# 1. Tải Ollama từ: https://ollama.ai
# 2. Cài đặt xong, mở terminal:

# Pull model Qwen2.5:14b (khuyên dùng vì máy 40GB RAM + GPU)
ollama pull qwen2.5:14b

# Kiểm tra model đã tải:
ollama list

# Test thử model:
ollama run qwen2.5:14b "Xin chào, bạn là ai?"
```

> **Tại sao `qwen2.5:14b` mà không phải `7b`?**
> - Máy bạn có 40GB RAM + NVIDIA GPU → dư sức chạy 14b
> - Model 14b trả lời tiếng Việt tốt hơn 7b rõ rệt
> - Reasoning (suy luận) mạnh hơn → câu trả lời chính xác hơn
> - Nếu muốn nhanh hơn nữa, dùng `qwen2.5:7b` cũng OK

### Bước 0.3: Tạo project & virtual environment

```bash
# Di chuyển đến thư mục project
cd e:\PTMNM\Project-LLMs-Rag-Agent

# Tạo virtual environment (môi trường ảo)
python -m venv venv

# Kích hoạt virtual environment (Windows)
venv\Scripts\activate

# Khi thấy (venv) ở đầu dòng → đã kích hoạt thành công
```

> **Virtual environment là gì?**
> Giống như tạo 1 "phòng riêng" cho project.
> Các thư viện cài trong đây không ảnh hưởng đến các project khác.

### Bước 0.4: Tạo `requirements.txt` & cài thư viện

```txt
# requirements.txt
streamlit==1.41.1
langchain==0.3.16
langchain-community==0.3.16
langchain-text-splitters==0.3.4
faiss-gpu==1.7.2
sentence-transformers==3.3.1
pytesseract==0.3.13
pdf2image==1.17.0
Pillow==11.1.0
pdfplumber==0.11.4
python-docx==1.1.2
rank-bm25==0.2.2
torch==2.5.1
transformers==4.47.1
numpy==1.26.4
pandas==2.2.3
```

```bash
# Cài tất cả thư viện
pip install -r requirements.txt
### Bước 0.4b: Cài đặt Tesseract-OCR (cho scan PDF)

```bash
# Tesseract là phần mềm OCR của Google — cần cài RIÊNG (không cài bằng pip được)

# === Windows ===
# 1. Tải installer từ: https://github.com/UB-Mannheim/tesseract/wiki
# 2. Chạy installer, chọn thêm ngôn ngữ Vietnamese (vie) khi cài
# 3. Mặc định cài vào: C:\Program Files\Tesseract-OCR
# 4. QUAN TRỌNG: Thêm vào PATH hoặc cấu hình trong code

# Kiểm tra đã cài thành công:
tesseract --version
```

> **Tesseract-OCR là gì?**
> - Là phần mềm nhận diện chữ từ hình ảnh (OCR = Optical Character Recognition)
> - Giống như khi bạn chụp ảnh trang sách → app đọc chữ ra cho bạn
> - `pytesseract` là thư viện Python "gọi" Tesseract, nhưng Tesseract phải cài riêng
> - Hỗ trợ tiếng Việt (cần tải thêm language data `vie`)

```python
# Giải thích flow OCR:
# PDF scan (toàn hình ảnh, không copy được chữ)
#     ↓
# pdf2image: Chuyển mỗi trang PDF → ảnh PNG
#     ↓
# pytesseract: Đọc chữ từ ảnh → text
#     ↓
# Text bình thường → tiếp tục chunking, embedding như PDF thường
```
```

> **Lưu ý**: Dùng `faiss-gpu` thay vì `faiss-cpu` vì máy có NVIDIA GPU.
> Nếu `faiss-gpu` lỗi, fallback về `faiss-cpu`.

### Bước 0.5: Kiến thức Python cần biết

```python
# 1. LIST (danh sách) — dùng để chứa nhiều phần tử
fruits = ["táo", "cam", "xoài"]
fruits.append("nho")       # Thêm phần tử
print(fruits[0])           # Lấy phần tử đầu: "táo"

# 2. DICTIONARY (từ điển) — dùng để chứa cặp key-value
student = {
    "name": "An",
    "age": 20,
    "score": 8.5
}
print(student["name"])     # "An"

# 3. FUNCTION (hàm) — đóng gói code để tái sử dụng
def chao(ten):
    return f"Xin chào {ten}!"

print(chao("An"))          # "Xin chào An!"

# 4. IMPORT — dùng thư viện/module khác
import os                           # Thư viện có sẵn
from modules.document_loader import load_document  # Module tự tạo

# 5. CLASS (lớp) — bản thiết kế cho object (sẽ gặp khi dùng LangChain)
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} says hello!"

cat = Animal("Mèo")
print(cat.speak())         # "Mèo says hello!"

# 6. WITH statement — tự động đóng file sau khi dùng xong
with open("file.txt", "r") as f:
    content = f.read()
# File tự động đóng khi ra khỏi block with
```

---

## Phase 1: Xây Dựng Base App (4-5 ngày)

### Bước 1.1: Tạo file cấu hình `config/settings.py`

```python
# config/settings.py
# ====================================================
# File cấu hình trung tâm — thay đổi settings ở đây
# thay vì phải sửa nhiều file khác nhau
# ====================================================

# --- Model Configuration ---
LLM_MODEL = "qwen2.5:14b"           # Model AI chính (máy 40GB RAM)
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
EMBEDDING_DEVICE = "cuda"            # Dùng GPU NVIDIA để tăng tốc (thay vì "cpu")

# --- Chunk Configuration ---
CHUNK_SIZE = 1000                    # Mỗi chunk tối đa 1000 ký tự
CHUNK_OVERLAP = 100                  # 100 ký tự trùng lặp giữa các chunks

# --- Retriever Configuration ---
SEARCH_TYPE = "similarity"           # Kiểu tìm kiếm (similarity hoặc mmr)
TOP_K = 3                            # Số chunks trả về

# --- LLM Configuration ---
TEMPERATURE = 0.7                    # Mức sáng tạo (0=chính xác, 1=sáng tạo)
TOP_P = 0.9                          # Nucleus sampling

# --- UI Colors ---
PRIMARY_COLOR = "#007BFF"
SECONDARY_COLOR = "#FFC107"
BACKGROUND_COLOR = "#F8F9FA"
SIDEBAR_BG = "#2C2F33"
TEXT_COLOR = "#212529"

# --- Supported File Types ---
SUPPORTED_EXTENSIONS = [".pdf", ".docx"]
```

> **Tại sao cần file settings?**
> Thay vì viết `chunk_size=1000` rải rác khắp nơi trong code,
> bạn chỉ cần thay đổi 1 chỗ trong `settings.py` là tất cả đều cập nhật.

### Bước 1.2: Document Loader — `modules/document_loader.py`

```python
# modules/document_loader.py
# ====================================================
# Module này chịu trách nhiệm ĐỌC nội dung từ file
# Hỗ trợ: PDF (pdfplumber) và DOCX (python-docx)
# ====================================================

import os
import tempfile
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.document_loaders import Docx2txtLoader


### Bước 1.2b: OCR Processor — `modules/ocr_processor.py`


# modules/ocr_processor.py
# ====================================================
# Module xử lý OCR cho PDF dạng hình ảnh (scanned PDF)
# Khi PDFPlumber không đọc được text → dùng OCR nhận diện chữ từ ảnh
# ====================================================

import os
import pytesseract
from pdf2image import convert_from_path
from langchain.schema import Document

# === CẤU HÌNH TESSERACT (Windows) ===
# Nếu Tesseract không nằm trong PATH, chỉ định đường dẫn thủ công:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def is_scanned_pdf(documents):
    """
    Kiểm tra xem PDF có phải dạng scan (hình ảnh) hay không.

    Giải thích cho người mới:
        PDF có 2 loại:
        1. PDF text: Tạo từ Word, LaTeX... → có text, copy được
        2. PDF scan: Chụp/scan tài liệu giấy → toàn hình ảnh, KHÔNG copy được

        Cách phát hiện: Nếu PDFPlumber đọc ra text rỗng hoặc rất ít text
        → khả năng cao là PDF scan → cần dùng OCR

        Ví dụ thực tế:
        - Bài giảng thầy/cô scan từ sách → PDF scan
        - File luận văn xuất từ Word → PDF text
    """
    if not documents:
        return True

    # Gộp tất cả text từ các trang
    total_text = "".join(doc.page_content.strip() for doc in documents)

    # Nếu tổng text quá ngắn (< 50 ký tự) → coi như scan
    # 50 là ngưỡng an toàn: PDF thật sẽ có ít nhất vài trăm ký tự
    return len(total_text) < 50


def ocr_pdf(pdf_path, lang="vie+eng"):
    """
    Dùng OCR để đọc chữ từ PDF dạng hình ảnh.

    Tham số:
        pdf_path: Đường dẫn file PDF
        lang: Ngôn ngữ OCR
              "vie" = tiếng Việt
              "eng" = tiếng Anh
              "vie+eng" = cả hai (khuyên dùng cho tài liệu VN)

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

    # Bước 1: Chuyển PDF → danh sách ảnh (mỗi trang = 1 ảnh)
    # dpi=300: Đủ rõ cho OCR. Nếu chữ quá nhỏ, tăng lên 400
    images = convert_from_path(pdf_path, dpi=300)

    for page_num, image in enumerate(images):
        # Bước 2: OCR — đọc chữ từ ảnh
        text = pytesseract.image_to_string(image, lang=lang)

        # Bước 3: Tạo Document object (giống format của PDFPlumberLoader)
        if text.strip():  # Chỉ thêm nếu có text
            doc = Document(
                page_content=text.strip(),
                metadata={
                    "source": pdf_path,
                    "page": page_num,
                    "loader": "OCR (Tesseract)",  # Đánh dấu đã dùng OCR
                }
            )
            documents.append(doc)

    return documents


def ocr_pdf_with_preprocessing(pdf_path, lang="vie+eng"):
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
    from PIL import ImageFilter, ImageEnhance

    documents = []
    images = convert_from_path(pdf_path, dpi=300)

    for page_num, image in enumerate(images):
        # Tiền xử lý ảnh
        # 1. Chuyển sang grayscale (đen trắng)
        image = image.convert("L")

        # 2. Tăng contrast (độ tương phản)
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)  # 2.0 = tăng gấp đôi contrast

        # 3. Sharpen (làm nét)
        image = image.filter(ImageFilter.SHARPEN)

        # OCR
        text = pytesseract.image_to_string(image, lang=lang)

        if text.strip():
            doc = Document(
                page_content=text.strip(),
                metadata={
                    "source": pdf_path,
                    "page": page_num,
                    "loader": "OCR (Tesseract + Preprocessing)",
                }
            )
            documents.append(doc)

    return documents
```

> **Khi nào dùng `ocr_pdf` vs `ocr_pdf_with_preprocessing`?**
> - `ocr_pdf`: PDF scan chất lượng tốt (scan máy, ảnh rõ nét)
> - `ocr_pdf_with_preprocessing`: PDF scan chất lượng kém (chụp bằng điện thoại, mờ, nghiêng)
> - Mặc định dùng `ocr_pdf_with_preprocessing` cho kết quả tốt hơn


def load_document(uploaded_file):
    """
    Đọc nội dung từ file upload (PDF hoặc DOCX).

    Tham số:
        uploaded_file: File từ st.file_uploader() của Streamlit

    Trả về:
        List[Document]: Danh sách các trang/đoạn văn bản

    Giải thích cho người mới:
        - Streamlit upload file vào RAM (bộ nhớ), không lưu vào ổ cứng
        - Nhưng PDFPlumberLoader cần đường dẫn file trên ổ cứng
        - Nên ta phải: RAM → tạo file tạm trên ổ cứng → đọc → xóa file tạm
    """
    # Lấy phần mở rộng file (.pdf hoặc .docx)
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()

    # Tạo file tạm thời trên ổ cứng
    # delete=False: không xóa ngay, ta sẽ tự xóa sau
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp:
        tmp.write(uploaded_file.getbuffer())  # Ghi nội dung vào file tạm
        tmp_path = tmp.name                   # Lưu đường dẫn file tạm

    try:
        # Chọn loader phù hợp dựa trên loại file
        if file_extension == ".pdf":
            loader = PDFPlumberLoader(tmp_path)
        elif file_extension == ".docx":
            loader = Docx2txtLoader(tmp_path)
        else:
            raise ValueError(f"Không hỗ trợ file {file_extension}")

        # Đọc nội dung → trả về list các Document objects
        documents = loader.load()
        return documents

    finally:
        # Luôn xóa file tạm sau khi đọc xong (dù có lỗi hay không)
        os.unlink(tmp_path)
```

> **Giải thích `Document` object:**
> ```python
> # Mỗi Document có 2 phần:
> doc.page_content  # Nội dung text: "Chương 1: Giới thiệu..."
> doc.metadata      # Thông tin thêm: {"source": "file.pdf", "page": 0}
> ```

### Bước 1.3: Text Splitter — `modules/text_splitter.py`

```python
# modules/text_splitter.py
# ====================================================
# Module này chia văn bản dài thành các đoạn nhỏ (chunks)
# Tại sao? Vì LLM có giới hạn token, không thể đọc cả quyển sách
# ====================================================

from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP


def split_documents(documents, chunk_size=None, chunk_overlap=None):
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
        chunk_overlap=chunk_overlap or CHUNK_OVERLAP,
        # RecursiveCharacterTextSplitter chia theo thứ tự ưu tiên:
        # 1. Chia theo "\n\n" (paragraph) trước
        # 2. Nếu vẫn quá dài, chia theo "\n" (dòng)
        # 3. Nếu vẫn quá dài, chia theo " " (khoảng trắng)
        # 4. Cuối cùng mới chia theo ký tự
        # → Giữ được cấu trúc văn bản tốt nhất!
    )

    chunks = text_splitter.split_documents(documents)
    return chunks
```

### Bước 1.4: Embeddings — `modules/embeddings.py`

```python
# modules/embeddings.py
# ====================================================
# Module này chuyển văn bản thành vector số (embedding)
# Để máy tính có thể "so sánh" độ giống nhau giữa các đoạn text
# ====================================================

from langchain_community.embeddings import HuggingFaceEmbeddings
from config.settings import EMBEDDING_MODEL, EMBEDDING_DEVICE


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
        model_kwargs={"device": EMBEDDING_DEVICE},  # "cuda" dùng GPU
        encode_kwargs={"normalize_embeddings": True}
    )
    return embedder
```

### Bước 1.5: Vector Store — `modules/vector_store.py`

```python
# modules/vector_store.py
# ====================================================
# Module này quản lý FAISS Vector Database
# Lưu trữ vectors và tìm kiếm các chunks liên quan
# ====================================================

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


def get_retriever(vector_store, search_type=None, top_k=None):
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
    retriever = vector_store.as_retriever(
        search_type=search_type or SEARCH_TYPE,
        search_kwargs={"k": top_k or TOP_K}
    )
    return retriever
```

### Bước 1.6: Prompt Templates — `modules/prompt_templates.py`

```python
# modules/prompt_templates.py
# ====================================================
# Module này chứa các prompt template
# Prompt = "lời hướng dẫn" cho AI biết cách trả lời
# ====================================================

from langchain.prompts import PromptTemplate


def detect_language(text):
    """
    Phát hiện ngôn ngữ: tiếng Việt hay tiếng Anh.

    Giải thích:
        Kiểm tra xem text có chứa các ký tự đặc trưng tiếng Việt không.
        Ví dụ: ă, ắ, ằ, ẳ, ẵ, ặ, â, ấ, ầ... chỉ có trong tiếng Việt.
    """
    vietnamese_chars = "àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ"
    return any(char in text.lower() for char in vietnamese_chars)


def get_prompt_template(user_input):
    """
    Trả về prompt template phù hợp với ngôn ngữ câu hỏi.

    Giải thích cho người mới:
        Prompt template = "khuôn mẫu" cho AI.
        Giống như khi bạn nhờ ai trả lời, bạn nói:
        "Đọc đoạn này (context), rồi trả lời câu hỏi (question) nhé.
         Nếu không biết thì nói không biết, đừng bịa."

        {context} và {input} sẽ được thay thế bằng giá trị thực tế.
    """
    if detect_language(user_input):
        template = """Sử dụng ngữ cảnh sau đây để trả lời câu hỏi.
Nếu bạn không biết câu trả lời, chỉ cần nói là bạn không biết.
Trả lời ngắn gọn (3-4 câu) BẮNG tiếng Việt.

Ngữ cảnh: {context}

Câu hỏi: {input}

Trả lời:"""
    else:
        template = """Use the following context to answer the question.
If you don't know the answer, just say you don't know.
Keep answer concise (3-4 sentences).

Context: {context}

Question: {input}

Answer:"""

    return PromptTemplate(
        template=template,
        input_variables=["context", "input"]
    )
```

### Bước 1.7: LLM Chain — `modules/llm_chain.py`

```python
# modules/llm_chain.py
# ====================================================
# Module này kết nối LLM với RAG pipeline
# Đây là "bộ não" của hệ thống
# ====================================================

from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from config.settings import LLM_MODEL, TEMPERATURE, TOP_P
from modules.prompt_templates import get_prompt_template


def create_llm():
    """
    Tạo kết nối đến LLM qua Ollama.

    Giải thích cho người mới:
        Ollama chạy model AI trên máy local (không cần internet).
        - model: Tên model (qwen2.5:14b)
        - temperature: Mức sáng tạo
          0.0 = rất chính xác, luôn cho cùng 1 câu trả lời
          1.0 = rất sáng tạo, mỗi lần trả lời khác nhau
          0.7 = cân bằng giữa chính xác và tự nhiên
    """
    llm = Ollama(
        model=LLM_MODEL,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        repeat_penalty=1.1  # Tránh lặp lại câu
    )
    return llm


def create_rag_chain(llm, retriever, user_input):
    """
    Tạo RAG chain hoàn chỉnh.

    Giải thích cho người mới:
        RAG chain = Nối các bước lại thành 1 pipeline:

        câu hỏi → retriever tìm context → prompt ghép context + câu hỏi → LLM trả lời

        create_stuff_documents_chain: "Stuff" = nhét tất cả context vào 1 prompt
        (còn có map_reduce, refine... nhưng stuff đơn giản nhất)

        create_retrieval_chain: Nối retriever + document chain thành 1 chain hoàn chỉnh
    """
    prompt = get_prompt_template(user_input)

    # Tạo chain xử lý documents
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)

    # Tạo RAG chain hoàn chỉnh
    rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

    return rag_chain


def ask_question(rag_chain, question):
    """
    Đặt câu hỏi và nhận câu trả lời.

    Trả về:
        dict với keys: "answer", "context" (các chunks đã dùng)
    """
    response = rag_chain.invoke({"input": question})
    return response
```

### Bước 1.8: UI Styles — `ui/styles.py`

```python
# ui/styles.py
# ====================================================
# CSS custom cho Streamlit
# Streamlit mặc định khá đơn giản, ta thêm CSS để đẹp hơn
# ====================================================

from config.settings import (
    PRIMARY_COLOR, SECONDARY_COLOR, BACKGROUND_COLOR,
    SIDEBAR_BG, TEXT_COLOR
)


def get_custom_css():
    """
    Trả về CSS string để inject vào Streamlit.

    Giải thích cho người mới:
        Streamlit cho phép chèn CSS bằng st.markdown().
        CSS = ngôn ngữ trang trí web (màu sắc, font, layout...).
        Bạn không cần hiểu sâu CSS, chỉ cần thay đổi màu trong settings.py.
    """
    return f"""
    <style>
        /* Sidebar background */
        [data-testid="stSidebar"] {{
            background-color: {SIDEBAR_BG};
        }}
        [data-testid="stSidebar"] * {{
            color: white !important;
        }}

        /* Main background */
        .stApp {{
            background-color: {BACKGROUND_COLOR};
        }}

        /* Upload button */
        .stFileUploader > div > button {{
            background-color: {SECONDARY_COLOR};
            color: black;
        }}

        /* Primary buttons */
        .stButton > button {{
            background-color: {PRIMARY_COLOR};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
        }}
        .stButton > button:hover {{
            background-color: #0056b3;
        }}

        /* Response area */
        .response-box {{
            background-color: white;
            border: 1px solid #dee2e6;
            border-radius: 10px;
            padding: 20px;
            margin-top: 10px;
        }}
    </style>
    """
```

### Bước 1.9: UI Sidebar — `ui/sidebar.py`

```python
# ui/sidebar.py
# ====================================================
# Giao diện sidebar (thanh bên trái)
# ====================================================

import streamlit as st


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

        st.subheader("📖 Hướng dẫn sử dụng")
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
```

### Bước 1.10: UI Main Page — `ui/main_page.py`

```python
# ui/main_page.py
# ====================================================
# Giao diện trang chính
# ====================================================

import streamlit as st
from modules.document_loader import load_document
from modules.text_splitter import split_documents
from modules.embeddings import create_embedder
from modules.vector_store import create_vector_store, get_retriever
from modules.llm_chain import create_llm, create_rag_chain, ask_question
from config.settings import SUPPORTED_EXTENSIONS


def render_main_page():
    """Hiển thị giao diện trang chính."""

    st.title("🤖 SmartDoc AI")
    st.subheader("Intelligent Document Q&A System")
    st.markdown("Upload tài liệu và đặt câu hỏi — AI sẽ trả lời dựa trên nội dung!")

    st.markdown("---")

    # --- PHẦN 1: UPLOAD FILE ---
    st.subheader("📁 Upload Tài Liệu")

    # st.file_uploader tạo nút upload file
    # type: chỉ cho phép upload PDF và DOCX
    uploaded_file = st.file_uploader(
        "Chọn file PDF hoặc DOCX",
        type=["pdf", "docx"],
        help="Kéo thả file vào đây hoặc click để chọn"
    )

    # --- PHẦN 2: XỬ LÝ FILE ---
    if uploaded_file is not None:
        # st.session_state = biến lưu trữ giữa các lần reload
        # Kiểm tra: chỉ xử lý nếu chưa xử lý file này
        if "processed_file" not in st.session_state or \
           st.session_state.processed_file != uploaded_file.name:

            with st.spinner("📄 Đang đọc tài liệu..."):
                docs = load_document(uploaded_file)

            with st.spinner("✂️ Đang chia nhỏ văn bản..."):
                chunks = split_documents(docs)
                st.info(f"📊 Đã chia thành {len(chunks)} chunks")

            with st.spinner("🔢 Đang tạo embeddings (dùng GPU)..."):
                embedder = create_embedder()
                vector_store = create_vector_store(chunks, embedder)
                retriever = get_retriever(vector_store)

            # Lưu vào session_state để không phải xử lý lại
            st.session_state.retriever = retriever
            st.session_state.vector_store = vector_store
            st.session_state.processed_file = uploaded_file.name
            st.session_state.llm = create_llm()

            st.success(f"✅ Đã xử lý thành công: {uploaded_file.name}")

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

            # Hiển thị câu trả lời
            st.markdown("### 💬 Câu Trả Lời")
            st.markdown(f"""
            <div class="response-box">
                {response["answer"]}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("👆 Hãy upload tài liệu trước khi đặt câu hỏi.")
```

### Bước 1.11: App Entry Point — `app.py`

```python
# app.py
# ====================================================
# Entry point — File chính để chạy ứng dụng
# Chạy bằng: streamlit run app.py
# ====================================================

import streamlit as st
from ui.styles import get_custom_css
from ui.sidebar import render_sidebar
from ui.main_page import render_main_page


def main():
    """
    Hàm chính của ứng dụng.

    Giải thích cho người mới:
        st.set_page_config(): Cài đặt cấu hình trang web
        - page_title: Tiêu đề trên tab browser
        - page_icon: Icon trên tab browser
        - layout: "wide" = dùng toàn bộ chiều rộng màn hình
    """
    # Cấu hình trang
    st.set_page_config(
        page_title="SmartDoc AI",
        page_icon="🤖",
        layout="wide"
    )

    # Inject CSS custom
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    # Render UI
    render_sidebar()
    render_main_page()


# Dòng này kiểm tra: chỉ chạy main() khi file được chạy trực tiếp
# (không chạy khi được import từ file khác)
if __name__ == "__main__":
    main()
```

### Bước 1.12: Tạo `__init__.py` cho các package

```python
# modules/__init__.py
# File rỗng — đánh dấu thư mục "modules" là Python package
# Để import được: from modules.xxx import yyy

# ui/__init__.py
# File rỗng — đánh dấu thư mục "ui" là Python package

# config/__init__.py
# File rỗng
```

### Bước 1.13: Kiểm tra Base App

```bash
# Đảm bảo Ollama đang chạy
ollama serve

# Mở terminal mới, chạy app
cd e:\PTMNM\Project-LLMs-Rag-Agent
venv\Scripts\activate
streamlit run app.py

# Mở browser: http://localhost:8501
# Test: Upload PDF → Đặt câu hỏi → Kiểm tra câu trả lời
```

---

## Phase 2: Câu Hỏi 1-3 — Tính Năng Cơ Bản (3-4 ngày)

### Câu hỏi 1: Hỗ trợ file DOCX ✅ (Đã tích hợp trong Phase 1)

> Câu hỏi 1 đã được giải quyết trong `modules/document_loader.py` ở Phase 1.
> Module này đã hỗ trợ cả PDF và DOCX.

**Kiểm tra:**
```bash
# Upload file .docx → hệ thống đọc được nội dung
# Upload file .pdf → vẫn hoạt động bình thường
```

---

### Câu hỏi 2: Lưu trữ lịch sử hội thoại

**File cần tạo:** `modules/chat_history.py`

```python
# modules/chat_history.py
# ====================================================
# Module quản lý lịch sử chat
# Dùng st.session_state để lưu dữ liệu trong phiên làm việc
# ====================================================

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
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def add_to_history(question, answer):
    """Thêm cặp hỏi-đáp vào lịch sử."""
    st.session_state.chat_history.append({
        "question": question,
        "answer": answer,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })


def get_history():
    """Lấy toàn bộ lịch sử chat."""
    return st.session_state.get("chat_history", [])


def clear_history():
    """Xóa toàn bộ lịch sử chat."""
    st.session_state.chat_history = []


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
```

**Cập nhật `ui/main_page.py`** — thêm lưu lịch sử sau khi nhận câu trả lời:

```python
# Thêm import ở đầu file:
from modules.chat_history import (
    init_chat_history, add_to_history, display_chat_history_sidebar
)

# Thêm vào đầu hàm render_main_page():
init_chat_history()

# Thêm sau khi hiển thị câu trả lời (sau st.markdown response):
add_to_history(user_input, response["answer"])

# Gọi display_chat_history_sidebar() trong render flow
```

---

### Câu hỏi 3: Thêm nút xóa lịch sử

**Cập nhật `ui/sidebar.py`:**

```python
# ui/sidebar.py — thêm phần nút xóa

import streamlit as st
from modules.chat_history import clear_history, display_chat_history_sidebar


def render_sidebar():
    with st.sidebar:
        st.title("📚 SmartDoc AI")
        st.markdown("---")

        # ... (phần hướng dẫn & cấu hình giữ nguyên) ...

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

        # Hiển thị lịch sử chat (từ module chat_history)
        display_chat_history_sidebar()
```

> **Giải thích `st.rerun()`:** Streamlit hoạt động kiểu "top-to-bottom". Mỗi khi user click button, Streamlit chạy LẠI toàn bộ code từ đầu. `st.rerun()` = bắt chạy lại ngay lập tức.

---

## Phase 3: Câu Hỏi 4-6 — Tính Năng Trung Bình (5-6 ngày)

### Câu hỏi 4: Cải thiện Chunk Strategy

**Cập nhật `ui/sidebar.py`** — thêm UI chỉnh chunk:

```python
# Thêm vào sidebar, phần cấu hình:

st.markdown("---")
st.subheader("🔧 Chunk Settings")

# Slider cho chunk_size
chunk_size = st.select_slider(
    "Chunk Size (ký tự)",
    options=[500, 1000, 1500, 2000],
    value=1000,
    help="Nhỏ→chính xác hơn nhưng ít context. Lớn→nhiều context nhưng noise."
)

# Slider cho chunk_overlap
chunk_overlap = st.select_slider(
    "Chunk Overlap (ký tự)",
    options=[50, 100, 200],
    value=100,
    help="Overlap giữa các chunk để không mất ngữ cảnh ở ranh giới."
)

# Lưu vào session_state
st.session_state.chunk_size = chunk_size
st.session_state.chunk_overlap = chunk_overlap
```

**Cập nhật `ui/main_page.py`** — dùng giá trị từ UI:

```python
# Thay dòng: chunks = split_documents(docs)
# Bằng:
chunks = split_documents(
    docs,
    chunk_size=st.session_state.get("chunk_size", 1000),
    chunk_overlap=st.session_state.get("chunk_overlap", 100)
)
```

> **Lý thuyết: Chunk size ảnh hưởng thế nào?**
> ```
> chunk_size=500:  ✅ Chính xác cho câu hỏi cụ thể
>                  ❌ Thiếu context cho câu hỏi tổng quát
>
> chunk_size=1000: ✅ Cân bằng (khuyên dùng mặc định)
>
> chunk_size=2000: ✅ Nhiều context, tốt cho câu hỏi tổng quát
>                  ❌ Có thể chứa thông tin dư thừa (noise)
> ```

---

### Câu hỏi 5: Citation / Source Tracking

**Tạo `modules/citation.py`:**

```python
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
    sources = []
    # response["context"] chứa list các Document objects
    context_docs = response.get("context", [])

    for i, doc in enumerate(context_docs):
        source_info = {
            "index": i + 1,
            "content": doc.page_content[:200] + "...",  # 200 ký tự đầu
            "page": doc.metadata.get("page", "N/A"),
            "source": doc.metadata.get("source", "N/A"),
        }
        sources.append(source_info)

    return sources


def display_sources(sources):
    """
    Hiển thị nguồn dưới câu trả lời.

    Giải thích cho người mới:
        st.expander() = tạo phần mở/đóng được
        Khi click vào "📄 Nguồn 1: Trang X", nó mở ra hiện đoạn text gốc
    """
    if not sources:
        return

    st.markdown("### 📑 Nguồn tham khảo")

    for src in sources:
        with st.expander(
            f"📄 Nguồn {src['index']}: Trang {src['page']}"
        ):
            st.markdown(f"**File:** {src['source']}")
            st.markdown(f"**Trang:** {src['page']}")
            st.markdown(f"**Nội dung trích:**")
            st.code(src["content"], language=None)
```

**Cập nhật `ui/main_page.py`** — hiển thị sources sau câu trả lời:

```python
# Thêm import:
from modules.citation import extract_sources, display_sources

# Sau phần hiển thị câu trả lời, thêm:
sources = extract_sources(response)
display_sources(sources)
```

---

### Câu hỏi 6: Conversational RAG

**Cập nhật `modules/llm_chain.py`** — thêm conversational chain:

```python
# Thêm import:
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory


def create_conversational_rag_chain(llm, retriever):
    """
    Tạo RAG chain có nhớ ngữ cảnh hội thoại.

    Giải thích cho người mới:
        Chain thường: Mỗi câu hỏi là độc lập
            User: "RAG là gì?" → AI trả lời
            User: "Nó dùng để làm gì?" → AI KHÔNG BIẾT "nó" là gì!

        Conversational chain: Nhớ các câu hỏi trước
            User: "RAG là gì?" → AI trả lời
            User: "Nó dùng để làm gì?" → AI HIỂU "nó" = RAG!

        ConversationBufferWindowMemory(k=5):
            Nhớ 5 cặp hỏi-đáp gần nhất (đủ context, không tốn RAM)
    """
    # Memory lưu lịch sử hội thoại
    memory = ConversationBufferWindowMemory(
        k=5,                           # Nhớ 5 cặp hỏi-đáp gần nhất
        memory_key="chat_history",     # Key trong prompt
        return_messages=True,          # Trả về dạng messages
        output_key="answer"            # Key output
    )

    # Tạo conversational chain
    conv_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,  # Trả về sources cho citation (Q5)
        verbose=False
    )

    return conv_chain


def ask_conversational(conv_chain, question):
    """Hỏi với conversational context."""
    response = conv_chain.invoke({"question": question})
    return {
        "answer": response["answer"],
        "context": response.get("source_documents", [])
    }
```

**Cập nhật `ui/main_page.py`** — dùng conversational chain:

```python
# Thay đổi phần tạo chain và hỏi đáp:

# Trong phần xử lý file, thêm:
st.session_state.conv_chain = create_conversational_rag_chain(
    st.session_state.llm,
    st.session_state.retriever
)

# Trong phần hỏi đáp, thay:
# rag_chain = create_rag_chain(...) và ask_question(...)
# Bằng:
response = ask_conversational(
    st.session_state.conv_chain,
    user_input
)
```

---

## Phase 4: Câu Hỏi 7-8 — Tìm Kiếm Nâng Cao (4-5 ngày)

### Câu hỏi 7: Hybrid Search

**Tạo `modules/hybrid_search.py`:**

```python
# modules/hybrid_search.py
# ====================================================
# Hybrid Search = Vector Search + Keyword Search
# Kết hợp 2 cách tìm kiếm để kết quả tốt hơn
# ====================================================

from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from config.settings import TOP_K


def create_hybrid_retriever(chunks, vector_retriever, top_k=None):
    """
    Tạo hybrid retriever kết hợp BM25 + Vector Search.

    Giải thích cho người mới:
        Có 2 cách tìm kiếm:

        1. Vector Search (đang dùng - FAISS):
           - Tìm theo NGHĨA (semantic)
           - "thủ đô Việt Nam" → tìm được "Hà Nội là trung tâm hành chính"
           - Mạnh: Hiểu nghĩa, synonyms
           - Yếu: Từ khóa chính xác (tên riêng, số...)

        2. BM25 (keyword search):
           - Tìm theo TỪ KHÓA chính xác
           - "Hà Nội" → tìm được câu chứa "Hà Nội"
           - Mạnh: Tên riêng, số liệu, từ khóa kỹ thuật
           - Yếu: Không hiểu synonyms

        Hybrid = kết hợp cả hai → tốt nhất!

        weights=[0.5, 0.5]: Trọng số bằng nhau
        Có thể chỉnh: [0.7, 0.3] = ưu tiên BM25 hơn
    """
    k = top_k or TOP_K

    # BM25 Retriever — tìm kiếm theo từ khóa
    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = k

    # Ensemble Retriever — kết hợp cả hai
    hybrid_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever],
        weights=[0.5, 0.5]  # Trọng số: 50% BM25 + 50% Vector
    )

    return hybrid_retriever
```

**Cập nhật `ui/sidebar.py`** — toggle hybrid search:

```python
# Thêm vào sidebar:
st.markdown("---")
st.subheader("🔍 Search Settings")
use_hybrid = st.toggle("Dùng Hybrid Search (BM25 + Vector)", value=False)
st.session_state.use_hybrid = use_hybrid

if use_hybrid:
    bm25_weight = st.slider("Trọng số BM25", 0.0, 1.0, 0.5, 0.1)
    st.session_state.bm25_weight = bm25_weight
    st.caption(f"BM25: {bm25_weight:.0%} | Vector: {1-bm25_weight:.0%}")
```

**Cập nhật `ui/main_page.py`:**

```python
# Thêm import:
from modules.hybrid_search import create_hybrid_retriever

# Sau khi tạo vector_store & retriever, thêm:
if st.session_state.get("use_hybrid", False):
    st.session_state.retriever = create_hybrid_retriever(
        chunks,
        retriever
    )
    st.info("🔀 Đang dùng Hybrid Search (BM25 + Vector)")
```

---

### Câu hỏi 8: Multi-document RAG với Metadata Filtering

**Cập nhật `ui/main_page.py`** — hỗ trợ upload nhiều file:

```python
# Thay file_uploader:
uploaded_files = st.file_uploader(
    "Chọn file PDF hoặc DOCX",
    type=["pdf", "docx"],
    accept_multiple_files=True,  # Cho phép chọn nhiều file
    help="Có thể chọn nhiều file cùng lúc"
)
```

**Cập nhật `modules/document_loader.py`** — thêm metadata:

```python
from datetime import datetime


def load_multiple_documents(uploaded_files):
    """
    Load nhiều files và gắn metadata.

    Giải thích cho người mới:
        Metadata = "nhãn" gắn cho mỗi document
        Ví dụ: file "baocao.pdf" trang 3 → metadata = {
            "source": "baocao.pdf",
            "page": 3,
            "upload_date": "2026-03-07",
            "file_type": "pdf"
        }
        → Khi trả lời, biết được "thông tin này từ file nào, trang mấy"
    """
    all_documents = []

    for uploaded_file in uploaded_files:
        docs = load_document(uploaded_file)

        # Gắn thêm metadata cho mỗi document
        for doc in docs:
            doc.metadata.update({
                "source_file": uploaded_file.name,
                "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "file_type": uploaded_file.name.split(".")[-1].upper()
            })
        all_documents.extend(docs)

    return all_documents
```

**Cập nhật `ui/sidebar.py`** — filter theo document:

```python
# Thêm vào sidebar (sau khi upload xong):
if "uploaded_file_names" in st.session_state:
    st.markdown("---")
    st.subheader("📋 Filter Documents")
    selected_files = st.multiselect(
        "Chọn tài liệu để tìm kiếm:",
        st.session_state.uploaded_file_names,
        default=st.session_state.uploaded_file_names
    )
    st.session_state.selected_files = selected_files
```

**Cập nhật `modules/vector_store.py`** — filter khi search:

```python
def get_filtered_retriever(vector_store, selected_files, top_k=None):
    """
    Retriever có filter theo tên file.

    Giải thích cho người mới:
        filter = "chỉ tìm trong file X, Y"
        Ví dụ: Upload 3 file, nhưng chỉ muốn hỏi về file 1 và 2
        → filter loại bỏ kết quả từ file 3
    """
    k = top_k or TOP_K

    def filter_fn(metadata):
        return metadata.get("source_file") in selected_files

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k,
            "filter": filter_fn
        }
    )
    return retriever
```

---

## Phase 5: Câu Hỏi 9-10 — Tính Năng Chuyên Sâu (5-7 ngày)

### Câu hỏi 9: Re-ranking với Cross-Encoder

**Tạo `modules/reranker.py`:**

```python
# modules/reranker.py
# ====================================================
# Re-ranking: Đánh giá lại mức độ liên quan sau khi tìm kiếm
# Dùng Cross-Encoder — chính xác hơn nhưng chậm hơn
# ====================================================

from sentence_transformers import CrossEncoder


class Reranker:
    """
    Cross-Encoder Re-ranker.

    Giải thích cho người mới:
        Tưởng tượng bạn tìm Google, được 10 kết quả.
        Re-ranking = đọc kỹ lại 10 kết quả đó, sắp xếp lại cho chính xác hơn.

        Bi-Encoder (FAISS - bước 1):
            - Encode query và document RIÊNG BIỆT → so sánh vector
            - Nhanh (có thể tìm triệu documents)
            - Nhưng kém chính xác hơn

        Cross-Encoder (Re-ranker - bước 2):
            - Encode query VÀ document CÙNG LÚC → cho điểm trực tiếp
            - Chậm (chỉ xử lý được vài chục documents)
            - Nhưng CHÍNH XÁC hơn nhiều

        Workflow: query → FAISS lấy top-20 → Cross-Encoder re-rank → lấy top-3
    """

    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(self, query, documents, top_k=3):
        """
        Re-rank documents based on relevance to query.

        Tham số:
            query: Câu hỏi
            documents: List[Document] từ retriever
            top_k: Số documents giữ lại sau re-ranking
        """
        if not documents:
            return documents

        # Tạo cặp [query, document_content] để Cross-Encoder đánh giá
        pairs = [[query, doc.page_content] for doc in documents]

        # Cross-Encoder cho điểm relevance mỗi cặp
        scores = self.model.predict(pairs)

        # Sắp xếp documents theo điểm (cao → thấp)
        scored_docs = list(zip(documents, scores))
        scored_docs.sort(key=lambda x: x[1], reverse=True)

        # Trả về top_k documents có điểm cao nhất
        reranked_docs = [doc for doc, score in scored_docs[:top_k]]
        return reranked_docs
```

**Cập nhật flow trong `ui/main_page.py`:**

```python
# Thêm import:
from modules.reranker import Reranker

# Sau khi lấy kết quả từ retriever, thêm bước re-rank:
if st.session_state.get("use_reranker", False):
    with st.spinner("🔄 Đang re-ranking kết quả..."):
        reranker = Reranker()
        docs = retriever.get_relevant_documents(user_input)
        reranked_docs = reranker.rerank(user_input, docs, top_k=3)
        # Dùng reranked_docs thay vì retriever
```

**Thêm toggle trong sidebar:**

```python
use_reranker = st.toggle("Dùng Re-ranking (Cross-Encoder)", value=False)
st.session_state.use_reranker = use_reranker
if use_reranker:
    st.caption("⚡ Re-ranking chính xác hơn nhưng chậm hơn ~2-3 giây")
```

---

### Câu hỏi 10: Advanced RAG với Self-RAG

**Tạo `modules/self_rag.py`:**

```python
# modules/self_rag.py
# ====================================================
# Self-RAG: LLM tự đánh giá và cải thiện câu trả lời
# Bao gồm: Query Rewriting, Self-Evaluation, Confidence Scoring
# ====================================================

from langchain_community.llms import Ollama
from config.settings import LLM_MODEL


class SelfRAG:
    """
    Self-RAG: LLM tự kiểm tra và cải thiện output.

    Giải thích cho người mới:
        Giống như làm bài kiểm tra:
        1. Viết bài (generation)
        2. Đọc lại (self-evaluation)
        3. Sửa chỗ sai (refinement)

        Self-RAG có 3 bước:
        1. Query Rewriting: Viết lại câu hỏi cho rõ ràng hơn
        2. Self-Evaluation: Kiểm tra câu trả lời có đúng không
        3. Confidence Scoring: Cho điểm mức độ tin cậy
    """

    def __init__(self, llm=None):
        self.llm = llm or Ollama(model=LLM_MODEL)

    def rewrite_query(self, original_query):
        """
        Viết lại câu hỏi cho rõ ràng hơn.

        Ví dụ:
            "nó hoạt động ntn?" → "Hệ thống RAG hoạt động như thế nào?"
        """
        prompt = f"""Hãy viết lại câu hỏi sau cho rõ ràng và cụ thể hơn.
Chỉ trả về câu hỏi đã viết lại, không giải thích thêm.

Câu hỏi gốc: {original_query}

Câu hỏi cải thiện:"""

        rewritten = self.llm.invoke(prompt).strip()
        return rewritten

    def evaluate_answer(self, question, answer, context):
        """
        LLM tự đánh giá câu trả lời.

        Trả về dict với:
        - is_relevant: Câu trả lời có liên quan đến câu hỏi không?
        - is_factual: Câu trả lời có dựa trên context không?
        - confidence: Mức độ tin cậy (0-100)
        """
        prompt = f"""Đánh giá câu trả lời sau dựa trên context và câu hỏi.
Trả về CHÍNH XÁC theo format:
relevant: yes/no
factual: yes/no
confidence: [số từ 0 đến 100]

Context: {context[:500]}

Câu hỏi: {question}

Câu trả lời: {answer}

Đánh giá:"""

        evaluation = self.llm.invoke(prompt).strip()

        # Parse kết quả
        result = {
            "is_relevant": "yes" in evaluation.lower().split("relevant:")[-1].split("\n")[0] if "relevant:" in evaluation.lower() else True,
            "is_factual": "yes" in evaluation.lower().split("factual:")[-1].split("\n")[0] if "factual:" in evaluation.lower() else True,
            "confidence": self._extract_confidence(evaluation)
        }

        return result

    def _extract_confidence(self, text):
        """Trích xuất confidence score từ text."""
        import re
        numbers = re.findall(r'confidence:\s*(\d+)', text.lower())
        if numbers:
            return min(int(numbers[0]), 100)
        return 70  # Default

    def multi_hop_query(self, question, retriever, rag_chain, max_hops=2):
        """
        Multi-hop reasoning: Nếu 1 lần tìm chưa đủ, tìm lại.

        Giải thích:
            Câu hỏi phức tạp cần nhiều bước:
            "So sánh A và B" → tìm về A → tìm về B → so sánh

            max_hops=2: Tối đa 2 lần tìm kiếm lại
        """
        # Lần 1: Hỏi bình thường
        response = rag_chain.invoke({"input": question})
        answer = response.get("answer", "")
        context_docs = response.get("context", [])
        context_text = " ".join([d.page_content for d in context_docs])

        # Đánh giá
        evaluation = self.evaluate_answer(question, answer, context_text)

        # Nếu confidence thấp và còn hops, thử lại với query mới
        if evaluation["confidence"] < 50 and max_hops > 0:
            # Viết lại query
            new_query = self.rewrite_query(question)
            # Tìm lại
            return self.multi_hop_query(
                new_query, retriever, rag_chain, max_hops - 1
            )

        return {
            "answer": answer,
            "context": context_docs,
            "evaluation": evaluation,
            "query_used": question
        }
```

**Hiển thị confidence trong UI:**

```python
# Trong main_page.py, sau phần hiển thị câu trả lời:

if st.session_state.get("use_self_rag", False):
    evaluation = response.get("evaluation", {})
    confidence = evaluation.get("confidence", 0)

    # Thanh confidence
    st.markdown("### 📊 Mức độ tin cậy")
    st.progress(confidence / 100)

    if confidence >= 80:
        st.success(f"🟢 Tin cậy cao ({confidence}%)")
    elif confidence >= 50:
        st.warning(f"🟡 Tin cậy trung bình ({confidence}%)")
    else:
        st.error(f"🔴 Tin cậy thấp ({confidence}%) — nên kiểm tra lại")
```

---

## Phase 6: Hoàn Thiện & Nộp Bài (2-3 ngày)

### Bước 6.1: Viết README.md

```markdown
# SmartDoc AI - Intelligent Document Q&A System

## Giới thiệu
Hệ thống hỏi đáp tài liệu thông minh dựa trên RAG...

## Cài đặt
1. Clone project
2. `python -m venv venv && venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. `ollama pull qwen2.5:14b`
5. `streamlit run app.py`

## Tính năng
- Upload PDF/DOCX
- Hỏi đáp bằng tiếng Việt/Anh
- Lịch sử chat
- Hybrid search
- ...
```

### Bước 6.2: Testing

```python
# tests/test_loader.py
def test_load_pdf():
    """Test đọc file PDF."""
    # Upload file mẫu → kiểm tra có trả về documents không
    pass

def test_load_docx():
    """Test đọc file DOCX."""
    pass

def test_invalid_file():
    """Test file không hỗ trợ → có báo lỗi đúng không."""
    pass
```

### Bước 6.3: Checklist trước khi nộp

- [ ] Tất cả 10 tính năng hoạt động
- [ ] Code có comments
- [ ] README.md đầy đủ
- [ ] Không có error khi chạy
- [ ] Test edge cases (file rỗng, câu hỏi ngoài nội dung)

---

## Checklist Kiểm Tra

| # | Tính năng | Cách kiểm tra | Status |
|---|-----------|---------------|--------|
| Base | Upload PDF + hỏi đáp | Upload PDF → đặt câu hỏi → nhận trả lời | ⬜ |
| Q1 | Hỗ trợ DOCX | Upload file .docx → đọc được nội dung | ⬜ |
| Q2 | Lịch sử chat | Hỏi nhiều câu → lịch sử hiện sidebar | ⬜ |
| Q3 | Nút xóa | Click "Xóa" → hiện confirm → xóa sạch | ⬜ |
| Q4 | Chunk strategy | Thay chunk_size trên UI → kết quả thay đổi | ⬜ |
| Q5 | Citation | Trả lời hiển thị "Nguồn: Trang X" | ⬜ |
| Q6 | Conversational | Hỏi "nó là gì?" → AI hiểu context trước | ⬜ |
| Q7 | Hybrid search | Toggle hybrid → kết quả keyword tốt hơn | ⬜ |
| Q8 | Multi-document | Upload 2+ files → filter → trả lời đúng nguồn | ⬜ |
| Q9 | Re-ranking | Toggle reranker → kết quả chính xác hơn | ⬜ |
| Q10 | Self-RAG | Hiển thị confidence + query rewriting hoạt động | ⬜ |

---

## Timeline Gợi Ý

```
Tuần 1 (07-13/03): Phase 0 + Phase 1 (Setup + Base App)
Tuần 2 (14-20/03): Phase 2 (Q1-Q3: DOCX, History, Clear)
Tuần 3 (21-27/03): Phase 3 (Q4-Q6: Chunk, Citation, Conversational)
Tuần 4 (28/03-03/04): Phase 4 (Q7-Q8: Hybrid, Multi-doc)
Tuần 5 (04-10/04): Phase 5 (Q9-Q10: Reranker, Self-RAG)
Tuần 6 (11-17/04): Phase 6 (Testing, Documentation, Polish)
Deadline: 19/04/2026
```

> **Lời khuyên:** Hoàn thành Phase 0-3 trước (Q1-Q6 = phần lớn điểm). Q7-Q10 là bonus, làm được càng tốt nhưng không bắt buộc 100%.
```

---

Toàn bộ nội dung trên là file `PLANNING.md`. Hãy tạo file tại:

**`e:\PTMNM\Project-LLMs-Rag-Agent\PLANNING.md`**

và paste toàn bộ nội dung từ ` ```markdown ` đến hết ` ``` ` cuối cùng.

**Tóm tắt cập nhật theo yêu cầu:**
- **Tách module**: 12 files riêng biệt (config, modules, ui, tests) thay vì 1 file `app.py`. Mỗi file 50-100 dòng dễ đọc
- **Model**: Dùng **`qwen2.5:14b`** (máy 40GB RAM dư sức), embedding chạy trên **CUDA** (GPU NVIDIA) thay vì CPU
- **`faiss-gpu`** thay `faiss-cpu` để tận dụng GPU
- Mỗi đoạn code đều có comment tiếng Việt giải thích cho người mới---

Toàn bộ nội dung trên là file `PLANNING.md`. Hãy tạo file tại:

**`e:\PTMNM\Project-LLMs-Rag-Agent\PLANNING.md`**

và paste toàn bộ nội dung từ ` ```markdown ` đến hết ` ``` ` cuối cùng.

**Tóm tắt cập nhật theo yêu cầu:**
- **Tách module**: 12 files riêng biệt (config, modules, ui, tests) thay vì 1 file `app.py`. Mỗi file 50-100 dòng dễ đọc
- **Model**: Dùng **`qwen2.5:14b`** (máy 40GB RAM dư sức), embedding chạy trên **CUDA** (GPU NVIDIA) thay vì CPU
- **`faiss-gpu`** thay `faiss-cpu` để tận dụng GPU
- Mỗi đoạn code đều có comment tiếng Việt giải thích cho người mới