"""Module to assist wrapping a binary in python for an endpoint"""
import json
import re
from subprocess import PIPE, STDOUT, Popen

from cnvrgv2 import Endpoint

from .custom_thread import ThreadWithReturnValue


class EndpointBinary:
    """
    A class used to manage running a binary from python in an endpoint.

    Attributes
    ----------
    endpoint : cnvrgv2.Endpoint
        A cnvrg Endpoint object. If you do not pass in, we assume you want us
        to create this on your behalf.
    binary_name : str
        The name of the binary you wish us to execute
    binary_args : list, default=[]
        Argurments in list format that you wish to pass to the binary
    metrics_prefix : str, default="cnvrg_tag"
        Prefix to watch for in stdout.
    delimiter : str, default="_"
        Delimiter used to split prefix away from metric and result in stdout

    Examples
    --------
    >>> from cnvrg_endpoint_binary import EndpointBinary
    >>> eb = EndpointBinary(binary_name="demo", binary_args=["--flag=true"])
    >>> result = eb.predict("input_arg")
    >>> print(result)
    """

    def __init__(self, **kwargs):
        self.endpoint = kwargs.get("endpoint", None)
        self.binary_name = kwargs["binary_name"]
        self.binary_args = kwargs.get("binary_args", [])
        self.metrics_prefix = kwargs.get("metrics_prefix", "cnvrg_tag")
        self.delimiter = kwargs.get("delimiter", "_")
        if not self.endpoint:
            self._generate_endpoint()

    def _convert_camelcase(self, word):
        """
        This private method converts a string to camel case keying off of the
        delimiter
        """
        return word.split(self.delimiter)[0] + "".join(
            x.capitalize() or self.delimiter
            for x in word.split(self.delimiter)[1:]
        )

    def _is_prefix(self, stdout):
        if re.match(rf"^{self.metrics_prefix}", stdout):
            return "metric"
        try:
            json.loads(stdout)
        except ValueError:
            return False
        return "result"

    def _extract_tag(self, tag):
        tag_split = tag.split("_")
        tag_extracted = "_".join(tag_split[2:])
        kv = tag_extracted.split(":")
        return self._convert_camelcase(kv[0]), ":".join(kv[1:])

    def _deal_with_stdout(self, process):
        result = None
        for line in process.stdout:
            decoded_line = line.decode("utf-8")
            match self._is_prefix(decoded_line):
                case "metric":
                    key, value = self._extract_tag(decoded_line)
                    print(f"key: {key}\nvalue: {value}")
                    if isinstance(self.endpoint, Endpoint):
                        self.endpoint.log_metric(key, value)
                case "result":
                    result = json.loads(decoded_line)
                    print(result)
                    break
                case _:
                    print(decoded_line)
        return result

    def predict(self, *args):
        """
        This is the main entrypoint for this module. Users will call this from
        within their endpoint code. Any number of args can be passed to this
        method allowing inputs to be passed to the binary

        Paramters
        ---------
        *args : list
            Input arguments to pass to the binary

        Returns
        -------
        result : dict
            The json (dict) result output of the binary
        """
        command = [self.binary_name] + self.binary_args + list(args)
        p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        t = ThreadWithReturnValue(
            target=self._deal_with_stdout, args=(p,), daemon=True
        )
        t.start()
        return t.join()

    def _generate_endpoint(self):
        self.endpoint = Endpoint()
