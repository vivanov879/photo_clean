
import os
from pathlib import Path
import datetime
from tqdm import tqdm
import time
import datetime
import subprocess
import exifread
from pathlib import Path


if __name__ == "__main__":
    dir1 = Path("/Volumes/Photos/Jan2021")
    dir2 = Path("/Volumes/Photos/May2021")

    print("Globbing fns1 ... ")
    fns1 = dir1.glob("*")

    print("Globbing fns2 ... ")
    fns2 = dir2.glob("*")

    print("Glob done. ")

    fns1 = [fn.name for fn in fns1]
    fns2 = [fn.name for fn in fns2]

    fns1 = set(fns1)
    fns2 = set(fns2)

    fns = fns1.intersection(fns2)
    identicals = []
    for fn in fns:
        fn1 = dir1 / fn
        fn2 = dir2 / fn
        size1 = fn1.stat().st_size
        size2 = fn2.stat().st_size

        if size1 != size2:
            continue

        identicals.append(fn)
        print(fn2)
        # fn2.unlink()

    print(f"{len(identicals)=}")
