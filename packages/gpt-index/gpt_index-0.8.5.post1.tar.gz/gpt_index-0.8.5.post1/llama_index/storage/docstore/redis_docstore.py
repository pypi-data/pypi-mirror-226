from typing import Optional, Any
from llama_index.storage.docstore.keyval_docstore import KVDocumentStore
from llama_index.storage.kvstore.redis_kvstore import RedisKVStore


class RedisDocumentStore(KVDocumentStore):
    """Redis Document (Node) store.

    A Redis store for Document and Node objects.

    Args:
        redis_kvstore (RedisKVStore): Redis key-value store
        namespace (str): namespace for the docstore

    """

    def __init__(
        self,
        redis_kvstore: RedisKVStore,
        namespace: Optional[str] = None,
    ) -> None:
        """Init a RedisDocumentStore."""
        super().__init__(redis_kvstore, namespace)
        # avoid conflicts with redis index store
        self._node_collection = f"{self._namespace}/doc"

    @classmethod
    def from_redis_client(
        cls,
        redis_client: Any,
        namespace: Optional[str] = None,
    ) -> "RedisDocumentStore":
        """Load a RedisDocumentStore from a Redis Client."""
        redis_kvstore = RedisKVStore.from_redis_client(redis_client=redis_client)
        return cls(redis_kvstore, namespace)

    @classmethod
    def from_host_and_port(
        cls,
        host: str,
        port: int,
        namespace: Optional[str] = None,
    ) -> "RedisDocumentStore":
        """Load a RedisDocumentStore from a Redis host and port."""
        redis_kvstore = RedisKVStore.from_host_and_port(host, port)
        return cls(redis_kvstore, namespace)
