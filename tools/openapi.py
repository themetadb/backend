#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from typing import IO

import click
from themetadb.backend.app import app


@click.command()
@click.option('--output', type=click.File('wt', encoding='utf-8'), default='openapi.json', show_default=True)
def cli(output: IO[str]) -> None:
    openapi = app.openapi()

    json.dump(openapi, output, indent=2)


if __name__ == '__main__':
    cli()
