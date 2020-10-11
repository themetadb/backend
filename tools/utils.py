#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import subprocess
from enum import Enum, auto
from typing import Union, Match, Pattern, Optional, Mapping, Tuple, List
from typing import cast
from ast import literal_eval
import configparser

from semantic_version import Version

BASE_PATH: str = os.path.dirname(os.path.dirname(__file__))
METADATA_FILE: str = os.path.join(BASE_PATH, 'themetadb', 'backend', '__init__.py')


def run(args: Union[Tuple[str, ...], List[str]]) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf-8',
        universal_newlines=True
    )


class VersionFragment(Enum):
    MAJOR = auto()
    MINOR = auto()
    PATCH = auto()
    PRE = auto()


PRERELEASE_MAP: Mapping[str, str] = {
    'alpha': 'alpha',
    'a': 'alpha',
    'beta': 'beta',
    'b': 'beta',
    'rc': 'rc',
}

_re_version: Pattern[str] = re.compile(r'^__version__[ \t]*=[ \t]*(?P<quote>["\'])(?P<version>.*?)(?P=quote)[ \t]*(\#.*)?$', re.MULTILINE)
_re_version_prerelease_normalization: Pattern[str] = re.compile(r'^(?P<name>[a-z]+)\.?(?P<number>[0-9]+)?$')


def normalize_version(version: Optional[Union[Version, str]]) -> Version:
    normalized = Version(str(version))

    if normalized.prerelease:
        prerelease = list(normalized.prerelease)
        if len(prerelease) == 1:
            m = re.match(_re_version_prerelease_normalization, prerelease[0])
            assert m, f"{prerelease[0]} does not match r'{_re_version_prerelease_normalization.pattern}'."
            gd = m.groupdict()
            prerelease = [cast(str, gd.get('name')), gd.get('number') or '1']

        assert prerelease[0].lower() in PRERELEASE_MAP.keys(), f"{prerelease[0].lower()} is not in {tuple(PRERELEASE_MAP.keys())}."
        assert prerelease[1].isdecimal(), f"{prerelease[1]} is not a decimal number."

        normalized.prerelease = (PRERELEASE_MAP[prerelease[0].lower()], str(int(prerelease[1])))

    return normalized


def get_version(file: Optional[str] = None) -> Version:
    if file is None:
        file = os.path.join(BASE_PATH, 'themetadb', 'backend', '__init__.py')

    with open(file, 'r') as fh:
        version_match = re.search(_re_version, fh.read())
        assert isinstance(version_match, Match), "unable to find version in {}".format(file)

    version_literal = "{quote}{version}{quote}".format(**version_match.groupdict())

    return normalize_version(cast(str, literal_eval(version_literal)))


def set_version(version: Union[Version, str], file: str = METADATA_FILE) -> None:
    with open(file, 'r') as fh:
        old = fh.read()

    new = re.sub(_re_version, '__version__ = {!r}'.format(str(version)), old)

    with open(file, 'w') as fh:
        fh.write(new)


def git_get_config() -> Mapping[str, Mapping[str, str]]:
    config = configparser.ConfigParser(default_section='core')
    config.read(os.path.join(BASE_PATH, '.git', 'config'))

    # Convert config to a dict of dicts
    return dict([(section_name, dict(config[section_name])) for section_name in config])


def git_get_remotes() -> Mapping[str, Optional[str]]:
    config = git_get_config()

    res = {}

    for section in config:
        if ' ' in section:
            section_type, section_name = section.split(' ', 1)
            section_name = section_name.strip('"')

            if section_type == 'remote':
                res[section_name] = config[section].get('url')

    return res


def git_normalize_url(url: str) -> Tuple[str, str]:
    # TODO: Handle ports, and http simple auth

    if url.endswith('.git'):
        url = url[:-4]

    if url.startswith('http'):
        url = url.split('://', 1)[1]
        host, path = url.split('/', 1)
        return (host, path)

    else:
        host, path = url.split(':', 1)
        host = host.split('@')[-1]
        return (host, path)


def git_get_remote_name(remote: Union[str, Tuple[str, str]]) -> Optional[str]:
    if isinstance(remote, str):
        remote = git_normalize_url(remote)

    for name, url in git_get_remotes().items():
        if url is None:
            continue

        normalized_url = git_normalize_url(url)

        if remote == normalized_url:
            return name

    return None


def git_is_clean(untracked: bool = True) -> bool:
    cmd = ['git', 'status', '--porcelain']
    if not untracked:
        cmd.append('--untracked-files=no')

    status_r = run(cmd)
    if status_r.returncode:
        sys.stdout.write(status_r.stdout)
        sys.stderr.write(status_r.stderr)
        return False

    if status_r.stdout.strip():
        return False

    return True
