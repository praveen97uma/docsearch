
from parser import DocumentParser
from store import DocumentStoreFactory, TermStoreFactory
from index import IndexFactory
from parser import TextParser


url1 = "https://stackoverflow.com/questions/9626535/get-domain-name-from-url"

text1 = "Extracting domain from URL in python"
text2 = "How to Get Domain Name from URL String domain in Python"
text3 = "How to automatically extract domain from URL through conf files at search-time"
url3 = "https://answers.splunk.com/answers/188774/how-to-automatically-extract-domain-from-url-throu.html"
url2 = "https://ashiknesin.com"


doc1 = DocumentParser.parse_document(url1, text1)
doc2 = DocumentParser.parse_document(url2, text2)
doc3 = DocumentParser.parse_document(url3, text3)

doc_store = DocumentStoreFactory.get_store()
print(doc_store._data)

index = IndexFactory.get_or_create_index("default")

index.add_document(doc1)
index.add_document(doc2)
index.add_document(doc3)

index.display()

from query import QueryEvaluator

qeval = QueryEvaluator(IndexFactory, TermStoreFactory)


query = "extracting domain"
docs = qeval.evaluate_phrase(query)
print("INTERSECT RESULT")
print(docs)
