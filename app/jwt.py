import json

from sdc.crypto.key_store import KeyStore
from sdc.crypto.key_store import validate_required_keys
from structlog import get_logger

logger = get_logger('respondent-home')


def key_store(keys: str) -> KeyStore:
    secrets = json.loads(keys)

    logger.info("Validating key file")
    validate_required_keys(secrets, "authentication")

    return KeyStore(secrets)
