from sempy.fabric._environment import _get_environment

from typing import Any, Optional

import fsspec


class FSClient(object):
    """
    Class that contains the filesystem accessors for opening, deleting and listing
    files. All methods are  static.
    To implement other filesystems, you extend this class and override the static methods.
    """

    @staticmethod
    def open(*args, **kwargs):
        pass

    @staticmethod
    def realpath(path):
        pass

    @staticmethod
    def remove(path):
        pass

    @staticmethod
    def exists(path: str):
        pass

    @staticmethod
    def listdir(path: str):
        pass

    @staticmethod
    def makedirs(path: str, exist_ok=False):
        pass


class FsspecClient(object):
    """
    Class that contains the filesystem accessors for opening, deleting and listing
    files via calling the Fsspec API.
    FsspecClient: FsspecClient is an implementation of the FSclient that uses Fsspec
    fsspec : Filesystem interfaces for Python — https://filesystem-spec.readthedocs.io/en/latest/
    This comes with an entire battery of supported filesystems
    such as ADLS, local, hdfs e.t.c Furthermore, in Azure Synapse, Fsspec is preregistered with access
    tokens for working with files on the blob system in linked workspaces. This means via Fsspec we
    automatically get access to the all the filesystems and authentication supported by Synapse.
    The FsspecClient is the recommended client to use and should be sufficient for the majority of use
    cases in SemPy , especially when running on Synapse. Implementation is straight-forward. The client
    simply aliases the FSclient methods to their ffspec equivalents.
    """

    @staticmethod
    def open(*args, **kwargs):
        """
        Calls inbuilt python open and creates any intermediate directories if necessary

        Returns
        -------
        File
            opened file object
        """
        return fsspec.open(*args, **kwargs).open()

    @staticmethod
    def realpath(path):
        """
        Calls os.path.realpath to return canonical paths

        Parameters
        ----------
        path : str
            input path

        Returns
        -------
        str
            real path
        """
        return fsspec.open(path).full_name

    @staticmethod
    def remove(path):
        """
        Removes a file or directory only containing files

        Parameters
        ----------
        path : str
            path to file or dir
        """
        if FsspecClient.exists(path):
            fs = fsspec.open(path).fs
            fs.delete(path, recursive=True)

    @staticmethod
    def exists(path: str):
        """
        calls fsspec.open(path).fs.exists(path) to check if a path exists

        Parameters
        ----------
        path : str
            path to check

        Returns
        -------
        bool
            true if path exists
        """
        return fsspec.open(path).fs.exists(path)

    @staticmethod
    def listdir(path: str):
        """
        Calls os.listdir to list files in dir

        Parameters
        ----------
        path : str
            path to dir

        Returns
        -------
        list(str)
            list of paths in dir
        """
        return fsspec.open(path).fs.ls(path)

    @staticmethod
    def makedirs(path: str, exist_ok=False):
        if FsspecClient.exists(path) and not exist_ok:
            raise OSError(f"Directory '{path}' already exists")
        fsspec.open(path).fs.mkdirs(path)


class LakehouseFsClient(FsspecClient):
    """
    Class that contains the filesystem accessors for opening, deleting and listing
    files via calling the notebookutils.mssparkutils.fs API.
    LakehouseFsClient: LakehouseFsClient is an implementation of FsspecClient that uses notebookutils.mssparkutils.fs
    notebookutils.mssparkutils.fs: Filesystem interfaces for Trident Lakehouse —
    https://review.learn.microsoft.com/en-us/trident-docs-private-preview/synapse-spark-developer-experience/trident-file-mount-api?branch=main.
    """

    @staticmethod
    def listdir(path: str):
        """
        Calls mssparkutils.fs.ls to list files in dir

        Parameters
        ----------
        path : str
            path to dir

        Returns
        -------
        list(str)
            list of paths in dir
        """
        from notebookutils import mssparkutils
        return [f.path for f in mssparkutils.fs.ls(path)]

    @staticmethod
    def makedirs(path: str, exist_ok=False):
        if FsspecClient.exists(path) and not exist_ok:
            raise OSError(f"Directory '{path}' already exists")
        from notebookutils import mssparkutils
        mssparkutils.fs.mkdirs(path)

    @staticmethod
    def remove(path):
        """
        Removes a file or directory only containing files

        Parameters
        ----------
        path : str
            path to file or dir
        """
        if LakehouseFsClient.exists(path):
            from notebookutils import mssparkutils
            mssparkutils.fs.rm(path, recurse=True)


fs_client: Optional[Any] = None


def _get_fsclient():
    global fs_client
    if fs_client is None:
        fs_client = LakehouseFsClient if _get_environment() != 'local' else FsspecClient
    return fs_client
