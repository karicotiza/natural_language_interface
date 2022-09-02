import nltk


def normalize(sentence: str) -> list:
    valid_parts_of_speech = ["NN", "NNS", "NNP", "NNPS"]

    tokenizer = nltk.TweetTokenizer()
    lemmatizer = nltk.wordnet.WordNetLemmatizer()

    sentence = tokenizer.tokenize(sentence)
    sentence = [
        word for word in sentence if nltk.pos_tag([word])[0][1] in valid_parts_of_speech
    ]
    sentence = [lemmatizer.lemmatize(word).lower() for word in sentence]

    return sentence


