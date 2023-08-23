from xbutils.simple_config import SimpleConfig, Path


class Config(SimpleConfig):
    #: Package Name
    name: str = ''
    #: Package Version
    version: str = ''
    #: doc path
    doc_path: Path = Path("build/sphinx")
    #: src doc path
    src_doc_path: Path = Path("doc")
    #: packages path
    out_path: Path = Path("dist")


cfg = Config()
cfg.read_config('~/.xbbuild.cfg')
cfg.read_config('.xbbuild.cfg')
