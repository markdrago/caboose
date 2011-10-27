import os

def _create_random_file(directory):
    i = 0
    while True:
        filename = "file%d" % i
        filepath = os.path.join(directory, filename)
        if os.path.exists(filepath):
            i += 1
            continue
        with open(filepath, 'w') as f:
            f.write(filename)
            f.close()
        return filepath

