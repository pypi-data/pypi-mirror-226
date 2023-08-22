""" A client library for accessing Chopin KMD HMDB API """
from .client import AuthenticatedClient, Client

__version__ = "1.0.0"
__all__ = (
    "AuthenticatedClient",
    "Client",
    "__version__"
)

