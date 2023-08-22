"""Main module for generating and saving ArUco markers.

Copyright (c) 2023 Stroma Vision Inc.
"""
import hashlib
import re


class IdentifierHandler:
    """Handles operations related to the product identifier."""

    @staticmethod
    def is_valid(identifier: str) -> bool:
        """Check if the provided identifier follows the format: 3 alphabetical chars, a dash, and 8 alphanumeric digits."""
        pattern = re.compile(r"^[A-Za-z]{3}-[A-Za-z0-9]{8}$")
        return bool(pattern.match(identifier))

    @staticmethod
    def map_to_product_id(alphanumeric: str) -> int:
        """Map an alphanumeric string to a product ID using SHA-256 for uniform distribution."""
        sha256_hash = hashlib.sha256(alphanumeric.encode()).hexdigest()
        int_value = int(sha256_hash, 16)
        product_id = int_value % 250 + 1
        return product_id
