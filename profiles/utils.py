import uuid

def get_random_text():
    text = str(uuid.uuid4())[:8].replace('-','').lower()
    return text