import boolean

from parser import TextParser


class QueryEvaluator:
    def __init__(self, index_factory, term_store_factory):
        self.index_factory = index_factory
        self.term_store = term_store_factory.get_store()

    def get_default_index(self):
        return self.index_factory.get_or_create_index("default")

    def evaluate_phrase(self, query_text):
        terms = self.get_terms(query_text)
        index = self.get_default_index()

        return index.evaluate_phrase_query(terms)

    def get_terms(self, query_text):
        query_terms = TextParser.parse(query_text)
        query_term_ids = [self.term_store.get_id_for_term(term) for term in
                query_terms]
        return query_term_ids
