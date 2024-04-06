import re
import math
from document import Document


class Collection:
    
    _document_counter = 0

    def __init__(self):
        """Constructor"""
        ## for every item in the sample value, add to index.
        _index = (
        {}
    )

    def add_document_to_index(self, doc: Document) -> None:
        """adds a document into the collection's inverted index

        Args:
            doc (Document): the document to be added.
        """
        # Remove whitespaces, punctuation and create list of all words in doc. 
        punctuationless = re.sub(r"[.,\/#!$%\^&\*;:{}=\-_`~()]", "", doc.get_body())
        final_string = re.sub(r"\s{2,}", " ", punctuationless)
        document_array = final_string.split()

        # Build a temporary index containing the term frequency of all terms in this document.
        temp_index = {}
        for term in document_array:
            if term in temp_index:
                temp_index[term] += 1
            else:
                temp_index[term] = 1

        # add all data to the main inverted index
        for doc_term in temp_index.keys():
            if doc_term in self._index:
                self._index[doc_term].append((doc, temp_index[doc_term]))
            else:
                self._index[doc_term] = [(doc, temp_index[doc_term])]
                
        self._increment_docs()
    
    def print_index(self):
        """prints contents of index. Used for testing
        """
        for term in self._index.keys():
            print("term: " + str(term))
            for doc in self._index[term]:
                print("    -> " + str(doc[1]) + " in: " + str(doc[0].get_id()))
                
    def _increment_docs(self) -> None: 
        """increments the number of documents by 1
        """
        self._document_counter += 1
        
    def get_df(self, term: str) -> int:
        """finds the document frequency (df) of a term in the collection

        Args:
            term (str): term to search for

        Raises:
            ValueError: when the term is not in the collection

        Returns:
            int: document frequency of a term in the collection
        """
        if term in self._index:
            return len(self._index[term])
        else:
            raise ValueError(term + " does not appear in the collection")
        
    def get_idf(self, term: str) -> float: 
        """gets the inverse document frequency (idf) of a term

        Args:
            term (str): term being searched

        Returns:
            float: idf of the term
        """
        try: 
            return math.log(self._document_counter/float(self.get_df(term)))
        except ValueError as e: 
            print("An error occured: ", e)
        
    def get_tf(self, term: str, document: Document) -> int: 
        """finds the term frequency (tf) of a term in a document

        Args:
            term (str): term to search the collection for
            document (Document): document the term frequency is being checked for

        Raises:
            ValueError: if the term is not in the collection
            ValueError: if an existing term is not found in the specified document

        Returns:
            int: term frequency (tf) of a term in a document
        """
        if not term in self._index:
            raise ValueError(term + " is not in the collection")
        for tuple in self._index[term]:
            if tuple[0] == document:
                return tuple[1]
        raise ValueError("the document doesn't contain the term")
        

    def get_tfidf(self, term: str, document: Document) -> float: 
        """gets the tf-idf weighting of the term for a given document

        Args:
            term (str): term being queried
            document (Document): document to search for

        Returns:
            float: tf-idf weighting of the term in the document vector
        """
        try: 
            return self.get_tf(term, document) * self.get_idf(term)
        except ValueError as e: 
            print("An error occured: ", e)
            