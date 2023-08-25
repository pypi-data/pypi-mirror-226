from gpao_utils import utils_store
from pathlib import Path, WindowsPath, PurePosixPath, PureWindowsPath
import pytest


if isinstance(Path("a"), WindowsPath):
    local_path = Path("L:/")
else:
    local_path = Path("/mnt/store1")


def test_to_unix_ok():
    store = utils_store.Store(local_path, "//store.example.fr/store1/", "/mnt/store1/")
    path_to_test = local_path / "toto.txt"
    assert store.to_unix(path_to_test) == PurePosixPath("/mnt/store1/toto.txt")


def test_to_unix_not_relative():
    store = utils_store.Store(local_path, "//store.example.fr/store1", "/mnt/store1/")
    # resolve path before sending to store to make sure it works on the current platform
    path_to_test = Path("./toto.txt").resolve()
    assert store.to_unix(path_to_test) == PurePosixPath(path_to_test)


def test_to_unix_nok():
    store = utils_store.Store(local_path, "//store.example.fr/store1/", None)
    path_to_test = local_path / "toto.txt"
    with pytest.raises(ValueError):
        store.to_unix(path_to_test)


def test_to_win_ok():
    store = utils_store.Store(local_path, "//store.example.fr/store1/", "/mnt/store1/")
    path_to_test = local_path / "toto.txt"
    assert store.to_win(path_to_test) == PureWindowsPath("//store.example.fr/store1/toto.txt")


def test_to_win_not_relative():
    store = utils_store.Store(local_path, "//store.example.fr/store1", "/mnt/store1/")
    # resolve path before sending to store to make sure it works on the current platform
    path_to_test = Path("./toto.txt").resolve()
    assert store.to_win(path_to_test) == PureWindowsPath(path_to_test)


def test_to_win_nok():
    store = utils_store.Store(local_path, None, "/mnt/store1/")
    path_to_test = local_path / "toto.txt"
    with pytest.raises(ValueError):
        assert store.to_win(path_to_test)


def test_to_win_case():
    store = utils_store.Store(local_path, "//store.example.fr/store1/", "/mnt/store1/")
    path_to_test = local_path / "TOTO.txt"
    assert store.to_win(path_to_test) == PureWindowsPath("//store.example.fr/store1/toto.txt")


def test_to_win_separator():
    if isinstance(Path("a"), WindowsPath):
        local_path = Path("\\\\store.example.fr\\store1")
    else:
        local_path = Path("/mnt/store1")
    store = utils_store.Store(local_path, "\\\\store.example.fr\\store2", "/mnt/store1/")
    path_to_test = local_path / "toto.txt"
    assert store.to_win(path_to_test) == PureWindowsPath("\\\\store.example.fr\\store2\\toto.txt")


def test_no_local_path():
    win_path = PureWindowsPath("//store1.example.fr/win_path")
    unix_path = PurePosixPath("/mnt/store1/unix_store")
    store = utils_store.Store(win_runner_path=win_path, unix_runner_path=unix_path)
    if isinstance(Path("a"), WindowsPath):
        assert store._local_path == win_path
    else:
        assert store._local_path == unix_path
