import re
import string

def clean_text(text):
    # Keep it lowercase
    text = str(text).lower()
    

    punctuation_to_keep = '?!'
    punctuation_to_remove = "".join([char for char in string.punctuation if char not in punctuation_to_keep])
    
    text = text.translate(str.maketrans('', '', punctuation_to_remove))
    
    return text.strip()