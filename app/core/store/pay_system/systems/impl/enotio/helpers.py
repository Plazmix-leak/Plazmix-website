import hashlib


def generate_pay_sign(merchant_id: int, order_amount: float, secret_word: str, payment_id) -> str:
    sign_raw = f"{merchant_id}:{order_amount}:{secret_word}:{payment_id}"
    return hashlib.md5(sign_raw.encode('utf-8')).hexdigest()
