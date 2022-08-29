import os


class Config:
    PAY_ENDPOINT = os.getenv('ENOT_PAY_ENDPOINT')
    API_ENDPOINT = os.getenv('ENOT_API_ENDPOINT')
    MERCHANT_ID = os.getenv('ENOT_MERCHANT_ID')
    SECRET_WORD_1 = os.getenv('ENOT_SECRET_WORD_1')
    SECRET_WORD_2 = os.getenv('ENOT_SECRET_WORD_2')
    API_KEY = os.getenv('ENOT_API_KEY')
    EMAIL = os.getenv('ENOT_EMAIL')
