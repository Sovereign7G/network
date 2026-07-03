# gateway/token_counter.py
import tiktoken

def estimate_tokens(messages: list, model: str = "gpt-3.5-turbo") -> int:
    try:
        enc = tiktoken.encoding_for_model(model)
    except KeyError:
        enc = tiktoken.get_encoding("cl100k_base")
    n = sum(len(enc.encode(m.get("content", ""))) + 4 for m in messages) + 2
    return n

def calculate_cost(tokens: int, price_per_1k: float = 0.001) -> float:
    return (tokens / 1000.0) * price_per_1k
