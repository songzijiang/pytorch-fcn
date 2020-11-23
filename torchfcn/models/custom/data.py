import hashlib
import os
import os.path as osp
import gdown


def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(blocksize), b''):
            hash.update(block)
    return hash.hexdigest()


def cached_download(url, path, md5=None, quiet=False, postprocess=None):
    def check_md5(path, md5):
        print('[{:s}] Checking md5 ({:s})'.format(path, md5))
        return md5sum(path) == md5

    if osp.exists(path) and not md5:
        print('[{:s}] File exists ({:s})'.format(path, md5sum(path)))
    elif osp.exists(path) and md5 and check_md5(path, md5):
        pass
    else:
        dirpath = osp.dirname(path)
        if not osp.exists(dirpath):
            os.makedirs(dirpath)
        gdown.download(url, path, quiet=quiet, proxy="127.0.0.1:1080")

    if postprocess is not None:
        postprocess(path)

    return path
