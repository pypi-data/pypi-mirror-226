import asyncio, errno, io, os, stat, traceback

import pyfuse3 # install with "pip install pyfuse3"; on Ubuntu use "sudo apt install python3-pyfuse3"
import pyfuse3_asyncio

from .header  import PartCloneException
from .bitmap  import Bitmap
from .blockio import BlockIO


class PartCloneFS(pyfuse3.Operations):
    """
    This class implements a FUSE filesystem on top of a partclone image.

    A single read-only file is shown under the moint point. This file
    is named like the image.

    This file can be read and it refects the partition stored in the partclone
    image. Unused (and hence not stored) blocks are returned as bytes of zeros.

    This file represents a partition which can be mounted with the loop option
    to inspect or save its contents. Remember to mount it read-only.
    """

    FILE_INODE = pyfuse3.ROOT_INODE + 1

    def __init__(self, file: io.BufferedReader, bitmap: Bitmap,
                 debug: bool = False):
        super().__init__()
        filename = os.path.split(file.name)[1]
        if filename.lower().endswith('.img'):
            filename = filename[:-4]
        self.fuse_filename = bytes(filename, 'utf-8')
        self.block_io = BlockIO(file, bitmap)
        self.image_stat = os.fstat(file.fileno())
        umask = os.umask(0o0750)
        os.umask(umask)
        self.dir_st_mode  = stat.S_IFDIR | (0o555 & (0o777 ^ umask))
        self.file_st_mode = stat.S_IFREG | (0o444 & (0o777 ^ umask))

        # Make sure file allows tell() and seek().
        if not (self.image_stat.st_mode & (stat.S_IFREG|stat.S_IFBLK)):
            file_type = 'something else'
            if self.image_stat.st_mode & stat.S_IFSOCK:
                file_type = 'a socket'
            elif self.image_stat.st_mode & stat.S_IFCHR:
                file_type = 'a character device'
            elif self.image_stat.st_mode & stat.S_IFIFO:
                file_type = 'a fifo'
            raise PartCloneException(f"Image file '{file.name}' is {file_type}."
                                     " In order to mount an image as a virtual "
                                     "partiton, it must be a regular file.")
        self.debug = debug

    async def getattr(self, inode: int, ctx=None):
        try:
            entry = pyfuse3.EntryAttributes()
            if inode == pyfuse3.ROOT_INODE:
                entry.st_mode = self.dir_st_mode
                entry.st_nlink = 2
                entry.st_size = 0
                entry.st_atime_ns = self.image_stat.st_atime_ns
                entry.st_ctime_ns = self.image_stat.st_ctime_ns
                entry.st_mtime_ns = self.image_stat.st_mtime_ns
            elif inode == self.FILE_INODE:
                entry.st_mode = self.file_st_mode
                entry.st_nlink = 1
                entry.st_size = self.block_io.getTotalSize()
                entry.st_atime_ns = self.image_stat.st_atime_ns
                entry.st_ctime_ns = self.image_stat.st_ctime_ns
                entry.st_mtime_ns = self.image_stat.st_mtime_ns
            else:
                raise pyfuse3.FUSEError(errno.ENOENT)
            entry.st_gid = os.getgid()
            entry.st_uid = os.getuid()
            entry.st_ino = inode
            return entry
        except Exception as e:
            print(f'getattr(inode={inode}) encountered: {e}.')
            raise pyfuse3.FUSEError(errno.ENOENT)

    async def lookup(self, parent_inode: int, name: bytes, ctx):
        if parent_inode != pyfuse3.ROOT_INODE or \
           name != self.fuse_filename:
            raise pyfuse3.FUSEError(errno.ENOENT)
        return await self.getattr(self.FILE_INODE)

    async def opendir(self, inode: int, ctx):
        if inode != pyfuse3.ROOT_INODE:
            raise pyfuse3.FUSEError(errno.ENOENT)
        return inode

    async def readdir(self, inode: int, start_id: int, token):
        try:
            assert inode == pyfuse3.ROOT_INODE
            # only one entry in directory
            if start_id == 0:
                pyfuse3.readdir_reply(token, self.fuse_filename,
                                      await self.getattr(self.FILE_INODE), 1)
            return
        except Exception as e:
            print(f'readdir(inode={inode}, start_id={start_id}, '
                  f'token={token}) encountered: {e}.')
            raise pyfuse3.FUSEError(errno.ENOENT)

    async def open(self, inode: int, flags: int, ctx):
        try:
            if inode != self.FILE_INODE:
                raise pyfuse3.FUSEError(errno.ENOENT)
            if flags & os.O_RDWR or flags & os.O_WRONLY:
                raise pyfuse3.FUSEError(errno.EROFS)
            return pyfuse3.FileInfo(fh=inode)
        except Exception as e:
            print(f'open(inode={inode}, flags=0x{flags:x}) '
                  f'encountered: {e}.')
            raise pyfuse3.FUSEError(errno.ENOENT)

    async def read(self, inode: int, offset: int, size: int):
        try:
            assert inode == self.FILE_INODE
            return self.block_io.read_data(offset, size)
        except Exception as e:
            print(f'read(inode={inode}, offset=0x{offset:x}, '
                  f'size=0x{size:x}) encountered: {e}.')
            if self.debug:
                print(traceback.format_exc())
            raise pyfuse3.FUSEError(errno.EIO)

    async def write(self, inode: int, offset: int, buffer: bytes):
        if len(buffer) != 0:
            raise pyfuse3.FUSEError(errno.EROFS)
        return 0


def runFuse(file: io.BufferedReader, bitmap: Bitmap, mountpoint: str,
            debug: bool = False):
    if not os.path.isdir(mountpoint) or len(os.listdir(mountpoint)) != 0:
        raise PartCloneException(f"Mount point '{mountpoint}' "
                                 "is not an empty directory.")
    fs = PartCloneFS(file, bitmap, debug)
    print()
    dir_name = os.path.abspath(mountpoint)
    file_name = os.path.join(dir_name, str(fs.fuse_filename, 'utf-8'))
    print(f"Virtual partition provided as '{file_name}'.")
    print()
    print(f"The file system of this virtual partition can be checked "
          "with this command:")
    print(f"   {bitmap.getHeader().fsckCmd()} {file_name}")
    print()
    print(f"This virtual partition can be mounted as a read-only filesystem "
          f"at '{dir_name}' with this command:")
    mnt_type = bitmap.getHeader().mntType()
    print(f"   sudo mount -t {mnt_type} {file_name} {dir_name} -o loop,ro")
    print()
    print(f"Forking subprocess to enter event-loop. When done unmount "
          f"'{os.path.abspath(mountpoint)}' to quit this event-loop and "
          "its subprocess:")
    print(f"   sudo umount {dir_name}; umount {dir_name}")
    print()
    if os.fork() == 0:
        fuse_options = set(pyfuse3.default_options)
        fuse_options.add('fsname=vpartclone')
        fuse_options.add('allow_other')
        if debug:
            fuse_options.add('debug')

        pyfuse3_asyncio.enable()
        pyfuse3.init(fs, mountpoint, fuse_options)

        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(pyfuse3.main())
        except Exception:
            pass

        loop.close()
        pyfuse3.close(unmount=True)
