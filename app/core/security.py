import base64
import binascii
import hashlib
import hmac
import json
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

from app.core.config import (
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_SECRET_KEY,
)

JWT_ALGORITHM = "HS256"
PASSWORD_HASH_ALGORITHM = "pbkdf2_sha256"
PASSWORD_HASH_ITERATIONS = 260000


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        PASSWORD_HASH_ITERATIONS,
    ).hex()

    return (
        f"{PASSWORD_HASH_ALGORITHM}"
        f"${PASSWORD_HASH_ITERATIONS}"
        f"${salt}"
        f"${password_hash}"
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        algorithm, iterations, salt, expected_hash = hashed_password.split("$")
    except ValueError:
        return False

    if algorithm != PASSWORD_HASH_ALGORITHM:
        return False

    actual_hash = hashlib.pbkdf2_hmac(
        "sha256",
        plain_password.encode("utf-8"),
        salt.encode("utf-8"),
        int(iterations),
    ).hex()

    return secrets.compare_digest(actual_hash, expected_hash)


def create_access_token(subject: str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub": subject,
        "exp": int(expires_at.timestamp()),
    }

    return encode_jwt(payload)


def encode_jwt(payload: dict[str, Any]) -> str:
    header = {
        "alg": JWT_ALGORITHM,
        "typ": "JWT",
    }
    header_segment = base64url_encode_json(header)
    payload_segment = base64url_encode_json(payload)
    signing_input = f"{header_segment}.{payload_segment}".encode("ascii")
    signature = hmac.new(
        JWT_SECRET_KEY.encode("utf-8"),
        signing_input,
        hashlib.sha256,
    ).digest()
    signature_segment = base64url_encode(signature)

    return f"{header_segment}.{payload_segment}.{signature_segment}"


def decode_jwt(token: str) -> dict[str, Any]:
    try:
        header_segment, payload_segment, signature_segment = token.split(".")
    except ValueError as exc:
        raise ValueError("Invalid token format") from exc

    signing_input = f"{header_segment}.{payload_segment}".encode("ascii")
    expected_signature = hmac.new(
        JWT_SECRET_KEY.encode("utf-8"),
        signing_input,
        hashlib.sha256,
    ).digest()

    try:
        actual_signature = base64url_decode(signature_segment)
    except binascii.Error as exc:
        raise ValueError("Invalid token signature") from exc

    if not hmac.compare_digest(actual_signature, expected_signature):
        raise ValueError("Invalid token signature")

    try:
        header = base64url_decode_json(header_segment)
        payload = base64url_decode_json(payload_segment)
    except (binascii.Error, json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError("Invalid token payload") from exc

    if not isinstance(header, dict):
        raise ValueError("Invalid token header")

    if header.get("alg") != JWT_ALGORITHM:
        raise ValueError("Invalid token algorithm")

    if not isinstance(payload, dict):
        raise ValueError("Invalid token payload")

    expires_at = payload.get("exp")

    if not isinstance(expires_at, int):
        raise ValueError("Invalid token expiration")

    if expires_at < int(datetime.now(timezone.utc).timestamp()):
        raise ValueError("Token has expired")

    return payload


def base64url_encode_json(data: dict[str, Any]) -> str:
    json_data = json.dumps(
        data,
        separators=(",", ":"),
    ).encode("utf-8")

    return base64url_encode(json_data)


def base64url_decode_json(data: str) -> dict[str, Any]:
    decoded_data = base64url_decode(data)

    return json.loads(decoded_data)


def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def base64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)

    return base64.urlsafe_b64decode(data + padding)
