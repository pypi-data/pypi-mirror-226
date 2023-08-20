#!/usr/bin/env python3
import argparse, os, sys

from .header import PartCloneException, Header
from .bitmap import Bitmap
from .blocks import BlocksReader
from .fuse   import runFuse


def isEmptyDirectory(path: str) -> str:
    "Is argument an empty directory?"
    if os.path.isdir(path) and len(os.listdir(path)) == 0:
        return path
    raise argparse.ArgumentTypeError(f"'{path}' is not an empty directory")


def indexSizeType(arg: str) -> int:
    "Is argument an acceptable argument for option --index_size?"
    try:
        iarg = int(arg)
    except:
        raise argparse.ArgumentTypeError(f"'{arg}' is not an integer")

    if iarg < 1000:
        raise argparse.ArgumentTypeError(f"'{arg}' is too small, "
                                         "should be >= 1000")
    if iarg % 8 != 0:
        raise argparse.ArgumentTypeError(f"'{arg}' is not a multiple of 8")
    return iarg


def main():
    """
    Processes command-line argumments, reads image and mounts it as
    virtual partition.
    """

    parser = argparse.ArgumentParser(prog='vpartclone',
                                     description='Mount partclone image '
                                     'backup as virtual partition.')
    parser.add_argument('image', type=argparse.FileType('rb'),
                        help='partclone image to read')
    parser.add_argument('-m', '--mountpoint', type=isEmptyDirectory,
                        help='mount point for virtual partition; '
                        'an empty directory')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='dump header and bitmap info')
    parser.add_argument('-d', '--debug_fuse', action='store_true',
                        help='enable FUSE filesystem debug messages')
    parser.add_argument('-c', '--crc_check', action='store_true',
                        help='verify all checksums in image (slow!)')
    parser.add_argument('-i', '--index_size', type=indexSizeType,
                        help='Size parameter for building bitmap index; leave '
                        'unchanged unless memory usage too high. Increase '
                        'size to reduce memory usage by doubling or '
                        'quadrupling number '
                        f'repeatedly (default {Bitmap.BLOCK_OFFSET_SIZE}).',
                        default=Bitmap.BLOCK_OFFSET_SIZE)
    args = parser.parse_args()

    try:
        header = Header(args.image)
        if args.verbose:
            print(header)

        bitmap = Bitmap(header, args.image, args.index_size)
        if args.mountpoint is not None:
            bitmap.buildBlockIndex()

        if args.verbose:
            print()
            print(bitmap)
            print()

        if args.crc_check:
            print(f"Verifying all checksums of image '{args.image.name}'...")
            BlocksReader(bitmap, args.image, verify_crc=args.crc_check)

        if args.mountpoint is not None:

            try:

                runFuse(args.image, bitmap, args.mountpoint, args.debug_fuse)

            except Exception as e:
                print(file=sys.stderr)
                print(f'FUSE file system errored out with: "{e}".',
                      file=sys.stderr)
                sys.exit(1)

    except PartCloneException as e:
        print(file=sys.stderr)
        print('Error:', e, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
