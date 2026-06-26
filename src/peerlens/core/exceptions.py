class PeerLensError(Exception):
    """Base error for PeerLens."""


class IngestionError(PeerLensError):
    """Paper could not be fetched or parsed."""


class IdentifierError(PeerLensError):
    """Identifier format is invalid or unsupported."""


class RAGError(PeerLensError):
    """RAG / Q&A pipeline failed."""
