import operator
from collections import defaultdict


class IndexFactory:
    _cache = {}

    @classmethod
    def get_or_create_index(cls, name):
        if name not in cls._cache:
            cls._cache[name] = StandardIndex(name)
        return cls._cache[name]

class Posting:
    def __init__(self, term_id, doc_id, pos_offsets=[]):
        self._term_id = term_id
        self._doc_id = doc_id
        self._pos_offsets = pos_offsets

    @property
    def doc_id(self):
        return self._doc_id

    @property
    def term_id(self):
        return self._term_id

    @property
    def pos_offsets(self):
        return self._pos_offsets

    def add_term_offset(self, offset):
        self._pos_offsets.append(offset)

    def __repr__(self):
        return "Posting(doc_id=%s, term_id=%s); Offsets:[%s]"%(self.doc_id,
                self.term_id,
                ",".join(str(x) for x in self.pos_offsets))

    def __eq__(self, other):
        return self.doc_id == other.doc_id and self.term_id == other.term_id

    def __hash__(self):
        return hash(str(self.doc_id) + str(self.term_id))

class StandardIndex:
    def __init__(self, name):
        self._name = name
        self._index = defaultdict(set)

    def add_document(self, document):
        doc_id = document.doc_id
        terms = document.terms

        infos = {}

        for term in terms:
            if term.term_id in infos:
                term_info = infos.get(term.term_id).add_term_offset(term.offset)
            else:
                term_info = Posting(term.term_id, doc_id, [term.offset])
                infos[term.term_id] = term_info

                self._index[term.term_id].add(term_info)


    def display(self):
        for term_id, info in self._index.items():
            print (term_id, "\t", info)

    def get_postings(self, term_id):
        return self._index.get(term_id, set())

    def get_docs(self, term_id):
        postings = self.get_postings(term_id)
        docs = set([posting.doc_id for posting in postings])
        return docs

    def _apply_operator(self, term_ids, operator):
        docs = self.get_docs(term_ids[0])
        for i in range(1, len(term_ids)):
            term_id = term_ids[i]
            docs = operator(docs, self.get_docs(term_id))
        return docs

    def get_common_docs_for_terms(self, term_ids):
        return self._apply_operator(term_ids, operator.and_)

    def get_all_docs_containing_terms(self, term_ids):
        return self._apply_operator(term_ids, operator.or_)

    def get_posting(self, term_id, doc_id):
        postings = self.get_postings(term_id)
        for posting in postings:
            if posting.doc_id == doc_id:
                return posting

    def evaluate_phrase_query(self, term_ids):
        common_docs = self.get_common_docs_for_terms(term_ids)

        matched_docs = []
        for doc_id in common_docs:
            term_positions = []
            for term_id in term_ids:
                term_positions.append(self.get_posting(term_id,
                    doc_id).pos_offsets)
            it = set(term_positions[0])
            for i in range(1, len(term_positions)):
                pos = term_positions[i]
                curr = set([p - i for p in pos])
                it = it & curr

            if it:
                matched_docs.append(doc_id)

        print("PHRASE QUERY RESULT ", term_ids, matched_docs)

        return matched_docs

    def evaluate_owq(self, term_id):
        matched_docs = self.get_docs(term_id)
        print("OWQ RESULT", term_id, matched_docs)
        return matched_docs
