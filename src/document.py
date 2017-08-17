import uuid
from urllib.parse import urlparse


class TermFactory:
    @classmethod
    def create(cls, term_id, name, offset):
        return Term(term_id, name, offset)

class Term:
    def __init__(self, term_id, name, offset=None):
        self._name = name
        self._term_id = term_id
        self._offset = offset

    @property
    def term_id(self):
        return self._term_id

    @property
    def name(self):
        return self._name

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        self._offset = offset

    def __repr__(self):
        return "Term(name=%s, offset=%d)"%(self.name, self.offset)




class Document:
    def __init__(self, url):
        self._url = url
        self._id =  self.get_hash(url)      
        self._domain = None
        self._outgoing_links = set()
        self._terms = list()

    def get_hash(self, _id):
        # uuid.uuid5(uuid.NAMESPACE_OID, url)

        return _id

    @property
    def url(self):
        return self._url

    @property
    def doc_id(self):
        return self._id

    @property
    def domain(self):
        if self._domain is None:
            self._domain = urlparse(self._url).netloc
        return self._domain

    @property
    def outgoing_links(self):
        return self._outgoing_links

    @property
    def terms(self):
        return self._terms

    @terms.setter
    def terms(self, terms):
        self._terms = terms

    def __repr__(self):
        doc = "Document(url=%s, domain=%s)"%(self.url, self.domain)
        terms_info = ""
        for term in self.terms:
            terms_info += (repr(term) + ",")

        return doc + terms_info + "\n"
