import nltk
from nltk.stem import PorterStemmer
from document import Document
from store import DocumentStoreFactory
from store import TermStoreFactory
from document import TermFactory


class TextParser:
    @classmethod
    def parse(cls, text):
        words = nltk.word_tokenize(text)
        words = cls.stem_words(words)
        return words
 
    @classmethod
    def stem_words(cls, words):
        ps = PorterStemmer()
        return [ps.stem(word) for word in words]


class DocumentParser:
    @classmethod
    def parse_document(cls, url, raw_text):
        words = TextParser.parse(raw_text)
        term_store = TermStoreFactory.get_store()

        doc = Document(url)
        doc_terms = []
        for index, word in enumerate(words):
            term_id = term_store.add_term(word)
            term = TermFactory.create(term_id, word, index)
            doc_terms.append(term)

        doc.terms = doc_terms

        doc_store = DocumentStoreFactory.get_store()
        doc_store.add_document(doc)

        return doc
