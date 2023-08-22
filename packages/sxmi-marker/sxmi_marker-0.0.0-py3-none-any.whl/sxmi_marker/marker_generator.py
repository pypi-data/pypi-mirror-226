"""Marker generator.

Copyright (c) 2023 Stroma Vision Inc.
"""


from importlib import resources

import numpy as np


class MarkerGenerator:
    """Handles the generation of ArUco markers."""

    def __init__(self):
        """Initialize the generator with the given ArUco dictionary."""
        aruco_file_path = resources.path("sxmi_marker", "ARUCO_DICT_7X7_1000.npz")
        with aruco_file_path as path:
            self.aruco_dict = np.load(path)["bytesList"]

    def get_aruco_ids_by_position(self, product_id: int) -> dict[str, int]:
        """Get ArUco marker IDs based on product_id and position subsets."""
        base_idx = (product_id - 1) % 250
        offsets = {"TSL": 0, "TSR": 250, "USL": 500, "USR": 750}
        return {position: base_idx + offset for position, offset in offsets.items()}

    def generate_markers(self, aruco_ids: dict[str, int]) -> dict[str, str]:
        """Generate SVG ArUco markers for the given IDs."""
        return {pos: self.generate_marker(7, 7, self.aruco_dict[aruco_id]) for pos, aruco_id in aruco_ids.items()}

    def bits_from_bytes(self, bytes_data: bytes) -> list[int]:
        """Extract the first 7 bits from the given bytes."""
        # Convert bytes to binary and concatenate
        binary_representation: str = "".join([f"{byte:08b}" for byte in bytes_data])
        # Extract the first 7 bits from the concatenated binary string
        relevant_bits: list[int] = list(map(int, list(binary_representation[:7])))
        return relevant_bits

    def generate_marker(self, width: int, height: int, bytes_data: list[bytes]) -> str:
        """Generate an SVG marker from the given bytes."""
        # Extract relevant bits from bytes
        bits = [bit for row in bytes_data for bit in self.bits_from_bytes(row)]

        # Starting SVG definition
        svg = [
            f'<svg baseProfile="full" width="{width + 2}" height="{height + 2}" xmlns="http://www.w3.org/2000/svg">',
            f'<rect x="0" y="0" width="{width + 2}" height="{height + 2}" fill="black" />',
        ]

        for i in range(height):
            for j in range(width):
                white = bits[i * width + j]
                if not white:
                    continue

                svg.append(f'<rect x="{j + 1}" y="{i + 1}" width="{1}" height="{1}" fill="white" />')

        svg.append("</svg>")
        return "\n".join(svg)
