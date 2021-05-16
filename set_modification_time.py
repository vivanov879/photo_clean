import os
from pathlib import Path
import datetime
from tqdm import tqdm
import time
import datetime
import subprocess
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata


def get_mov_date_taken(filename):
    parser = createParser(filename)
    metadata = extractMetadata(parser)

    if metadata is None:
        return
    try:
        date = metadata.get('creation_date')
        return date
    except ValueError:
        return None


def get_photo_date_taken(filepath):
    """Gets the date taken for a photo through a shell."""
    cmd = "mdls '%s'" % filepath
    output = subprocess.check_output(cmd, shell=True)
    lines = output.decode("ascii").split("\n")
    for l in lines:
        if "kMDItemContentCreationDate" in l:
            datetime_str = l.split("= ")[1]
            datetime_str = datetime_str
            date = datetime.datetime.strptime(
                datetime_str, "%Y-%m-%d %H:%M:%S +0000")

            return date


def update_creation_time(fn):
    fn = fn.as_posix()
    date = get_mov_date_taken(fn)
    if date is None:
        date = get_photo_date_taken(fn)
    if date is None:
        return
    date = time.mktime(date.timetuple())
    date -= 3600 * 7
    os.utime(fn, (date, date))


def run_all(d):
    fns = d.glob("**/*")
    fns = list(fns)
    for fn in tqdm(fns):
        if fn.is_dir():
            continue
        if fn.stem[0] == ".":
            continue
        update_creation_time(fn)


if __name__ == "__main__":

    fn = "/Volumes/Photos/May2021/IMG_6364.HEIC"
    fn = "/Volumes/Photos/May2021/IMG_6206.MOV"
    fn = "/Volumes/Photos/May2021/IMG_7593.MOV"
    fn = Path("/Volumes/Photos/May2021/IMG_0659.MOV")
    update_creation_time(fn)
    d = Path("/Volumes/Photos/")
    run_all(d)
