from os import makedirs, listdir, path
from shutil import rmtree

from backend.app.utils.logging import clear_folder_items


def test_clear_folder_items_success():
    """Tests clear_latest_items with successful removal."""
    tmp_path = "tests/tmp"
    rmtree(tmp_path, ignore_errors=True)

    makedirs(tmp_path, exist_ok=True)
    makedirs(f"{tmp_path}/1", exist_ok=True)
    makedirs(f"{tmp_path}/2", exist_ok=True)
    makedirs(f"{tmp_path}/3", exist_ok=True)

    def key_map(file):
        return file.path

    clear_folder_items(tmp_path, 2, key=key_map)

    listdir(tmp_path)

    assert not path.exists(f"{tmp_path}/1")
    assert path.exists(f"{tmp_path}/2")
    assert path.exists(f"{tmp_path}/3")


def test_clear_folder_items_key_name():
    """Tests clear_latest_items with a key name."""
    tmp_path = "tests/tmp"
    rmtree(tmp_path, ignore_errors=True)

    makedirs(tmp_path, exist_ok=True)
    makedirs(f"{tmp_path}/1", exist_ok=True)
    makedirs(f"{tmp_path}/2", exist_ok=True)
    makedirs(f"{tmp_path}/3", exist_ok=True)

    def key(item):
        return item.name

    clear_folder_items(tmp_path, 2, key=key)

    assert not path.exists(f"{tmp_path}/1")
    assert path.exists(f"{tmp_path}/2")
    assert path.exists(f"{tmp_path}/3")

    rmtree(tmp_path, ignore_errors=True)


def test_clear_folder_items_not_found():
    """Tests clear_latest_items with a non-existent path."""
    tmp_path = "tests/tmp"
    rmtree(tmp_path, ignore_errors=True)

    try:
        clear_folder_items(tmp_path, 2)
    except FileNotFoundError as e:
        assert str(e) == f"Path not found: {tmp_path}"
    else:
        assert False, "Expected FileNotFoundError."

    rmtree(tmp_path, ignore_errors=True)


def test_clear_folder_items_not_enough_items():
    """Tests clear_latest_items with fewer items than requested."""
    tmp_path = "tests/tmp"
    rmtree(tmp_path, ignore_errors=True)

    makedirs(tmp_path, exist_ok=True)
    makedirs(f"{tmp_path}/1", exist_ok=True)
    makedirs(f"{tmp_path}/2", exist_ok=True)

    clear_folder_items(tmp_path, 3)

    assert path.exists(f"{tmp_path}/1")
    assert path.exists(f"{tmp_path}/2")

    rmtree(tmp_path, ignore_errors=True)


def test_clear_folder_items_files():
    """Tests clear_latest_items with files."""
    tmp_path = "tests/tmp"
    rmtree(tmp_path, ignore_errors=True)

    makedirs(tmp_path, exist_ok=True)
    with open(f"{tmp_path}/1.txt", "w", encoding="utf8") as f:
        f.write("test")
    with open(f"{tmp_path}/2.txt", "w", encoding="utf8") as f:
        f.write("test")
    with open(f"{tmp_path}/3.txt", "w", encoding="utf8") as f:
        f.write("test")

    clear_folder_items(tmp_path, 2, key=lambda item: item.name)

    assert not path.exists(f"{tmp_path}/1.txt")
    assert path.exists(f"{tmp_path}/2.txt")
    assert path.exists(f"{tmp_path}/3.txt")

    rmtree(tmp_path, ignore_errors=True)
