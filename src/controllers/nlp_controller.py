from .base_controller import BaseController
from models.db_schemas import Project, DataChunk
from typing import List
from stores.llm.LLMEnums import DocumentTypeEnums
import json
import logging


class NLPController(BaseController):
    
    def __init__(self, vectordb_client, generation_client, embedding_client):
        super().__init__()

        self.vectordb_client = vectordb_client
        self.gemeration_client = generation_client
        self.embedding_client = embedding_client
        self.logger = logging.getLogger(__name__)

    def create_collection_name(self, project_id: str):
        
        return f"collection_{project_id}".strip()
    

    def reset_vector_db_collection(self, project:Project):
        
        collection_name = self.create_collection_name(project_id= project.project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)
    
    def get_vector_db_info(self, project: Project):

        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = self.vectordb_client.get_collection_info(collection_name)

        return json.loads(
            json.dumps(collection_info, default = lambda x : x.__dict__)
        )
    
    def index_into_vector_db(self, project: Project, chunks: List[DataChunk], chunks_ids: List[int], do_reset: bool = False):

        # step1: get collection_name 
        collection_name = self.create_collection_name(project.project_id)

        # step2: manage_items 
        texts = [chunk.chunk_text for chunk in chunks]
        metadata = [chunk.chunk_metadata for chunk in chunks ]
        vectors = [self.embedding_client.embed_text(text=text, document_type=DocumentTypeEnums.DOCUMENT.value)
            for text in texts ]

        # step 3 : create collection if not exist 
        _ = self.vectordb_client.create_collection(
            collection_name = collection_name,
            embedding_size = self.embedding_client.embedding_size,
            do_reset = do_reset,
            
        )


        # step 4: insert into vector_db
        _ = self.vectordb_client.insert_many(
            collection_name = collection_name,
            texts = texts,
            metadata = metadata,
            vectors = vectors,
            record_ids = chunks_ids
            )

        return True

    def search_vector_db_collection(self, project: Project, text:str, limit:int = 5):

        #get collection name 
        collection_name = self.create_collection_name(project_id= project.project_id)

        # get embedding vector

        vector = self.embedding_client.embed_text(
            text= text,
            document_type = DocumentTypeEnums.QUERY.value,
            
        )
        

        
    # get embedding size from the client
        embedding_size = self.embedding_client.embedding_size
        self.logger.error(f"Embedding size (expected): {embedding_size}, vector length (actual): {len(vector)}")


        if not vector or len(vector)==0 :
                return False
        
            # optional: check mismatch
        if len(vector) != embedding_size:
            raise ValueError(
                f"Embedding size mismatch: expected {embedding_size}, got {len(vector)}"
            )
        # do semantic search 
        results = self.vectordb_client.search_by_vector(
            collection_name = collection_name,
            vector = vector,
            limit = limit,
            
        )

        if not results:
            return False

        return json.loads(
                json.dumps(results, default = lambda x : x.__dict__)
            )
        