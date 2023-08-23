from xbbuild.info import Info
from xbutils.log import *
from pathlib import Path
from typing import Optional
from subprocess import run


def zip_doc(info: Info, doc_path: Optional[Path] = None, zip_path: Optional[Path] = None):
    if zip_path is None:
        zip_path = info.doc_zip_path()
    if doc_path is None:
        doc_path = info.doc_path()

    if not doc_path.is_dir():
        error(f"Missing doc ({doc_path}")
        return False

    if (doc_path / 'html').is_dir():
        zip_what = 'html'
    elif (doc_path / 'index.html').is_file():
        zip_what = '.'
    else:
        error(f"Missing html in ({doc_path}")
        return False

    if not zip_path.parent.exists():
        zip_path.parent.mkdir(parents=True)

    if zip_path.exists():
        zip_path.unlink()

    run(['zip', str(zip_path), '-r', zip_what], cwd=doc_path)


def zip_doc_cmd():
    zip_doc(Info())
