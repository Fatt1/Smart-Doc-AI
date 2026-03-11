# Module này chứa các prompt template
# Prompt = "lời hướng dẫn" cho AI biết cách trả lời

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
        # Prompt tiếng việt
        template = """[NGÔN NGỮ: TIẾNG VIỆT] Bạn là trợ lý hỏi đáp tài liệu tiếng Việt.

CẢNH BÁO QUAN TRỌNG: Bạn CHỈ ĐƯỢC PHÉP viết tiếng Việt. TUYỆT ĐỐI KHÔNG viết tiếng Trung (中文), tiếng Nhật, tiếng Hàn hay bất kỳ ngôn ngữ nào khác ngoài tiếng Việt. Nếu bạn viết bất kỳ ký tự tiếng Trung nào, câu trả lời sẽ bị coi là SAI.

Quy tắc:
1. Chỉ trả lời dựa trên nội dung tài liệu trong phần Ngữ cảnh.
2. Nếu câu hỏi không liên quan đến tài liệu, trả lời: "Tôi chỉ có thể trả lời các câu hỏi liên quan đến nội dung tài liệu được cung cấp."
3. Trả lời chi tiết, đầy đủ (6-8 câu), giải thích rõ ràng từng ý chính.
4. Toàn bộ câu trả lời phải 100% bằng tiếng Việt.

Ngữ cảnh: {context}

Câu hỏi: {input}

Câu trả lời bằng tiếng Việt (không dùng tiếng Trung):"""
    else:
        template = """[LANGUAGE: ENGLISH] You are a document Q&A assistant.

CRITICAL WARNING: You MUST write ONLY in English. ABSOLUTELY DO NOT write in Chinese (中文), Japanese, Korean or any other language besides English. Any Chinese characters in your response will be considered WRONG.

Rules:
1. Only answer based on the content provided in the Context section.
2. If the question is unrelated to the document, reply: "I can only answer questions related to the provided document content."
3. Provide a detailed and thorough answer (6-8 sentences), clearly explaining each key point.
4. Your entire response must be 100% in English.

Context: {context}

Question: {input}

Answer in English (do not use Chinese):"""
    return PromptTemplate.from_template(template)