from decouple import config

API_KEY = config('API_KEY')
MODEL4 = config('GPT4')
MODEL3 = config('GPT3')
GPT4_ENABLED = False
MAX_USER_INPUT = 16