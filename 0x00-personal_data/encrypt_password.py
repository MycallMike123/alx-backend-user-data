#!/usr/bin/env python3
"""
Password Encryption and Validation Module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Generates a salted hashed password.
    Args:
        password (str): Plain text password.
    Returns:
        bytes: Salted, hashed password byte string.
    """
    encoded = password.encode()
    hashed = bcrypt.hashpw(encoded, bcrypt.gensalt())

    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates password against hashed password.
    Args:
        hashed_password (bytes): Hashed password byte string.
        password (str): Plain text password.
    Returns:
        bool: True if password matches; otherwise False.
    """
    valid = False
    encoded = password.encode()
    if bcrypt.checkpw(encoded, hashed_password):
        valid = True
    return valid
