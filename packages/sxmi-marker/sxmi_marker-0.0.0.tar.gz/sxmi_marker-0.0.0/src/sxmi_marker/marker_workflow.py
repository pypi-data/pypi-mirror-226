"""Main module for generating and saving ArUco markers.

Copyright (c) 2023 Stroma Vision Inc.
"""
import logging

from sxmi_marker.file_handler import FileHandler
from sxmi_marker.identifier_handler import IdentifierHandler
from sxmi_marker.marker_generator import MarkerGenerator


class MarkerWorkflow:
    """Main workflow for generating and saving ArUco markers."""

    def __init__(self):
        """Initialize the workflow with the required handlers."""
        self.identifier_handler = IdentifierHandler()
        self.marker_generator = MarkerGenerator()
        self.file_handler = FileHandler()

    def execute(self, identifier: str, save_path: str) -> list[str]:
        """Execute the workflow to generate and save markers."""
        if not self.identifier_handler.is_valid(identifier):
            logging.error("Invalid identifier format. Please provide in the format: AAA-12345678")
            return []

        product_id = self.identifier_handler.map_to_product_id(identifier)
        aruco_ids = self.marker_generator.get_aruco_ids_by_position(product_id)
        marker_images = self.marker_generator.generate_markers(aruco_ids)

        return self.file_handler.save_marker_images(identifier, marker_images, aruco_ids, save_path)
