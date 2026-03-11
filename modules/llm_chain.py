# Module này kết nối LLM với RAG pipeline
# Đây là "bộ não" của hệ thống

from langchain.chains import retrieval_qa
from langchain_community.llms import ollama
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from config.settings import LLM_MODEL, TEMPERATURE, TOP_P
from modules.prompt_templates import get_prompt_template
from langchain_core.runnables import Runnable
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
    llm = ollama.Ollama(
        model=LLM_MODEL,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        repeat_penalty=1.1 # Tránh lặp lại câu trả lời giống nhau
                        )
    return llm

def create_rag_chain(llm, retriever, user_input)-> Runnable:
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

    # Tạo document chain (cách kết hợp context + câu hỏi)
    combine_docs_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)

    # Tạo Rag chain nối retriever + document chain
    rag_chain = create_retrieval_chain(retriever=retriever, combine_docs_chain=combine_docs_chain)
    return rag_chain

def ask_question(rag_chain: Runnable, question):
    """
    Đặt câu hỏi và nhận câu trả lời.

    Trả về:
        dict với keys: "answer", "context" (các chunks đã dùng)
    """
    response = rag_chain.invoke({"input": question})
    return response