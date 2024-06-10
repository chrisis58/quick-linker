import os

def get_whole_ext(file):
    info = os.path.splitext(file)
    if info[1] in [".ass", '.srt', '.ssa', '.sub']:
        ext = ""
        while len(info[1]) > 0:
            file = info[0]
            ext = info[1] + ext
            info = os.path.splitext(file)
        return ext
    else:
        return info[1]