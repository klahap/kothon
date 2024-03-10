import re
import subprocess
from pathlib import Path
from shlex import split

kothon_path = Path(__file__).parent / "kothon"
kothon_seq_path = kothon_path / "iterable" / "seq.py"
kothon_seq_stub_path = kothon_path / "iterable" / "seq.pyi"
kothon_type_utils_stub_path = kothon_path / "_utils" / "type_utils.pyi"
kothon_sequence_stub_path = kothon_path / "functions" / "sequence.pyi"

if __name__ == "__main__":
    for stub_file in kothon_path.glob("**/*.pyi"):
        stub_file.unlink()
    code = subprocess.check_call(
        split("stubgen -o . -p kothon"),
        cwd=Path(__file__).parent,
    )
    assert code == 0
    assert kothon_seq_path.is_file()
    assert kothon_seq_stub_path.is_file()
    assert kothon_type_utils_stub_path.is_file()
    assert kothon_sequence_stub_path.is_file()

    with open(kothon_seq_path, "r") as fd:
        regex = re.compile(r'^( {4}def \w+\(self): "[^"]+"')
        all_matches = [m for d in fd.readlines() if (m := regex.match(d))]

    with open(kothon_seq_stub_path, "r+") as fd:
        data = fd.read()
        for match in all_matches:
            prefix = match.group(1)
            data = data.replace(prefix, match.group(0))
        data = data.replace(
            "from typing import ",
            "from typing import Optional, ",
        )
        fd.seek(0)
        fd.write(data)

    with open(kothon_sequence_stub_path, "r+") as fd:
        data = fd.read()
        data = data.replace(
            "from typing import ",
            "from typing import Type, ",
        )
        data = data.replace(
            "def filter_is_instance(cls",
            "def filter_is_instance(cls: Type[R]",
        )
        fd.seek(0)
        fd.write(data)

    with open(kothon_type_utils_stub_path, "r+") as fd:
        data = fd.read()
        data = data.replace(
            "def __lt__(self, other: CT) -> bool:",
            "def __lt__(self: CT, other: CT) -> bool:",
        )
        data = data.replace(
            "def __add__(self, other: AT) -> AT:",
            "def __add__(self: AT, other: AT) -> AT:",
        )
        fd.seek(0)
        fd.write(data)
