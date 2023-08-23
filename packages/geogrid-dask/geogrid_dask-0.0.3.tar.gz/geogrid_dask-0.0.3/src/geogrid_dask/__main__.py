"""Command-line interface."""
import click
import uvicorn

from .server.main import app


@click.command()
@click.version_option()
def main() -> None:
    """Geogrid Dask."""
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    main(prog_name="geogrid-dask")  # pragma: no cover
