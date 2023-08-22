import json
from nodejs import node
from subprocess import PIPE
import pathlib


class PM2MP:
    def __init__(
        self,
    ) -> None:
        self.node = node
        self.wrapper_file = pathlib.Path(__file__).with_name("pm2wrapper.js")

    def list(
        self,
    ):
        res, err = self.node.Popen(
            [
                "-e",
                f'require("{self.wrapper_file}").list()',
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
                f'require("{self.wrapper_file}").start("{id}")',
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
                f'require("{self.wrapper_file}").stop({id})',
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
                f'require("{self.wrapper_file}").restart({id})',
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
                f'require("{self.wrapper_file}").reload({id})',
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
                f'require("{self.wrapper_file}").delete({id})',
            ],
            stdout=PIPE,
            encoding="utf-8",
        ).communicate()
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
                f'require("{self.wrapper_file}").kill()',
            ],
            stdout=PIPE,
            encoding="utf-8",
        ).communicate()
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
                f'require("{self.wrapper_file}").describe({id})',
            ],
            stdout=PIPE,
            encoding="utf-8",
        ).communicate()
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
