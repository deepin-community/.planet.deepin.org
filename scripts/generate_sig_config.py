# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: LGPL-2.0-or-later

import configparser
import logging
import shutil
import yaml
import sys
import sh
import os
from typing import Any
from pathlib import Path


def val_of_key(obj: dict, key_path: list[str], fallback: Any) -> Any:
    cur_obj = obj
    while len(key_path) > 0:
        try:
            cur_obj = cur_obj[key_path.pop(0)]
        except KeyError:
            return fallback
    return cur_obj


def ensure_working_dir():
    working_dir_path = os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + "/../.temp/")
    logging.info("Working dir: {0}".format(working_dir_path))
    if not Path(working_dir_path).exists():
        logging.info("Creating that working dir...")
        os.mkdir(working_dir_path)
    os.chdir(working_dir_path)


def fetch_repo(repo_name):
    need_update = True
    repo_path = "{0}.git/".format(repo_name)
    if not Path(repo_path).exists():
        remote_url = "https://github.com/deepin-community/{0}".format(repo_name)
        logging.info("Mirror cloning {0} from {1}".format(repo_name, remote_url))
        sh.git.clone(remote_url, mirror=True, depth=1, _out=sys.stdout, _err=sys.stderr)
        need_update = False
    git = sh.git.bake('-C', repo_path, _tty_out=False)
    if need_update:
        logging.info("Uploading mirror repo {0}".format(repo_name))
        git.remote.update(_out=sys.stdout, _err=sys.stderr)


def rebuild_working_repo(repo_name):
    bare_repo_path = "{0}.git/".format(repo_name)
    working_repo_path = "{0}".format(repo_name)
    if Path(working_repo_path).exists():
        logging.info("Removing previous working repo...")
        shutil.rmtree(working_repo_path)
    logging.info("Rebuilding working repo...")
    sh.git.clone(bare_repo_path, working_repo_path)


def generate_config(repo_name):
    config = configparser.ConfigParser()
    working_repo_path = "{0}".format(repo_name)
    dirs = os.scandir( working_repo_path + "/sig/" )
    for folder in dirs:
        if folder.name.startswith('.') or not folder.is_dir(follow_symlinks = False):
            continue
        sig_id = folder.name
        metadata_path = working_repo_path + "/sig/" + sig_id + "/metadata.yml"
        logging.info(metadata_path)
        if Path(metadata_path).exists():
            with open(metadata_path, 'r', encoding='utf-8') as metadata_file:
                metadata = yaml.safe_load(metadata_file)
                rss = val_of_key(metadata, ['rss'], '')
                if rss:
                    sig_name = val_of_key(metadata, ['name'], sig_id)
                    site_url = val_of_key(metadata, ['blog'], '')
                    matrix_url = val_of_key(metadata, ['matrix'], '')
                    avatar = val_of_key(metadata, ['avatar'], 'default-sig.svg')
                    flairs: list[str] = []
                    if matrix_url:
                        flairs.append("matrix:{0}".format(matrix_url))
                    config[sig_id] = {
                        'title': sig_name,
                        'feed_url': rss,
                        'site_url': site_url,
                        'flairs': ' '.join(flairs),
                        'avatar': avatar,
                    }
                    logging.info(sig_name + rss)
    with open('../sig.ini', 'w') as configfile:
        configfile.write('# This file is auto-generated. All changes will be lost. See generate_sig_config.py\n')
        config.write(configfile)
    logging.info("Done.")


def generate():
    ensure_working_dir()
    fetch_repo("SIG")
    rebuild_working_repo("SIG")
    generate_config("SIG")


if __name__ == "__main__":
    level = logging.INFO
    logging.basicConfig(format='%(levelname)s: %(message)s', level=level)
    generate()
