import functools
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import warnings
warnings.filterwarnings("ignore", message=".*TOKENIZERS_PARALLELISM.*")
warnings.filterwarnings("ignore", message=".*torch.classes.*__path__._path.*")
warnings.filterwarnings("ignore", message=".*Examining the path of torch.classes.*")

MODEL_NAME = "wonrax/phobert-base-vietnamese-sentiment"

@functools.lru_cache(maxsize=1)
def get_sentiment_pipeline():
    # Tải mô hình đã được tinh chỉnh cho 3 nhãn (NEGATIVE, NEUTRAL, POSITIVE)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    clf = pipeline(
        "sentiment-analysis", 
        model=model, 
        tokenizer=tokenizer, 
        device=-1
        )
    return clf