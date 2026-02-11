import shutil
from pathlib import Path


class FileService:
    def __init__(self, base_workspace: str | Path | None = None) -> None:
        """
        Initialize the FileService with an optional base workspace.

        If a base workspace is provided, all filesystem operations are restricted
        to paths inside this workspace. If not provided, operations are unrestricted
        (use with caution).

        Args:
            base_workspace (Optional[Union[str, Path]]): Root directory that limits
                where filesystem operations are allowed. Defaults to None.

        Returns:
            None
        """
        self.base_workspace = Path(base_workspace).resolve() if base_workspace else None

    def _safe_path(self, path: str | Path) -> Path:
        """
        Validate and normalize a path to ensure it is inside the base workspace.

        This method resolves the given path to an absolute path and checks if it
        is located within the configured base workspace. If no base workspace is
        configured, the path is considered safe without validation.

        Args:
            path (Union[str, Path]): Path to validate and normalize

        Returns:
            Path: Resolved Path object that is safe to use

        Raises:
            PermissionError: If the path is outside the base workspace when a
                           base workspace is configured
        """
        p = Path(path).resolve()
        if self.base_workspace and not p.is_relative_to(self.base_workspace):
            raise PermissionError(
                f"Access denied: {p} is outside workspace {self.base_workspace}"
            )
        return p

    def create_folder(self, path: str | Path) -> Path:
        """
        Create a directory at the specified path.

        This method creates the directory and all necessary parent directories.
        If the directory already exists, it does nothing and does not raise an
        error. The path is validated against the base workspace if one is configured.

        Args:
            path (Union[str, Path]): Path where the folder should be created

        Returns:
            Path: Path object representing the created (or existing) folder

        Raises:
            PermissionError: If the path is outside the base workspace when a
                           base workspace is configured
        """
        p = self._safe_path(path)
        p.mkdir(parents=True, exist_ok=True)
        return p

    def delete_folder(self, path: str | Path) -> None:
        """
        Delete a directory and all its contents recursively.

        This method deletes the specified directory, including all files and
        subdirectories. If the directory does not exist, the method does nothing.
        The deletion is only allowed if the path is inside the configured base workspace.

        Args:
            path (Union[str, Path]): Path of the folder to delete

        Returns:
            None

        Raises:
            PermissionError: If the path is outside the base workspace when a
                           base workspace is configured
        """
        p = self._safe_path(path)
        if p.exists() and p.is_dir():
            shutil.rmtree(p)

    def copy_file(self, source: str | Path, destination: str | Path) -> None:
        """
        Copy a single file from a source path to a destination path.

        This method copies the source file to the destination path. Parent
        directories of the destination are created automatically if they don't exist.
        The destination path is validated against the base workspace, but the source
        path is not (as it may be outside the workspace, e.g., system files).

        Args:
            source (Union[str, Path]): Path of the file to copy
            destination (Union[str, Path]): Destination file path

        Returns:
            None

        Raises:
            FileNotFoundError: If the source file does not exist
            ValueError: If the source path is not a file (e.g., a directory)
            PermissionError: If the destination is outside the base workspace when
                           a base workspace is configured
        """
        src = Path(source).resolve()
        dst = self._safe_path(destination)

        if not src.exists():
            raise FileNotFoundError(f"Source file not found: {src}")
        if not src.is_file():
            raise ValueError(f"Source is not a file: {src}")

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    def copy_directory(self, source: str | Path, destination: str | Path) -> None:
        """
        Copy a directory and all of its contents recursively.

        This method copies the entire source directory tree to the destination path.
        If the destination directory already exists, files are merged (existing files
        may be overwritten). The destination path is validated against the base
        workspace, but the source path is not.

        Args:
            source (Union[str, Path]): Path of the directory to copy
            destination (Union[str, Path]): Destination directory path

        Returns:
            None

        Raises:
            FileNotFoundError: If the source directory does not exist
            ValueError: If the source path is not a directory
            PermissionError: If the destination is outside the base workspace when
                           a base workspace is configured
        """
        src = Path(source).resolve()
        dst = self._safe_path(destination)

        if not src.exists():
            raise FileNotFoundError(f"Source directory not found: {src}")
        if not src.is_dir():
            raise ValueError(f"Source is not a directory: {src}")

        shutil.copytree(src, dst, dirs_exist_ok=True)