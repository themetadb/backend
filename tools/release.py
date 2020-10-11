#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from .utils import run, git_get_remote_name, get_version


@click.command()
@click.pass_context
@click.option('--upstream-url', type=str, default="https://github.com/themetadb/backend.git", show_default=True)
@click.option('--branch', type=str, default="master", show_default=True)
# @click.option('--version', type=str, default=get_version, show_default=True)
@click.option('--yes', type=bool, is_flag=True, help="Answer yes to all questions (non-interactive mode).")
def cli(ctx: click.Context, upstream_url: str, branch: str, yes: bool) -> None:
    upstream = git_get_remote_name(upstream_url)
    version = get_version()

    if upstream is None:
        ctx.fail('Unable to determine the upstream repository')

    # Fetch latest commits from upstream
    fetch_res = run(['git', 'fetch', upstream, branch])
    if fetch_res.returncode:
        click.echo(fetch_res.stdout)
        click.echo(fetch_res.stderr, err=True)
        ctx.fail(f'Unable to fetch {upstream} {branch}')

    # Display latest commit
    show_r = run(['git', 'show', f'{upstream}/{branch}'])
    click.echo(show_r.stdout)

    # Tag release
    if not yes:
        click.confirm(f'Tag this commit as release v{version}?', abort=True)
    run(['git', 'tag', '--annotate', f'--message=Release {version}', f'v{version}', f'{upstream}/{branch}'])

    # Push upstream
    if not yes:
        click.confirm(f'Push release v{version} to {upstream}?', abort=True)
    run(['git', 'push', f'--repo={upstream}', 'tag', f'v{version}'])


if __name__ == '__main__':
    cli()
