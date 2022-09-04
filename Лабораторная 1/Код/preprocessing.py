import nltk
import string


def normalize(sentence: str) -> list:
    valid_parts_of_speech = ["NN", "NNS", "NNP", "NNPS", "JJ", "JJR", "JJS"]

    tokenizer = nltk.TweetTokenizer()
    stemmer = nltk.stem.LancasterStemmer()

    sentence = tokenizer.tokenize(sentence)
    sentence = [
        word for word in sentence if nltk.pos_tag([word])[0][1] in valid_parts_of_speech
    ]
    sentence = [stemmer.stem(word).lower() for word in sentence]
    sentence = [word for word in sentence if is_in_english(word)]

    return sentence


def is_article(title: str) -> bool:
    if not title.startswith("User:") and not title.startswith("Talk:"):
        return True
    else:
        return False


def is_in_english(word: str) -> bool:
    allowed_letters = list(string.ascii_lowercase)
    allowed_letters.append("'")
    for letter in word.lower():
        if letter in allowed_letters:
            pass
        else:
            return False
    return True
