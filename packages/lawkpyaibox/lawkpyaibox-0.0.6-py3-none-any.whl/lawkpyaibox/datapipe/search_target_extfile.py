import os


def search_target_extfile(rootdir, ext='.jpg'):
    filepaths = list()
    for root, dirs, files in os.walk(rootdir, topdown=True):
        for name in files:
            filepath = os.path.join(root, name)
            if ext not in filepath:
                continue
            filepaths.append(filepath)

    return filepaths
