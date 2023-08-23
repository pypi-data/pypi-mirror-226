from xbbuild.config import cfg
from xbutils.log import warning
import re
from pathlib import Path
from typing import Optional



class Info:
    path: Path
    version: str = ''
    name: str = ''

    def __init__(self, path: Optional[Path] = None):
        self.path = Path.cwd() if path is None else path.resolve()
        if cfg.version:
            self.version = cfg.version
        if cfg.name:
            self.name = cfg.version
        self.read_egg()

    def read_egg(self):
        if self.name:
            egg_path = self.path / (self.name + '.egg-info')
        else:
            egg_list = list(i for i in self.path.glob('*.egg-info') if i.is_dir())
            if not egg_list:
                warning(f"No egg in {self.path}")
                return
            if len(egg_list) > 1:
                warning(f"Multiple eggs in {self.path} using {egg_list[0].name}")
            egg_path = egg_list[0]

        info_path = egg_path / 'PKG-INFO'
        if not info_path.exists():
            warning(f"No PKG-INFO in {egg_path}")
            return

        pkg_info = info_path.read_text()
        if not self.version:
            match = re.search(r"(?m)^Version: (\S*)\s*?$", pkg_info)
            if not match:
                warning(f"Missing Version in {info_path}")
            else:
                self.version = match.group(1)
        if not self.name:
            match = re.search(r"(?m)^Name: (\S*)\s*?$", pkg_info)
            if not match:
                warning(f"Missing Name in {info_path}")
            else:
                self.name = match.group(1)

    def pkg_name(self, ext: str = ''):
        return (self.name or 'NONAME') + '-' + (self.version or '0.0.0') + ext

    def doc_zip_path(self):
        return (self.path / cfg.out_path / self.pkg_name("-doc.zip")).resolve()

    def doc_path(self):
        return (self.path / cfg.doc_path).resolve()

    def src_doc_path(self):
        return (self.path / cfg.src_doc_path).resolve()


def info_cmd():
    i = Info()

    print("Name    :", i.name or '????')
    print("Version :", i.version or '????')
    print("Path    :", i.path)


if __name__ == '__main__':
    info_cmd()
