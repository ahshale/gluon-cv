"""Prepare ADE20K datasets.
========================

This script download and prepare the `ADE20K
<http://sceneparsing.csail.mit.edu/>`_ dataset for scene parsing.  It contains
more than 20 thousands scene-centric images annotated with 150 object
categories.

.. image:: http://groups.csail.mit.edu/vision/datasets/ADE20K/assets/images/examples.png
   :width: 600 px

Prepare the dataset
-------------------

The easiest way is simply running this script, which will automatically download
and extract the data into ``~/.mxnet/datasets/ade``.

.. code-block:: bash

   python scripts/datasets/ade20k.py

.. note::

   You need 2.3 GB disk space to download and extract this dataset. SSD is
   preferred over HDD because of its better performance.

.. note::

   The total time to prepare the dataset depends on your Internet speed and disk
   performance. For example, it may take 15 min on AWS EC2 with EBS.


If you have already downloaded the following required files, whose URLs can be
obtained from the source codes at the end of this tutorial,

===========================  ======
Filename                     Size
===========================  ======
ADEChallengeData2016.zip     923 MB
release_test.zip             202 MB
===========================  ======

then you can specify the folder name through ``--download-dir`` to avoid
download them again. For example

.. code-block:: python

   python scripts/datasets/ade20k.py --download-dir ~/ade_downloads

How to load the dataset
-----------------------

TODO.

Dive deep into source code
--------------------------

The implementation of ade20k.py is straightforward. It simply downloads and
extract the data.
"""
import os
import shutil
import argparse
import zipfile
from gluonvision.utils import download, makedirs

_TARGET_DIR = os.path.expanduser('~/.mxnet/datasets/ade')


def parse_args():
    parser = argparse.ArgumentParser(
        description='Initialize ADE20K dataset.',
        epilog='Example: python setup_ade20k.py --path ~/Datasets --download',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--path', required=True, help='dataset directory on disk')
    parser.add_argument('--download', action='store_true', help='try download if set')
    parser.add_argument('--overwrite', action='store_true', help='overwrite downloaded if set')
    args = parser.parse_args()
    return args

# what does aug mean?
def download_aug(path, overwrite=False):
    _AUG_DOWNLOAD_URLS = [
        ('http://data.csail.mit.edu/places/ADEchallenge/ADEChallengeData2016.zip', '219e1696abb36c8ba3a3afe7fb2f4b4606a897c7'),
        ('http://data.csail.mit.edu/places/ADEchallenge/release_test.zip', 'e05747892219d10e9243933371a497e905a4860c'),]
    download_dir = os.path.join(path, 'downloads')
    makedirs(download_dir)
    for url, checksum in _AUG_DOWNLOAD_URLS:
        filename = download(url, path=download_dir, overwrite=overwrite, sha1_hash=checksum)
        # extract
        with zipfile.ZipFile(filename,"r") as zip_ref:
            zip_ref.extractall(path=path)


if __name__ == '__main__':
    args = parse_args()
    path = os.path.expanduser(args.path)
    if not os.path.isdir(os.path.join(path, 'ADEChallengeData2016')):
        if not args.download:
            raise ValueError(('{} is not a valid directory, make sure it is present.'
                              ' Or you can try "--download" to grab it'.format(path)))
        else:
            download_aug(path, overwrite=args.overwrite)

    # make symlink
    makedirs(os.path.expanduser('~/.mxnet/datasets'))
    if os.path.isdir(_TARGET_DIR):
        os.remove(_TARGET_DIR)
    os.symlink(args.path, _TARGET_DIR)