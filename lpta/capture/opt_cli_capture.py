import os
import re
import subprocess
import tempfile

from .base import CaptureBackend
from .models import PassEvent

HEADER_PATTERN = re.compile(r"\*\*\* IR Dump After (.+?) on (.+?) \*\*\*")

class OptCliCapture(CaptureBackend):
    """
    Captures pass-by-pass IR using `clang` and `opt` as subprocesses.
    """

    def capture(self, source_path: str, opt_level: str = "O2") -> list[PassEvent]:
        """
        source_path: path to a .c/cpp file
        opt_level: optimization   level, e.g. "O2"
        returns ordered list of PassEvent for every pass that changed the IR
        """

        ll_path = self._compile_to_ir(source_path)
        pass_log = self.run_opt(ll_path, opt_level)

        os.remove(ll_path)

        return self.parse_log(pass_log)

    def _compile_to_ir(self,source_path: str) -> str:
        """
        source_path: path to source file
        returns: path to generated .ll file
        """

        ll_path = tempfile.mktemp(suffix=".ll")
        subprocess.run(["clang", "-S", "emit-llvm", "-Xclang", "-disable-O0-optnone", source_path, "-o", ll_path], check= True)

        return ll_path

    def _run_opt(self, ll_path: str, opt_level: str) -> str: 
        """
        ll_path: path to .ll file. 
        opt_level: optimization level
        returns: raw pass log text.
        """

        result = subprocess.run(["opt", f"-{opt_level}", "print-changed=quiet", "-S", ll_path, "-o", "/dev/null"], check= True)

        return result.stderr

    def _parse_log(self, pass_log: str) -> list[PassEvent]:
        """
        pass_log: raw opt stderr text. 
        returns: ordered list of PassEvent.
        """

        matches = list(HEADER_PATTERN.finditer(pass_log))
        events = []
        last_ir_by_function = {}

        for i, match in enumerate(matches):
            pass_name, function_name = match.group(1), match.group(2)
            start = match.end()
            end = match[i + 1].start() if i + 1 < len(matches) else len(pass_log)

            ir_after = pass_log[start:end].strip()

            ir_before = last_ir_by_function.get(function_name,"")

            events.append(PassEvent(pass_name,  function_name, ir_before, ir_after))

            last_ir_by_function[function_name] = ir_after

        return events

    