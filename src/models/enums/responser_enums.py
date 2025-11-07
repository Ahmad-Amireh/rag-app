from enum import Enum

class ResponseSignal(Enum): 
    FILE_VALIDATED_SUCCESS = "file_validate_success"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "file_upload_success"
    FILE_UPLOAD_FAIL = "file_upload_fail"
    PROCESSING_SUCCESS = "processing_success"
    PROCESSING_FAILD = "processing_faild"
    NO_FILES_ERRORS = "not_found_files"
    FILE_ID_ERROR = "no_file_found_with_this_id"
    PROJECT_NOT_FOUND_ERROR= "project_not_found"
    INSERT_INTO_VECTORDB_ERROR="inser_into_vectordb_error"
    INSERT_INTO_VECTORDB_SUCCESS="inser_into_vectordb_success"
    VECTORDB_COLLECTION_RETRIEVED= "vector_collection_retrieved"
    VECTOR_SEARCH_ERROR = "vector_search_error"
    VECTOR_SEARCH_SUCCESS = "vector_search_success"
