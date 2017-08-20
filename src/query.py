import operator

from parser import TextParser
from expression import ExpressionTree

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

    def evaluate_query(self, query_text):
        query_tokens = QueryParser.parse_query(query_text)
        exp_tree = ExpressionTree(query_tokens)

        root_node = exp_tree.build_tree()

        results = self.accumulate_results(root_node)

        print(results)
        return results

    def accumulate_results(self, node):
        if not node:
            return

        if node.is_operand():
            term = node.token.get_term()
            results = set()
            if node.token.is_phrase():
                results = self.evaluate_phrase(term)
            else:
                term_id = self.term_store.get_id_for_term(term)
                index = self.get_default_index()
                results = index.evaluate_owq(term_id)

            print("Results for ", term,results)
            return results

        left_results = self.accumulate_results(node.left)
        right_results = self.accumulate_results(node.right)

        if node.token.get_term() == "AND":
            return operator.and_(left_results, right_results)
        if node.token.get_term() == "OR":
            return operator.or_(left_results, right_results)

        if node.token.get_term() == "NOT":
            return operator.sub(left_results, right_results)


class QueryTokenType:
    ONE_WORD = 0
    COMPOUND_WORD = 1
    PHRASE = 2

class QueryToken:
    def __init__(self, token):
        self._token = token

    def __repr__(self):
        return "QT(token='%s', is_operator=%d, is_phrase=%d"%(self._token,
                self.is_operator(), self.is_phrase())

    def is_operator(self):
        return self._token in ["AND", "OR", "NOT"]

    def is_phrase(self):
        return self._token.startswith("'") or self._token.startswith('"')

    def get_term(self):
        return self._token


class ParseToken:
    def __init__(self, token):
        self._token = token

    def __repr__(self):
        return "QT(token='%s', words=[%s])"%(self._token,
             ", ".join(self.get_words()))

    def __add__(self, ch):
        self._token += ch
        return self

    def get_words(self):
        token = self._token.strip()
        if token.startswith("'") or token.startswith('"'):
            return [token]
        return token.split()

    def is_empty(self):
        return self._token == ""

    @classmethod
    def get_empty_token(self):
        return ParseToken("")

class QueryParser:

    @classmethod
    def parse_query(cls, query_text):
        infix_tokens = cls.generate_infix_tokens(query_text)
        tokens = cls.get_postfix(infix_tokens)
        return tokens

    @classmethod
    def generate_infix_tokens(cls, query_text):
        tokens = []

        token = ParseToken("")
        processing_token = False

        for ch in query_text:
            print("Processing ", ch, "last token ", token)
            if ch in ['(']:
                if not token.is_empty():
                    tokens.append(token)
                    token = ParseToken.get_empty_token()

                tokens.append(ParseToken(ch))
            elif ch in ['"',  "'"]:
                print("Processing ", ch, "processing token", processing_token)

                token += ch
                if processing_token:
                    tokens.append(token)

                    token = ParseToken("")
                    processing_token = False
                else:
                    processing_token = True
            elif ch in [")"]:
                words = token.get_words()
                if not token.is_empty():
                    tokens.append(token)
                tokens.append(ParseToken(ch))
                token = ParseToken.get_empty_token()
            else:
                token += ch

        if not token.is_empty():
            tokens.append(token)

        return tokens

    @classmethod
    def get_postfix(cls, tokens):
        oper_stack = []
        postfix = []

        for token in tokens:
            words = token.get_words()
            for word in words:
                print(word, oper_stack, postfix)
                if word == "(":
                    oper_stack.append(word)
                elif word in ["AND", "OR", "NOT"]:
                    while oper_stack:
                        top = oper_stack.pop()
                        if top == "(":
                            break
                        postfix.append(top)
                    oper_stack.append(word)
                elif word == ")":
                    while oper_stack and oper_stack[-1] != "(":
                        postfix.append(oper_stack.pop())
                    if oper_stack:
                        oper_stack.pop()
                else:
                    postfix.append(word)

        while oper_stack:
            top = oper_stack.pop()
            if top != "(":
                postfix.append(top)
        postfix = [QueryToken(token) for token in postfix]
        return postfix
