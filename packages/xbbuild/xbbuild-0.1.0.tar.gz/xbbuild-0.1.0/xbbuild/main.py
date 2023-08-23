from xbutils.cmd import Cmd

Cmd.default_function_module = 'xbbuild'

Cmd(name='info', function=".info.info_cmd")
Cmd(name='zip-doc', function=".zip_doc.zip_doc_cmd")


def main():
    Cmd.main()


if __name__ == '__main__':
    main()
