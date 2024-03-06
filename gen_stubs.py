import re
import subprocess
from pathlib import Path
from shlex import split

regex = re.compile(r'^( {4}def \w+\(self): "[^"]+"')

kothon_seq = Path(__file__).parent / "kothon" / "iterable" / "seq.py"
kothon_seq_stub = (
    Path(__file__).parent / "kothon" / "stubs" / "kothon" / "iterable" / "seq.pyi"
)

if __name__ == "__main__":
    code = subprocess.check_call(
        split("stubgen -o ./kothon/stubs -p kothon"),
        cwd=Path(__file__).parent,
    )
    assert code == 0
    assert kothon_seq.is_file()
    assert kothon_seq_stub.is_file()

    with open(kothon_seq, "r") as fd:
        all_matches = [m for d in fd.readlines() if (m := regex.match(d))]

    with open(kothon_seq_stub, "r+") as fd:
        data = fd.read()
        for match in all_matches:
            prefix = match.group(1)
            data = data.replace(prefix, match.group(0))
        fd.seek(0)
        fd.write(data)
