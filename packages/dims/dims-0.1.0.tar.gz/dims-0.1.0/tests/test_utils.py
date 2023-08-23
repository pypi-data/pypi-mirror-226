from pathlib import Path

import pytest

from dims.utils import read_all_recursively, get_unique_filenames, compare_paths

DATA_DIR = Path(__file__).parent.joinpath('data/')


def test_read_all_recursively():
    src_dir = DATA_DIR / 'src_tree'

    expected = [
        'a.txt',
        'b.txt',
        'c.txt',
        'd.ini',
        'foo',
        'foo/bar.txt',
        'foo/baz.ini',
        'foo/c.txt',
    ]

    assert sorted(read_all_recursively(src_dir)) == expected


def test_read_all_recursively_non_existing_path():
    with pytest.raises(ValueError) as exc_info:
        read_all_recursively(DATA_DIR / 'i do not exist')

    assert 'invalid path provided' in str(exc_info.value)


def test_read_all_recursively_file_as_path():
    with pytest.raises(ValueError) as exc_info:
        read_all_recursively(DATA_DIR / 'src_tree' / 'a.txt')

    assert 'provided path is not a directory' in str(exc_info.value)


def test_read_all_recursively_with_pattern():
    src_dir = DATA_DIR / 'src_tree'

    expected = [
        'd.ini',
        'foo/baz.ini',
    ]

    assert sorted(read_all_recursively(src_dir, pattern="*.ini")) == expected


def test_get_unique_filenames():
    src_dir = DATA_DIR / 'src_tree'

    expected = [
        'a.txt',
        'b.txt',
        'bar.txt',
        'baz.ini',
        'c.txt',
        'd.ini',
    ]

    assert sorted(get_unique_filenames(read_all_recursively(src_dir), src_dir)) == expected


def test_compare_paths():
    src_dir = DATA_DIR / 'src_tree'
    target_dir = DATA_DIR / 'target_tree'

    assert sorted(compare_paths(src_dir, target_dir)) == [
        'c.txt',
        'foo/baz.ini',
        'foo/c.txt'
    ]


def test_compare_paths_filenames_only():
    src_dir = DATA_DIR / 'src_tree'
    target_dir = DATA_DIR / 'target_tree'

    assert sorted(compare_paths(src_dir, target_dir, exact_paths=False)) == [
        'baz.ini',
        'c.txt',
    ]
