from xbbuild.info import Info
from xbbuild.zip_doc import zip_doc
from xbbuild.sphinx import run_sphinx
from pathlib import Path
from typing import Optional


def build_doc(info: Info, src_path: Optional[Path] = None, doc_path: Optional[Path] = None,
              zip_path: Optional[Path] = None):
    run_sphinx(info, src_path, doc_path)
    zip_doc(info, doc_path, zip_path)


def build_doc_cmd():
    build_doc(Info())
