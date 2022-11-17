import nltk
import os

from nltk.tree.prettyprinter import TreePrettyPrinter


class SyntaxTree:
    __JARS = (
        "C:/Storage/Modules/Stanford NLP Core/stanford-corenlp-4.4.0.jar",
        "C:/Storage/Modules/Stanford NLP Core/stanford-corenlp-4.4.0-models.jar"
    )

    os.environ['JAVAHOME'] = "C:/Program Files/Java/jre1.8.0_351/bin/java.exe"

    @staticmethod
    def make_tree(sentence: str) -> str:
        with nltk.parse.corenlp.CoreNLPServer(*SyntaxTree.__JARS):
            parser = nltk.parse.corenlp.CoreNLPParser()
            try:
                parse = next(parser.raw_parse(sentence))
            except StopIteration:
                return ""
            return str(TreePrettyPrinter(parse))


class POS:
    __POS = {
        "CC": "coordinating conjunction",
        "CD": "cardinal digit",
        "DT": "determiner",
        "EX": "existential there",
        "FW": "foreign word",
        "IN": "preposition / subordinating conjunction",
        "JJ": "adjective",
        "JJR": "adjective, comparative",
        "JJS": "adjective, superlative",
        "LS": "list marker",
        "MD": "modal",
        "NN": "noun, singular",
        "NNS": "noun, plural",
        "NNP": "proper noun, singular",
        "NNPS": "proper noun, plural",
        "PDT": "predeterminer",
        "POS": "possessive ending",
        "PRP": "personal pronoun",
        "PRP$": "possessive pronoun",
        "RB": "adverb",
        "RBR": "adverb, comparative better",
        "RBS": "adverb, superlative best",
        "RP": "particle",
        "TO": "to go",
        "UH": "interjection",
        "VB": "verb, base form",
        "VBD": "verb, past tense",
        "VBG": "verb, gerund / present participle",
        "VBN": "verb, past participle",
        "VBP": "verb, singular present",
        "VBZ": "verb, third person singular present",
        "WDT": "wh-determiner",
        "WP": "wh-pronoun",
        "WP$": "possessive wh-pronoun",
        "WRB": "wh-adverb",
    }

    @staticmethod
    def get_pos(word: str) -> str:
        word_ = [word]
        return f"{POS.__POS[nltk.pos_tag(word_)[0][1]]}"
