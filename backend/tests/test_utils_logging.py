import os
import shutil

from backend.app.utils.logging import clear_folder_items


def test_clear_folder_items_success():
    """Tests clear_latest_items with successful removal."""
    tmp_path = "tests/tmp"
    shutil.rmtree(tmp_path, ignore_errors=True)

    os.makedirs(tmp_path, exist_ok=True)
    os.makedirs(f"{tmp_path}/1", exist_ok=True)
    os.makedirs(f"{tmp_path}/2", exist_ok=True)
    os.makedirs(f"{tmp_path}/3", exist_ok=True)

    clear_folder_items(tmp_path, 2)

    assert os.path.exists(f"{tmp_path}/1")
    assert not os.path.exists(f"{tmp_path}/2")
    assert os.path.exists(f"{tmp_path}/3")


def test_clear_folder_items_key_name():
    """Tests clear_latest_items with a key name."""
    tmp_path = "tests/tmp"
    shutil.rmtree(tmp_path, ignore_errors=True)

    os.makedirs(tmp_path, exist_ok=True)
    os.makedirs(f"{tmp_path}/1", exist_ok=True)
    os.makedirs(f"{tmp_path}/2", exist_ok=True)
    os.makedirs(f"{tmp_path}/3", exist_ok=True)

    def key(item):
        return item.name

    clear_folder_items(tmp_path, 2, key=key)

    assert not os.path.exists(f"{tmp_path}/1")
    assert os.path.exists(f"{tmp_path}/2")
    assert os.path.exists(f"{tmp_path}/3")

    shutil.rmtree(tmp_path, ignore_errors=True)


def test_clear_folder_items_not_found():
    """Tests clear_latest_items with a non-existent path."""
    tmp_path = "tests/tmp"
    shutil.rmtree(tmp_path, ignore_errors=True)

    try:
        clear_folder_items(tmp_path, 2)
    except FileNotFoundError as e:
        assert str(e) == f"Path not found: {tmp_path}"
    else:
        assert False, "Expected FileNotFoundError."

    shutil.rmtree(tmp_path, ignore_errors=True)


def test_clear_folder_items_not_enough_items():
    """Tests clear_latest_items with fewer items than requested."""
    tmp_path = "tests/tmp"
    shutil.rmtree(tmp_path, ignore_errors=True)

    os.makedirs(tmp_path, exist_ok=True)
    os.makedirs(f"{tmp_path}/1", exist_ok=True)
    os.makedirs(f"{tmp_path}/2", exist_ok=True)

    clear_folder_items(tmp_path, 3)

    assert os.path.exists(f"{tmp_path}/1")
    assert os.path.exists(f"{tmp_path}/2")

    shutil.rmtree(tmp_path, ignore_errors=True)


def test_clear_folder_items_files():
    """Tests clear_latest_items with files."""
    tmp_path = "tests/tmp"
    shutil.rmtree(tmp_path, ignore_errors=True)

    os.makedirs(tmp_path, exist_ok=True)
    with open(f"{tmp_path}/1.txt", "w") as f:
        f.write("test")
    with open(f"{tmp_path}/2.txt", "w") as f:
        f.write("test")
    with open(f"{tmp_path}/3.txt", "w") as f:
        f.write("test")

    clear_folder_items(tmp_path, 2)

    assert not os.path.exists(f"{tmp_path}/1.txt")
    assert os.path.exists(f"{tmp_path}/2.txt")
    assert os.path.exists(f"{tmp_path}/3.txt")

    shutil.rmtree(tmp_path, ignore_errors=True)
