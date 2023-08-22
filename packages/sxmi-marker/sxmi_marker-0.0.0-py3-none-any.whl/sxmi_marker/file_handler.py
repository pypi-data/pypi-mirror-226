"""Main module for generating and saving ArUco markers.

Copyright (c) 2023 Stroma Vision Inc.
"""
import logging
import os


class FileHandler:
    """Handles file operations for the markers."""

    @staticmethod
    def save_marker_images(
        identifier: str, marker_images: dict[str, str], aruco_ids: dict[str, int], save_path: str = "."
    ) -> list[str]:
        """Save SVG marker images to the specified path."""
        file_paths = []
        for pos, svg_content in marker_images.items():
            svg_filename = os.path.join(save_path, f"{identifier}_{pos}_aruco_{aruco_ids[pos]}.svg")
            with open(svg_filename, "w") as svg_file:
                svg_file.write(svg_content)
            logging.info(f"Saved SVG marker at: {svg_filename}")
            file_paths.append(svg_filename)
        return file_paths
