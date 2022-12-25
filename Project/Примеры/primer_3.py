#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
from datetime import datetime


if __name__ == "__main__":
    directory = pathlib.Path.cwd()
    time, file_path = max((f.stat().st_mtime, f) for f in directory.iterdir())
    print(datetime.fromtimestamp(time), file_path)