from enum import Enum

class ResponseConstants(Enum):
    SUCCESS = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    FILE_NOT_FOUND = "File not found"
    FILE_UPLOAD_SUCCESS = "File uploaded successfully"
    FILE_SIZE_EXCEEDED = "File size exceeds the maximum limit"
    FILE_INVALID_CONTENT_TYPE = "Invalid content type"
    FILE_PROCESSING_FAILED = "File processing failed"
    FILE_PROCESSING_SUCCESS = "File processing success"
    NO_FILES_ERROR = "not_found_files"
    PROJECT_NOT_FOUND_ERROR = "project_not_found"
    INSERT_INTO_DATABASE_ERROR = "insert_into_database_error"
    INSERT_INTO_DATABASE_SUCCESS = "insert_success_into_vector_db"
    VECTORDB_COLLECTION_RETRIEVED = "vectordb_collection_retrived"
    VECTORDB_SEARCH_ERROR = "vectordb_search_error"
    VECTORDB_SEARCH_SUCCESS = "vectordb_search_success"

