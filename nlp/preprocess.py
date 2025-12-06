
import re
import unicodedata
from underthesea import word_tokenize

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"   # Dòng quan trọng nhất
os.environ["OMP_NUM_THREADS"] = "1"              # Tránh xung đột đa luồng


SLANG_MAP = {
    "rat": "rất", "hok": "không", "ko": "không", "k": "không",
    "dc": "được", "vs": "với", "dep": "đẹp", "xau": "xấu",
    "j": "gì", "lun": "luôn", "wa": "quá", "qá": "quá",
    "bik": "biết", "cj": "chị", "dt": "dễ thương", "vk": "vợ",
    "ck": "chồng", "hk": "không", "nhìu": "nhiều", "nh": "như",
    "bt": "bình thường", "iem": "em", "iemm": "em", "thui": "thôi",
    "r": "rồi", "iem": "em", "ntn": "như thế nào", "ng": "người",
    "iu": "yêu", "okela": "ổn", "okla": "ổn", "tạm dc": "tạm được",
}

# def normalize_slang(text: str) -> str:
#     """Thay viết tắt bằng từ gốc."""
#     tokens = text.split()
#     new_tokens = []
#     for t in tokens:
#         key = t.lower()
#         new_tokens.append(SLANG_MAP.get(key, t))
#     return " ".join(new_tokens)


# def preprocess_text(raw_text: str) -> str:
#     """
#     Chuẩn hóa tiếng Việt:
#     - loại bỏ biểu tượng, emoji, ký tự đặc biệt
#     - Xóa khoảng trắng
#     - lower case
#     - sửa viết tắt
#     - tách từ
#     - giới hạn độ dài
#     """
#     if not raw_text or not raw_text.strip():
#         return ""

#     text = unicodedata.normalize("NFC", raw_text.strip())
#     text = re.sub(r"[^\w\sàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ]", " ", text)
#     text = re.sub(r"\s+", " ", text).strip().lower()
#     text = normalize_slang(text)

#     try:
#         tokenized = word_tokenize(text, format="text")
#         if tokenized and isinstance(tokenized, str):
#             text = tokenized
#     except Exception as e:
#         print(f"Lỗi khi tách từ (word_tokenize)! {e}")
#         pass

#     return text[:50]  # giới hạn 50 ký tự



def preprocess_text(raw_text: str) -> str:
    """
    Tạm thời VÔ HIỆU HÓA các bước chuẩn hóa (tách từ và sửa viết tắt) 
    để kiểm tra mô hình KHÔNG sử dụng tiền xử lý.
    """
    if not raw_text or not raw_text.strip():
        return ""

    # 1. Chuẩn hóa Unicode
    text = unicodedata.normalize("NFC", raw_text.strip())

    # 2. Xóa biểu tượng, emoji, ký tự đặc biệt (giữ lại để tránh lỗi Tokenizer)
    # Loại bỏ các ký tự không phải chữ cái/số/khoảng trắng
    text = re.sub(r"[^\w\s]", "", text) 
    
    # 3. lower case và Xóa khoảng trắng thừa
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()

    # !!! CÁC BƯỚC QUAN TRỌNG ĐÃ BỊ VÔ HIỆU HÓA !!!
    # - Bỏ gọi normalize_slang(text)
    # - Bỏ gọi word_tokenize(text, format="text") 
    
    return text