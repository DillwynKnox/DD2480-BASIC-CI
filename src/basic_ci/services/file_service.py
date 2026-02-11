import shutil
from pathlib import Path


class FileService:
    def __init__(self, base_workspace: str | Path | None = None):
        """
        __init__ initializes the FileService with an optional base workspace.
        If a base workspace is provided, all filesystem operations are restricted
        to paths inside this workspace. If not provided, operations are unrestricted.

        :param base_workspace: Root directory that limits where filesystem operations
                               are allowed (string, Path, or None)
        :return: None
        """
        self.base_workspace = Path(base_workspace).resolve() if base_workspace else None

    def _safe_path(self, path: str | Path):
        """
        _safe_path validates and normalizes a path to ensure it is located inside
        the configured base workspace. The path is resolved to an absolute path
        before validation.

        :param path: Path to validate (string or Path)
        :return: Resolved Path object that is safe to use
        :raises PermissionError: If the path is outside the base workspace
        """
        p = Path(path).resolve()
        if self.base_workspace and not p.is_relative_to(self.base_workspace):
            raise PermissionError(
                f"Access denied: {p} is outside workspace {self.base_workspace}"
            )
        return p

    def create_folder(self, path: str | Path):
        """
        create_folder creates a directory at the given path.
        If the directory already exists, the function does nothing and does not
        raise an error. The path is validated against the base workspace if one
        is configured.

        :param path: Path where the folder should be created (string or Path)
        :return: Path object representing the created (or existing) folder
        """
        p = self._safe_path(path)
        p.mkdir(parents=True, exist_ok=True)
        return p

    def delete_folder(self, path: str | Path):
        """
        delete_folder deletes a directory recursively, including all files and
        subdirectories, if the directory exists. The deletion is only allowed
        if the path is inside the configured base workspace.

        :param path: Path of the folder to delete (string or Path)
        :return: None
        :raises PermissionError: If the path is outside the base workspace
        """
        p = self._safe_path(path)
        if p.exists() and p.is_dir():
            shutil.rmtree(p)

    def copy_file(self, source: str | Path, destination: str | Path):
        """
        copy_file copies a single file from a source path to a destination path.
        Parent directories of the destination are created automatically if needed.
        The destination path is validated against the base workspace.

        :param source: Path of the file to copy (string or Path)
        :param destination: Destination file path (string or Path)
        :return: None
        :raises FileNotFoundError: If the source file does not exist
        :raises ValueError: If the source path is not a file
        :raises PermissionError: If the destination is outside the base workspace
        """
        src = Path(source).resolve()
        dst = self._safe_path(destination)

        if not src.exists():
            raise FileNotFoundError(f"Source file not found: {src}")
        if not src.is_file():
            raise ValueError(f"Source is not a file: {src}")

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    def copy_directory(self, source: str | Path, destination: str | Path):
        """
        copy_directory copies a directory and all of its contents recursively
        from a source path to a destination path. The destination path is
        validated against the base workspace before copying.

        :param source: Path of the directory to copy (string or Path)
        :param destination: Destination directory path (string or Path)
        :return: None
        :raises FileNotFoundError: If the source directory does not exist
        :raises ValueError: If the source path is not a directory
        :raises PermissionError: If the destination is outside the base workspace
        """
        src = Path(source).resolve()
        dst = self._safe_path(destination)

        if not src.exists():
            raise FileNotFoundError(f"Source directory not found: {src}")
        if not src.is_dir():
            raise ValueError(f"Source is not a directory: {src}")

        shutil.copytree(src, dst, dirs_exist_ok=True)

def get_FileService() -> FileService:
    return FileService()