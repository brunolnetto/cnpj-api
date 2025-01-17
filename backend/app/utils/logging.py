from os import remove, scandir, path
from shutil import rmtree


# Function to clear the latest 'n' items (files or folders)
def clear_folder_items(
    path_, remaining_items: int, key=lambda item: item.stat().st_ctime
):
    """
    Clears the latest 'n' items (files or folders) in the specified path.

    Args:
        path (str): The path to the directory containing the items.
        n (int): The number of latest items to clear.

    Raises:
        FileNotFoundError: If the specified path is not found.
        OSError: If an error occurs during removal.
    """
    if not path.exists(path_):
        raise FileNotFoundError(f"Path not found: {path_}")

    # Get all items sorted by modification time (newest first)
    items = sorted(scandir(path_), key=key)

    # Clear the latest 'n' items
    items_len = len(items)
    if items_len >= remaining_items:
        to_remove = items[0: items_len - remaining_items]

        for item in to_remove:
            if path.isfile(item.path):
                remove(item.path)
            else:
                # Remove directory (ignore errors)
                rmtree(item.path, ignore_errors=True)
