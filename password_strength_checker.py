from pwnedpasswords import check
import nltk
import string
import math
import os

nltk.download('words', quiet=True)
from nltk.corpus import words

# Load commonly used passwords from file
COMMON_PASSWORDS_PATH = os.path.join(os.path.dirname(__file__), "commonly_used_passwords.txt")
try:
    with open(COMMON_PASSWORDS_PATH, "r", encoding="utf-8") as f:
        commonly_used_passwords = set(line.strip().lower() for line in f if line.strip())
except FileNotFoundError:
    commonly_used_passwords = set()

# Example commonly used passwords list (expand as needed)
def contains_dictionary_word(password):
    word_list = set(words.words())
    password_lower = password.lower()
    # Check for any word of length >= 3 in the password
    for word in word_list:
        if len(word) >= 3 and word in password_lower:
            return True, word
    return False, None

def estimate_crack_time(password):
    # Simple entropy-based estimate
    charset = 0
    if any(c.islower() for c in password):
        charset += 26
    if any(c.isupper() for c in password):
        charset += 26
    if any(c.isdigit() for c in password):
        charset += 10
    if any(c in string.punctuation for c in password):
        charset += len(string.punctuation)
    if charset == 0:
        charset = 1
    entropy = len(password) * math.log2(charset)
    guesses = 2 ** entropy
    guesses_per_second = 1e10  # 10 billion guesses/sec (modern GPU)
    seconds = guesses / guesses_per_second
    years = seconds / (60 * 60 * 24 * 365)
    return years

def check_password(password):
    results = []

    # Length check
    if len(password) < 8:
        results.append("❌ Password is too short (min 8 characters).")
    elif len(password) > 16:
        results.append("❌ Password is too long (max 16 characters).")
    else:
        results.append("✔️ Password length is OK.")

    # Commonly used password check
    if password.lower() in commonly_used_passwords:
        results.append("❌ Password is a commonly used password!")
    else:
        results.append("✔️ Not a commonly used password.")

    # Dictionary word check
    found, word = contains_dictionary_word(password)
    if found:
        results.append(f"❌ Password contains the dictionary word: '{word}'")
    else:
        results.append("✔️ No dictionary words found in password.")

    # Pwned password check
    try:
        pwned_count = check(password)
        if pwned_count > 0:
            results.append(f"❌ Password has been found in {pwned_count} data breaches!")
        else:
            results.append("✔️ Password has not been found in known breaches.")
    except Exception as e:
        results.append(f"⚠️ Could not check pwned status: {e}")

    # Crack time estimate
    years = estimate_crack_time(password)
    if years > 1e6:
        results.append(f"✔️ Estimated crack time: {int(years)} years (very strong).")
    elif years > 100:
        results.append(f"⚠️ Estimated crack time: {int(years)} years (strong).")
    elif years > 1:
        results.append(f"⚠️ Estimated crack time: {int(years)} years (moderate).")
    else:
        results.append(f"❌ Estimated crack time: {years:.2f} years (weak).")

    return "\n".join(results)