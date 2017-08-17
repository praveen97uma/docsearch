import uuid


class DocumentStoreFactory:
    _store = None

    @classmethod
    def get_store(cls):
        if cls._store is None:
            cls._store = DocumentStore()
        return cls._store


class DocumentStore:
    def __init__(self):
        self._data = {}

    def has_document(self, document):
        return document.doc_id in self._data

    def add_document(self, document):
       self._data[document.doc_id] = document 

    def get_document(self, doc_id):
        return self._data.get(doc_id)



class TermStoreFactory:
    _store = None

    @classmethod
    def get_store(cls):
        if cls._store is None:
            cls._store = TermStore()
        return cls._store


class TermStore:
    def __init__(self):
        self._data = {}

    def get_term_by_id(self, term_id):
        return self._data.get(term_id)

    def generate_hash(self, term):

        #term_id = uuid.uuid5(uuid.NAMESPACE_OID, term)
        return term

    def get_id_for_term(self, term):
        return self.generate_hash(term)

    def add_term(self, term):
        term_id = self.generate_hash(term)
        self._data[term_id] = term

        return term_id
