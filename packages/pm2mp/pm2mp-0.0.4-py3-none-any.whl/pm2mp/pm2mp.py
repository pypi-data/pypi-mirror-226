import json
from nodejs import node
from subprocess import PIPE


class PM2MP:
    def __init__(
        self,
    ) -> None:
        self.node = node

    def list(
        self,
    ):
        res, err = self.node.Popen(
            [
                "-e",
                'require("./pm2wrapper.js").list()',
            ],
            stdout=PIPE,
            encoding="utf-8",
        ).communicate()
        if not err:
            res = self.Js2Py_dict(res)
            return res
        else:
            print(err)

    def start(
        self,
        id: str,
    ):
        res, err = self.node.Popen(
            [
                "-e",
                f'require("./pm2wrapper.js").start("{id}")',
            ],
            stdout=PIPE,
            encoding="utf-8",
        ).communicate()
        if not err:
            res = self.Js2Py_dict(res)
            return res
        else:
            print(err)

    def stop(
        self,
        id: str,
    ):
        res, err = self.node.Popen(
            [
                "-e",
                f'require("./pm2wrapper.js").stop({id})',
            ],
            stdout=PIPE,
            encoding="utf-8",
        ).communicate()
        if not err:
            res = self.Js2Py_dict(res)
            return res
        else:
            print(err)

    def restart(
        self,
        id: str,
    ):
        res, err = self.node.Popen(
            [
                "-e",
                f'require("./pm2wrapper.js").restart({id})',
            ],
            stdout=PIPE,
            encoding="utf-8",
        ).communicate()
        if not err:
            res = self.Js2Py_dict(res)
            return res
        else:
            print(err)

    def reload(
        self,
        id: str,
    ):
        res, err = self.node.Popen(
            [
                "-e",
                f'require("./pm2wrapper.js").reload({id})',
            ],
            stdout=PIPE,
            encoding="utf-8",
        ).communicate()
        if not err:
            res = self.Js2Py_dict(res)
            return res
        else:
            print(err)

    def delete(
        self,
        id: str,
    ):
        res, err = self.node.Popen(
            [
                "-e",
                f'require("./pm2wrapper.js").delete({id})',
            ],
            stdout=PIPE,
            encoding="utf-8",
        )
        if not err:
            res = self.Js2Py_dict(res)
            return res
        else:
            print(err)


    def kill(
        self,
    ):
        res, err = self.node.Popen(
            [
                "-e",
                f'require("./pm2wrapper.js").kill()',
            ],
            stdout=PIPE,
            encoding="utf-8",
        )
        if not err:
            res = self.Js2Py_dict(res)
            return res
        else:
            print(err)

    def describe(
        self,
        id: str,
    ):
        res, err = self.node.Popen(
            [
                "-e",
                f'require("./pm2wrapper.js").describe({id})',
            ],
            stdout=PIPE,
            encoding="utf-8",
        )
        if not err:
            res = self.Js2Py_dict(res)
            return res
        else:
            print(err)

    def Js2Py_dict(
        self,
        json_str: str,
    ):
        json_object = json.loads(json_str)
        return json_object

