from xbbuild.info import Info
from xbutils.log import error
from pathlib import Path
from typing import Optional
from subprocess import run


def run_sphinx(info: Info, src_path: Optional[Path] = None, doc_path: Optional[Path] = None):
    if src_path is None:
        src_path = info.src_doc_path()
    if doc_path is None:
        doc_path = info.doc_path()

    if not src_path.is_dir():
        error(f"Missing doc ({src_path}")
        return False

    run(['sphinx-build', str(src_path), str(doc_path)])


def sphinx_cmd():
    run_sphinx(Info())
