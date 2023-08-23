"""Command line additions to CKAN."""

import logging

import click

from ckanext.cloudstorage_api.model import create_tables, drop_tables

log = logging.getLogger(__name__)


@click.group()
def cloudstorage_api():
    """CloudStorageApi management commands."""
    pass


@cloudstorage_api.command()
def initdb():
    """Reinitalize database tables."""
    drop_tables()
    create_tables()
    click.secho("DB tables are reinitialized", fg="green")


def get_cli_commands():
    """Gather CLI commands via click group."""
    return [cloudstorage_api]
