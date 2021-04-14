def ends_in_zip(name):
    return name.lower().endswith(".zip")


def is_index_file(name):
    return name.startswith("Files ")


def is_rtf_file(name):
    return name.lower().endswith(".rtf")
