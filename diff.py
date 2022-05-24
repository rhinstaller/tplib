#!/bin/env python3

import sys
import traceback
from tplib.diff_main import main

if __name__ == "__main__":
    try:
        rc = main()
    except:
        traceback.print_exc()
        sys.exit(2)
    sys.exit(rc)
