import pytest
from src.services.qdrant_service import QdrantService
from src.services.embedding_service import EmbeddingGenerator


TEST_COLLECTION = "test_kb"
VECTOR_SIZE = 384


@pytest.fixture
def qdrant():
    return QdrantService()


@pytest.fixture
def embedder():
    return EmbeddingGenerator()


# ----------------- Collection -----------------

def test_create_collection(qdrant):
    qdrant.ensure_collection(TEST_COLLECTION, VECTOR_SIZE)

    collections = qdrant.list_collections()

    assert TEST_COLLECTION in collections


def test_create_collection_idempotent(qdrant):
    qdrant.ensure_collection(TEST_COLLECTION, VECTOR_SIZE)
    qdrant.ensure_collection(TEST_COLLECTION, VECTOR_SIZE)  # should not fail


# ----------------- Insert -----------------

def test_upsert_single_point(qdrant, embedder):
    qdrant.ensure_collection(TEST_COLLECTION, VECTOR_SIZE)

    vec = embedder.embed_single("single test document")

    qdrant.add_document(
        collection_name=TEST_COLLECTION,
        doc_id=1,
        vector=vec,
        payload={
            "title": "Test",
            "content": "Single insert test",
            "category": "test"
        }
    )

    docs = qdrant.list_documents(TEST_COLLECTION)

    assert len(docs) >= 1


def test_upsert_multiple_points(qdrant, embedder):
    qdrant.ensure_collection(TEST_COLLECTION, VECTOR_SIZE)

    texts = ["doc one", "doc two", "doc three"]
    vectors = embedder.embed_batch(texts)

    for i, vec in enumerate(vectors, start=10):
        qdrant.add_document(
            collection_name=TEST_COLLECTION,
            doc_id=i,
            vector=vec,
            payload={
                "title": f"Doc {i}",
                "content": texts[i - 10],
                "category": "batch"
            }
        )

    docs = qdrant.list_documents(TEST_COLLECTION)

    assert len(docs) >= 3


# ----------------- Search -----------------

def test_search_returns_results(qdrant, embedder):
    qdrant.ensure_collection(TEST_COLLECTION, VECTOR_SIZE)

    query_vec = embedder.embed_single("test document")

    results = qdrant.search_documents(
        collection_name=TEST_COLLECTION,
        query_vector=query_vec,
        limit=5
    )

    assert isinstance(results, list)


def test_search_with_filter(qdrant, embedder):
    qdrant.ensure_collection(TEST_COLLECTION, VECTOR_SIZE)

    vec = embedder.embed_single("filtered document")

    qdrant.add_document(
        collection_name=TEST_COLLECTION,
        doc_id=100,
        vector=vec,
        payload={
            "title": "Filtered",
            "content": "Filtered search test",
            "category": "filter_test"
        }
    )

    query_vec = embedder.embed_single("filtered document")

    results = qdrant.search_documents_with_filter(
        collection_name=TEST_COLLECTION,
        query_vector=query_vec,
        limit=5,
        category="filter_test"
    )

    assert len(results) > 0

    for r in results:
        assert r.payload["category"] == "filter_test"


def test_search_empty_collection(qdrant, embedder):
    empty_collection = "empty_test_collection"

    qdrant.ensure_collection(empty_collection, VECTOR_SIZE)

    q_vec = embedder.embed_single("nothing here")

    results = qdrant.search_documents(
        collection_name=empty_collection,
        query_vector=q_vec,
        limit=5
    )

    assert results == []


# ----------------- Pagination -----------------

def test_scroll_pagination(qdrant):
    result = qdrant.list_documents_paginated(
        collection_name=TEST_COLLECTION,
        limit=2,
        offset=0
    )

    assert "points" in result
    assert "next_offset" in result


# ----------------- Delete -----------------

def test_delete_collection(qdrant):
    qdrant.ensure_collection("delete_test", VECTOR_SIZE)

    qdrant.delete_collection("delete_test")

    collections = qdrant.list_collections()

    assert "delete_test" not in collections
