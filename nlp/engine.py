from .preprocess import preprocess_text
from .pipeline import get_sentiment_pipeline

def map_label(label: str) -> str:
    """Chuyển nhãn từ mô hình sang định dạng chuẩn."""
    label = label.upper()
    if label in ["POS", "POSITIVE"]: return "POSITIVE"
    if label in ["NEG", "NEGATIVE"]: return "NEGATIVE"
    if label in ["NEU", "NEUTRAL"]:   return "NEUTRAL"
    return "NEUTRAL"

def classify_sentiment(raw_text: str) -> dict:
    """Trả về {text, sentiment, score}"""

    if not raw_text or len(raw_text.strip()) < 5:
        raise ValueError("Câu quá ngắn, vui lòng nhập ít nhất 5 ký tự.")

    preprocessed = preprocess_text(raw_text)

    clf = get_sentiment_pipeline()
    # Chỉ lấy kết quả có điểm số cao nhất (top_k=1)
    result = clf(preprocessed, top_k=1)[0]

    label = map_label(result["label"])
    score = float(result["score"])

    # Áp dụng quy tắc bổ sung để cải thiện độ chính xác
    lowered = raw_text.lower()
    
   
    if score < 0.5:
        label = "NEUTRAL"

    return {
        "text": raw_text,
        "sentiment": label,
        "score": score,
    }
