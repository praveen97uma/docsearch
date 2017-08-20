
class Node:
    def __init__(self, token):
        self._token = token
        self.left = None
        self.right = None

    def __repr__(self):
        return repr(self._token)

    def is_operator(self):
        return self._token.is_operator()

    def is_operand(self):
        return not self.is_operator()

    @property
    def token(self):
        return self._token

class ExpressionTree:
    def __init__(self, postfix_tokens):
        self._tokens = postfix_tokens
        self._root = None

    def build_tree(self):
        aux = []
        print(self._tokens)
        for token in self._tokens:
            print(token)
            if not token.is_operator():
                aux.append(Node(token))
            else:
                node = Node(token)
                n1 = aux.pop()
                n2 = aux.pop()

                node.left = n2
                node.right = n1
                aux.append(node)

        self._root = aux.pop()
        return self._root

    def inorder(self):
        return self._inorder(self._root)

    def _inorder(self, node):
        if not node:
            return

        self._inorder(node.left)
        print(node)
        self._inorder(node.right)
