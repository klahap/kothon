import re
import subprocess
from pathlib import Path
from shlex import split

kothon_stubs_path = Path(__file__).parent / "kothon" / "stubs" / "kothon"
kothon_seq_path = Path(__file__).parent / "kothon" / "iterable" / "seq.py"
kothon_stubs_seq_path = kothon_stubs_path / "iterable" / "seq.pyi"
kothon_stubs_sequence_path = kothon_stubs_path / "functions" / "sequence.pyi"

if __name__ == "__main__":
    code = subprocess.check_call(
        split("stubgen -o ./kothon/stubs -p kothon"),
        cwd=Path(__file__).parent,
    )
    assert code == 0
    assert kothon_seq_path.is_file()
    assert kothon_stubs_seq_path.is_file()
    assert kothon_stubs_sequence_path.is_file()

    with open(kothon_seq_path, "r") as fd:
        regex = re.compile(r'^( {4}def \w+\(self): "[^"]+"')
        all_matches = [m for d in fd.readlines() if (m := regex.match(d))]

    with open(kothon_stubs_seq_path, "r+") as fd:
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

    with open(kothon_stubs_sequence_path, "r+") as fd:
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
