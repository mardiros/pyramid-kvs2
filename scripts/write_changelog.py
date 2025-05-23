#!/usr/bin/env python3
import datetime

import pyramid_kvs2

head = "Changelog\n=========\n"
header = (
    f"{pyramid_kvs2.__version__} - "
    f"Released on {datetime.datetime.now().date().isoformat()}"
)
with open("CHANGES.rst.new", "w") as changelog:
    changelog.write(head)
    changelog.write("\n")
    changelog.write(header)
    changelog.write("\n")
    changelog.write("-" * len(header))
    changelog.write("\n")
    changelog.write("* please write here \n\n")
