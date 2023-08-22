"""Utils."""
import uuid


def generate_key() -> uuid.UUID:
    """Generate key."""
    return uuid.uuid4()
