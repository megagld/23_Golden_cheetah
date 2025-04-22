def fix_file(file):
    data = open(file).read().splitlines()
    with open(file, "w") as fh:
        fh.write(f"{data[0]}")   