# test_cases.py
from nlp.engine import classify_sentiment

TEST_CASES = [
    # STT, text, expected_sentiment
    (1, "Tốt quá ha, phục luôn đó", "POSITIVE"),
    (2, "Món ăn này dở quá", "NEGATIVE"),
    (3, "Thời tiết bình thường", "NEUTRAL"),
    (4, "Rat vui hom nay", "POSITIVE"),
    (5, "Công việc ổn định", "NEUTRAL"),
    (6, "Tôi rất thất vọng về sản phẩm", "NEGATIVE"),
    (7, "Tuyệt vời ông mặt trời", "POSITIVE"),
    (8, "Bình thường không có gì đặc biệt", "NEUTRAL"),
    (9, "Chán quá hôm nay ai cũng bực bội", "NEGATIVE"),
    (10, "Tạm ổn, không tốt cũng không xấu", "NEUTRAL"),
]


def run_tests():
    correct = 0
    total = len(TEST_CASES)

    for idx, text, expected in TEST_CASES:
        result = classify_sentiment(text)
        predicted = result["sentiment"]

        print(f"[{idx}] {text}")
        print(f"   Expected: {expected} | Predicted: {predicted}")

        if predicted == expected:
            correct += 1

    accuracy = correct / total * 100
    print("-" * 50)
    print(f"Accuracy: {correct}/{total} = {accuracy:.2f}%")


if __name__ == "__main__":
    run_tests()
