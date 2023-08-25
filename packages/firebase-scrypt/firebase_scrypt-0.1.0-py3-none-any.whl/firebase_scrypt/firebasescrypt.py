"""Python implementation of Firebase's customized scrypt password hashing algorithm

See: https://github.com/firebase/scrypt/issues/2#issuecomment-548203625

1. Decrypt the User's salt, and Project's base64_signer_key and base64_salt_separator from base64.

2. Run scrypt function with the parameters:
    password = User's password
    salt = User's salt + salt_separator
    options.N = 2 ^ mem_cost
    options.r = rounds
    options.p = 1

    This generates a derived key used in encryption.

3. Take the returned derived key, and run AES on it, with the key being the derived key, and the input being the project's signer_key (decrypted from base64).

4. Encode the result using base64 to finalize hash creation
"""
### IMPORTS
### ============================================================================
## Standard Library
import base64
import hashlib
import hmac

# Union required until python 3.10
from typing import Union

## Installed
from Crypto.Cipher import AES

## Application


### FUNCTIONS
### ============================================================================
def generate_derived_key(
    password: str,
    salt: Union[str, bytes],
    salt_separator: Union[str, bytes],
    rounds: int,
    mem_cost: int,
) -> bytes:
    """Generates derived key from known parameters

    `password` is the user's password as a `utf-8` string.
    `salt`, `salt_separator` can be passed in as either `bytes` or a `base64` encoded string.
    """

    n = 2**mem_cost  # pylint: disable=invalid-name
    p = 1  # pylint: disable=invalid-name

    if isinstance(salt, str):
        salt = base64.b64decode(salt)

    if isinstance(salt_separator, str):
        salt_separator = base64.b64decode(salt_separator)

    derived_key = hashlib.scrypt(
        password=bytes(password, "utf-8"),
        salt=salt + salt_separator,
        n=n,
        r=rounds,
        p=p,
    )

    return derived_key


def encrypt(signer_key: bytes, derived_key: bytes) -> bytes:
    """Encrypts signer key with derived key using AES256

    NOTE: We're only using first 32 bytes of the derived key to match
    expected key length.

    Nonce is fixed and IV-vector is basically 16 null bytes (counter starting from 0).

    See: https://pycryptodome.readthedocs.io/en/latest/src/faq.html#is-ctr-cipher-mode-compatible-with-java
    """
    key = derived_key[:32]
    iv = b"\x00" * 16  # pylint: disable=invalid-name
    nonce = b""
    cipher = AES.new(key, AES.MODE_CTR, initial_value=iv, nonce=nonce)
    return cipher.encrypt(signer_key)


def verify_password(
    password: str,
    known_hash: str,
    salt: Union[str, bytes],
    salt_separator: Union[str, bytes],
    signer_key: Union[str, bytes],
    rounds: int,
    mem_cost: int,
) -> bool:
    """Verify if password matches known hash"""
    derived_key: bytes = generate_derived_key(password, salt, salt_separator, rounds, mem_cost)

    if isinstance(signer_key, str):
        signer_key = base64.b64decode(signer_key)

    result = encrypt(signer_key, derived_key)

    password_hash = base64.b64encode(result).decode("utf-8")

    return hmac.compare_digest(password_hash, known_hash)
