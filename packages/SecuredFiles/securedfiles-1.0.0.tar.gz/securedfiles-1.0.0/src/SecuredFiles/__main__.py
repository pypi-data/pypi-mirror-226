import sys
import time

from __init__ import File

if __name__ == '__main__':
    """
    This is the main script that locks or unlocks files based on their extensions.
    """
    if len(sys.argv) > 1:
        for filepath in sys.argv[1:]:
            file = File(filepath)
            if isinstance(file, File.UnsecureFile):
                file.lock()
                print('LOCK ', file.path)
            else:
                file.unlock()
                print('UNLOCK ', file.path)
            time.sleep(0.1)
