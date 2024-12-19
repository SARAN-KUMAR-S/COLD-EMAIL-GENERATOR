import pandas as pd 
import chromadb
import uuid

class Portfolio:
    def __init__(self):
        self.df = pd.read_csv("my_portfolio.csv")
        self.client = chromadb.PersistentClient('vectorstore')
        self.collection = self.client.get_or_create_collection(name="portfolio")
    
    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.df.iterrows():
                self.collection.add(documents=row["Techstack"],
                            metadatas={"links": row["Links"]},
                            ids=[str(uuid.uuid4())])


    def query_links(self, skills):
        return self.collection.query(query_texts=skills).get('metadatas',[])