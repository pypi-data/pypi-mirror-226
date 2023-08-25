"""This module is used internally to handle cryptography actions.
It can be used as a stand-alone module with all static function.
That said the module has some internal state that doesn't work well in parallel threads."""

from cryptography.fernet import Fernet
from cryptography.exceptions import InvalidSignature

_enryption_key = None

def generate_key():
    """Genereate a new cryptographically safe key for AES encryption.

    Returns:
        bytes: A 128-bit AES key.
    """
    return Fernet.generate_key()

def set_key(key:bytes):
    """Set the key used by the module in all subsequent encrypt/decrypt calls

    Args:
        key: A 128-bit AES key. See crypto_util.generate_key.
    """
    if not validate_key(key):
        raise ValueError("The given key is not a valid 128-bit AES key.")
    
    global _enryption_key # pylint: disable=global-statement
    _enryption_key = key

def encrypt_string(data: str) -> str:
    """Encrypt a string using AES encryption. The encryption key should be set
    using crypto_util.set_key before calling this function.

    Args:
        data: The string to encrypt.

    Raises:
        RuntimeError: If the encryption hasn't been set before calling this function.

    Returns:
        str: A string representation of the encrypted bytes.
    """
    if not _enryption_key:
        raise RuntimeError("Encryption key has not been set. Use crypto_util.set_key before encrypting.")

    data = data.encode()
    data = Fernet(_enryption_key).encrypt(data)
    return data.decode()

def decrypt_string(data:str) -> str:
    """Decypt an AES encrypted string. The encryption key should be set
    using crypto_util.set_key before calling this function.

    Args:
        data: The encrypted string to decrypt.

    Raises:
        RuntimeError: If the encryption hasn't been set before calling this function.
        ValueError: If the decryption key doesn't match the encryption key used to encrypt the string.

    Returns:
        str: The decrypted string.
    """    

    if not _enryption_key:
        raise RuntimeError("Encryption key has not been set. Use crypto_util.set_key before encrypting.")

    try:
        data = data.encode()
        data = Fernet(_enryption_key).decrypt(data)
        return data.decode()
    except InvalidSignature as e:
        raise ValueError("Couldn't verify signature. The decryption key is not the same as the encryption key.") from e

def validate_key(key:bytes) -> bool:
    """Validates that a key is a valid 128-bit AES key.

    Args:
        key: The key to validate.

    Returns:
        bool: True if the key is a valid 128-bit AES key.
    """
    try:
        Fernet(key)
        return True
    except ValueError:
        return False
