from pathlib import Path
import shutil


class FileService:
    def create_folder(self, path: str | Path):
        """
        Create a folder at the given path.
        If the folder already exists, nothing happens.

        :param path: Path where the folder should be created
        :return: Path object of the created folder
        """
        p = Path(path)
        p.mkdir(parents=True, exist_ok=True)
        return p

    def delete_folder(self, path: str | Path):
        """
        Delete a folder at the given path.
        Deletion is recursive.

        :param path: Path of the folder to delete
        """
        p = Path(path)
        if p.exists() and p.is_dir():
            shutil.rmtree(p)

    def copy(self, source: str | Path, destination: str | Path):
        """
        Copy a file or directory from source to destination.

        :param source: Source path
        :param destination: Destination path
        """
        src = Path(source)
        dst = Path(destination)

        if not src.exists():
            raise FileNotFoundError(f"Source path does not exist: {src}")

        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
