from pathlib import Path
import pytest

from basic_ci.services.file_service import FileService


def test_create_folder_creates_directory(tmp_path: Path):
    fs = FileService()
    target = tmp_path / "a" / "b" / "c"

    created = fs.create_folder(target)

    assert created.exists()
    assert created.is_dir()
    assert created == target


def test_delete_folder_removes_directory_recursively(tmp_path: Path):
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
    fs = FileService()
    src = tmp_path / "src.txt"
    src.write_text("test")

    dst = tmp_path / "out" / "copied.txt"
    fs.copy(src, dst)

    assert dst.exists()
    assert dst.is_file()
    assert dst.read_text() == "test"


def test_copy_directory_copies_all_contents(tmp_path: Path):
    fs = FileService()
    src_dir = tmp_path / "srcdir"
    fs.create_folder(src_dir / "nested")
    (src_dir / "a.txt").write_text("A")
    (src_dir / "nested" / "b.txt").write_text("B")

    dst_dir = tmp_path / "dstdir"
    fs.copy(src_dir, dst_dir)

    assert (dst_dir / "a.txt").exists()
    assert (dst_dir / "nested" / "b.txt").exists()
    assert (dst_dir / "nested" / "b.txt").read_text() == "B"


def test_copy_raises_if_source_missing(tmp_path: Path):
    fs = FileService()
    missing = tmp_path / "nope"
    dst = tmp_path / "out"

    with pytest.raises(FileNotFoundError):
        fs.copy(missing, dst)
def test_create_folder_already_exists(tmp_path: Path):
    fs = FileService()
    target = tmp_path / "existing"
    target.mkdir()
    
    # This should not raise an exception
    fs.create_folder(target) 
    assert target.exists()

def test_copy_directory_merge(tmp_path: Path):
    """Verify that copy merges into an existing directory instead of crashing."""
    fs = FileService()
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    
    fs.create_folder(src)
    (src / "file1.txt").write_text("1")
    
    fs.create_folder(dst)
    (dst / "old.txt").write_text("old")
    
    fs.copy(src, dst)
    
    assert (dst / "file1.txt").exists()
    assert (dst / "old.txt").exists()  # Ensure existing files aren't wiped