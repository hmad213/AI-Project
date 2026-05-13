import re
import string
import html

# Precompiled regex patterns
MULTISPACE_PATTERN = re.compile(r"\s+")

# Preserve repeated punctuation as features
EXCLAMATION_PATTERN = re.compile(r"!{2,}")
QUESTION_PATTERN = re.compile(r"\?{2,}")

# Normalize elongated words
ELONGATED_PATTERN = re.compile(r"(.)\1{2,}")

# Detect ALL CAPS words
ALL_CAPS_PATTERN = re.compile(r"\b[A-Z]{2,}\b")

# Common laughter/interjection patterns
LAUGHTER_PATTERN = re.compile(
    r"\b(lmao+|lmfao+|rofl+|haha+|hehe+|lol+)\b",
    flags=re.IGNORECASE
)


def normalize_elongated(word):
    return ELONGATED_PATTERN.sub(r"\1\1", word)


def clean_text(text):

    if not isinstance(text, str):
        text = str(text)


    text = html.unescape(text)

    # Count ALL CAPS before lowercasing
    caps_count = len(ALL_CAPS_PATTERN.findall(text))

    # Replace repeated punctuation with tokens
    text = EXCLAMATION_PATTERN.sub(
        " <MULTIEXCLAMATION> ",
        text
    )

    text = QUESTION_PATTERN.sub(
        " <MULTIQUESTION> ",
        text
    )

    # Normalize laughter
    text = LAUGHTER_PATTERN.sub(
        " <LAUGH> ",
        text
    )

    # Normalize elongated words
    words = text.split()
    words = [normalize_elongated(w) for w in words]
    text = " ".join(words)

    # Lowercase
    text = text.lower()

    # Keep only useful punctuation
    punctuation_to_keep = "?!<>"

    punctuation_to_remove = "".join(
        ch for ch in string.punctuation
        if ch not in punctuation_to_keep
    )

    text = text.translate(
        str.maketrans("", "", punctuation_to_remove)
    )

    # Remove extra spaces
    text = MULTISPACE_PATTERN.sub(" ", text)

    text = text.strip()

    # Add capitalization feature token
    if caps_count > 0:
        text += f" <ALLCAPS_{min(caps_count,5)}>"

    return text