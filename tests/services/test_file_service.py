from pathlib import Path
import pytest

from basic_ci.services.file_service import FileService


def test_create_folder_creates_directory(tmp_path: Path):
    """
    test_create_folder_creates_directory verifies that create_folder creates
    the full directory structure when the directory does not already exist.

    :param tmp_path: Temporary directory provided by pytest
    :return: None
    """
    fs = FileService()
    target = tmp_path / "a" / "b" / "c"

    created = fs.create_folder(target)

    assert created.exists()
    assert created.is_dir()
    assert created == target


def test_delete_folder_removes_directory_recursively(tmp_path: Path):
    """
    test_delete_folder_removes_directory_recursively verifies that delete_folder
    removes a directory and all its contents recursively.

    :param tmp_path: Temporary directory provided by pytest
    :return: None
    """
    fs = FileService()
    folder = tmp_path / "to_delete"
    sub = folder / "sub"
    fs.create_folder(sub)

    # create a file inside
    f = sub / "x.txt"
    f.write_text("test")

    fs.delete_folder(folder)

    assert not folder.exists()


def test_copy_file_creates_parent_and_copies_content(tmp_path: Path):
    """
    test_copy_file_creates_parent_and_copies_content verifies that copy_file
    creates missing parent directories and correctly copies file content.

    :param tmp_path: Temporary directory provided by pytest
    :return: None
    """
    fs = FileService()
    src = tmp_path / "src.txt"
    src.write_text("test")

    dst = tmp_path / "out" / "copied.txt"
    fs.copy_file(src, dst)

    assert dst.exists()
    assert dst.is_file()
    assert dst.read_text() == "test"



def test_copy_directory_copies_all_contents(tmp_path: Path):
    """
    test_copy_directory_copies_all_contents verifies that copy_directory
    recursively copies all nested files and subdirectories.

    :param tmp_path: Temporary directory provided by pytest
    :return: None
    """
    fs = FileService()
    src_dir = tmp_path / "srcdir"
    fs.create_folder(src_dir / "nested")
    (src_dir / "a.txt").write_text("A")
    (src_dir / "nested" / "b.txt").write_text("B")

    dst_dir = tmp_path / "dstdir"
    fs.copy_directory(src_dir, dst_dir)

    assert (dst_dir / "a.txt").exists()
    assert (dst_dir / "nested" / "b.txt").exists()
    assert (dst_dir / "nested" / "b.txt").read_text() == "B"


def test_copy_file_raises_if_source_missing(tmp_path: Path):
    """
    test_copy_file_raises_if_source_missing verifies that copy_file raises a
    FileNotFoundError when the source file does not exist.

    :param tmp_path: Temporary directory provided by pytest
    :return: None
    """
    fs = FileService()
    missing = tmp_path / "nope.txt"
    dst = tmp_path / "out" / "x.txt"

    with pytest.raises(FileNotFoundError):
        fs.copy_file(missing, dst)
def test_create_folder_already_exists(tmp_path: Path):
    """
    test_create_folder_already_exists verifies that create_folder does not raise
    an exception when the target directory already exists.

    :param tmp_path: Temporary directory provided by pytest
    :return: None
    """
    fs = FileService()
    target = tmp_path / "existing"
    target.mkdir()
    
    fs.create_folder(target) 
    assert target.exists()

def test_copy_directory_merge(tmp_path: Path):
    """
    test_copy_directory_merge verifies that copying a directory into an existing
    destination directory merges contents instead of overwriting or crashing.

    :param tmp_path: Temporary directory provided by pytest
    :return: None
    """
    fs = FileService()
    src = tmp_path / "src"
    dst = tmp_path / "dst"

    fs.create_folder(src)
    (src / "file1.txt").write_text("1")

    fs.create_folder(dst)
    (dst / "old.txt").write_text("old")

    fs.copy_directory(src, dst)

    assert (dst / "file1.txt").exists()
    assert (dst / "old.txt").exists()
def test_workspace_restriction_blocks_outside_paths(tmp_path: Path):
    """
    test_workspace_restriction_blocks_outside_paths verifies that when a base
    workspace is set, operations outside that workspace raise PermissionError.

    :param tmp_path: Temporary directory provided by pytest
    :return: None
    """
    workspace = tmp_path / "workspace"
    outside = tmp_path / "outside"
    outside.mkdir(parents=True, exist_ok=True)

    fs = FileService(workspace)
    fs.create_folder(workspace)

    with pytest.raises(PermissionError):
        fs.create_folder(outside / "should_fail")