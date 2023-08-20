# src/mewicli/main.py

from __future__ import annotations  # for Python 3.7-3.9

import os
from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def download(
    api_url: Annotated[str, typer.Option(help="URL of MediaWiki site.")] = "",
    username: Annotated[str, typer.Option(help="username of API user.")] = "",
    password: Annotated[str, typer.Option(help="password of API user.")] = "",
    filename: Annotated[
        str, typer.Option(help="Filename to wiki text to.")
    ] = "",
    pagename: Annotated[
        str, typer.Option(help="Name of the page to download.")
    ] = "",
):
    api_url = api_url or os.environ.get(
        "MEDIAWIKI_URL", "http://localhost/w/api.php"
    )
    username = username or os.environ.get("MEDIAWIKI_USERNAME", "ingrid")
    password = password or os.environ.get("MEDIAWIKI_PASSWORD", "henk123")
    filename = filename or os.environ.get("MEDIAWIKI_FILENAME", "README.wiki")
    pagename = pagename or os.environ.get(
        "MEDIAWIKI_PAGENAME", "does_not_exist"
    )

    print(f"api_url: {api_url}")
    print(f"username: {username}")
    print(f"password: {password}")
    print(f"filename: {filename}")
    print(f"pagename: {pagename}")


@app.command()
def upload(
    api_url: Annotated[str, typer.Option(help="URL of MediaWiki site.")] = "",
    username: Annotated[str, typer.Option(help="username of API user.")] = "",
    password: Annotated[str, typer.Option(help="password of API user.")] = "",
    filename: Annotated[
        str, typer.Option(help="Filename of wiki text to upload.")
    ] = "",
    pagename: Annotated[
        str, typer.Option(help="Name of the page to upload.")
    ] = "",
):
    api_url = api_url or os.environ.get(
        "MEDIAWIKI_URL", "http://localhost/w/api.php"
    )
    username = username or os.environ.get("MEDIAWIKI_USERNAME", "ingrid")
    password = password or os.environ.get("MEDIAWIKI_PASSWORD", "henk123")
    filename = filename or os.environ.get("MEDIAWIKI_FILENAME", "README.wiki")
    pagename = pagename or os.environ.get(
        "MEDIAWIKI_PAGENAME", "does_not_exist"
    )

    print(f"api_url: {api_url}")
    print(f"username: {username}")
    print(f"password: {password}")
    print(f"filename: {filename}")
    print(f"pagename: {pagename}")


if __name__ == "__main__":
    app()
