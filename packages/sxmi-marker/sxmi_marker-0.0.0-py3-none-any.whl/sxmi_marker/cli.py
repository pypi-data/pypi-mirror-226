"""sxmi-marker CLI."""

import typer

from sxmi_marker.identifier_handler import IdentifierHandler
from sxmi_marker.marker_workflow import MarkerWorkflow

app = typer.Typer(help="CLI tool for saving SVG marker images based on a product identifier.")


def process_marker_generation(identifier: str, save_path: str = ".") -> None:
    """Process the generation and saving of SVG marker images to the specified path."""
    if not IdentifierHandler.is_valid(identifier):
        raise ValueError("The product identifier is invalid.")

    workflow = MarkerWorkflow()
    workflow.execute(identifier, save_path)


@app.command()
def generate_marker(
    identifier: str = typer.Argument(..., help="Product identifier to process."),
    save_path: str = typer.Option(".", help="Path to save marker images. Defaults to current directory."),
) -> None:
    """Save SVG marker images to the specified path."""
    try:
        process_marker_generation(identifier, save_path)
    except Exception as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1) from e


if __name__ == "__main__":
    app()
