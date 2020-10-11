#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Optional

import click
from semantic_version import Version

from .utils import run, get_version, set_version, VersionFragment, normalize_version, METADATA_FILE
from .utils import git_get_remote_name, git_is_clean

# TODO: Consider combining bump version and tag release


@click.command()
@click.pass_context
@click.option('--upstream-url', type=str, default="https://github.com/themetadb/backend.git", show_default=True)
@click.option('--branch', type=str, default="master", show_default=True)
@click.option('--version', type=Version, required=False, help='Set version.\nConflicts with bump.', callback=lambda ctx, param, val: normalize_version(val) if val else None)
@click.option('--yes', type=bool, is_flag=True, help="Answer yes to all questions (non-interactive mode).")
@click.option('--pretend', type=bool, is_flag=True, help="Print bumped version and exit.")
@click.option('bump', '--bump', type=click.Choice([e.name.lower() for e in VersionFragment], case_sensitive=False),
              help='What part of the version number to bump.\nmajor.minor.patch(-[alpha|beta|rc].pre)')
@click.option('bump', '--major', is_flag=True, flag_value=VersionFragment.MAJOR.name, help='--bump=major')
@click.option('bump', '--minor', is_flag=True, flag_value=VersionFragment.MINOR.name, help='--bump=minor')
@click.option('bump', '--patch', is_flag=True, flag_value=VersionFragment.PATCH.name, help='--bump=patch')
@click.option('bump', '--pre', '--pre-release', is_flag=True, flag_value=VersionFragment.PRE.name, help='--bump=pre')
def cli(ctx: click.Context,
        upstream_url: str,
        branch: str,
        version: Optional[Version],
        yes: bool,
        pretend: bool,
        bump: Optional[str],
        ) -> None:

    if version is not None and bump is not None:
        ctx.fail('You can specify only one of --version or --bump, not both.')

    elif version is None and bump is None:
        ctx.fail('You must specify one of --version or --bump.')

    elif version is None:
        version = get_version()

    new_version: Version = normalize_version(version)
    if bump is not None:
        bump_fragment = VersionFragment[bump.upper()]

        if bump_fragment is VersionFragment.MAJOR:
            new_version = version.next_major()

        elif bump_fragment is VersionFragment.MINOR:
            new_version = version.next_minor()

        elif bump_fragment is VersionFragment.PATCH:
            new_version = version.next_patch()

        elif bump_fragment is VersionFragment.PRE:
            if not version.prerelease:
                ctx.fail(f'Prerelease bump specified, but no prerelease in existing version {version}. Use --version to set one.')
            new_version.prerelease = (version.prerelease[0], str(int(version.prerelease[1]) + 1))

    click.echo(new_version)
    del version

    if pretend:
        ctx.exit(0)

    if not git_is_clean(untracked=False):
        ctx.fail('Git working directory is not clean.')

    upstream = git_get_remote_name(upstream_url)
    if upstream is None:
        ctx.fail('Unable to determine the upstream repository.')

    # Fetch latest commits from upstream
    fetch_res = run(['git', 'fetch', upstream, branch])
    if fetch_res.returncode:
        click.echo(fetch_res.stdout)
        click.echo(fetch_res.stderr, err=True)
        ctx.fail(f'Unable to fetch {upstream} {branch}')

    create_branch: bool = False
    if not yes:
        create_branch = click.confirm('Create new branch and commit version bump?', default=True, show_default=True)

    new_branch = f'bump_{new_version}'

    if yes or create_branch:
        # Create new branch
        checkout_r = run(['git', 'checkout', '-b', new_branch, f'{upstream}/{branch}'])
        if checkout_r.returncode:
            click.echo(checkout_r.stdout)
            click.echo(checkout_r.stderr, err=True)
            ctx.fail(f'Failed to create {new_branch} from {branch}')
        del checkout_r

    # Write new version to file
    set_version(new_version)

    if yes or create_branch:
        # Commit version
        add_r = run(['git', 'add', METADATA_FILE])
        if add_r.returncode:
            click.echo(add_r.stdout)
            click.echo(add_r.stderr, err=True)
            ctx.fail(f'Failed to git add {METADATA_FILE}')
        del add_r

        commit_r = run(['git', 'commit', f'--message=Bump version to {new_version}'])
        if commit_r.returncode:
            click.echo(commit_r.stdout)
            click.echo(commit_r.stderr, err=True)
            ctx.fail('Failed to commit')
        del commit_r

    if yes or (create_branch and click.confirm(f'Push to {upstream}?', default=True, show_default=True)):
        # Push bump branch to upstream
        push_r = run(['git', 'push', f'--set-upstream={upstream}', new_branch])
        click.echo(push_r.stdout)
        if push_r.returncode:
            click.echo(push_r.stderr, err=True)
            ctx.fail(f'Failed to push {new_branch} to {upstream}')
        del push_r

    # TODO: pull-request


if __name__ == '__main__':
    cli()
