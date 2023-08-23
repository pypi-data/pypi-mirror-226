import os
from typing import Iterable, List, Dict, Set
from dataclasses import dataclass
import pytest
from urllib3.connectionpool import HTTPConnectionPool


class SandboxError(Exception):
    pass


@pytest.fixture(autouse=True)
def no_http_requests(monkeypatch):
    allowed_hosts = {"localhost", "0.0.0.0"}
    original_urlopen = HTTPConnectionPool.urlopen

    def urlopen_mock(self, method, url, *args, **kwargs):
        if self.host in allowed_hosts:
            return original_urlopen(self, method, url, *args, **kwargs)

        raise SandboxError(
            f"Tests aren't allowed to make network requests. The test attempted: {method} {self.scheme}://{self.host}{url}"
        )

    monkeypatch.setattr(
        "urllib3.connectionpool.HTTPConnectionPool.urlopen", urlopen_mock
    )


@pytest.fixture(autouse=False)
def mock_file_system(fs):
    yield fs


@dataclass
class MockFileData:
    data: bytes


class MockFile:
    def __init__(
        self, file_data: MockFileData, mode: str = "r"  # type: ignore
    ) -> None:
        self.file_data = file_data
        self.mode = mode
        self.seek_pos = 0

    def close(self) -> bool:
        return True

    def write(self, __b) -> int:  # type: ignore
        if self.mode == "a":
            self.file_data.data += __b
        elif self.mode == "w":
            self.file_data.data = __b
        else:
            raise PermissionError("File not opened for writing")
        self.seek_pos = len(self.file_data.data)
        return len(__b)

    def read(self, __size: int = -1):
        if __size == -1:
            data_to_return = self.file_data.data[self.seek_pos :]
            self.seek_pos = len(self.file_data.data)
            return data_to_return
        else:
            data_to_return = self.file_data.data[self.seek_pos : self.seek_pos + __size]
            self.seek_pos = max(self.seek_pos + __size, len(self.file_data.data))
            return data_to_return

    def writelines(self, __lines: Iterable[str]) -> None:
        self.write("\n".join(__lines))

    def readline(self, __size: int = -1) -> bytes:
        lines = self.readlines()
        if lines:
            return lines[0]
        else:
            return b""

    def readlines(self, *args) -> List[bytes]:
        return self.read().splitlines()

    def seek(self, offset: int, __whence: int = -1) -> int:
        self.seek_pos = max(offset, len(self.file_data.data))
        return self.seek_pos


class MockOsModule:
    def __init__(self):
        self.current_dir = ""
        self.files: Dict[str, MockFileData] = {}
        self.dirs: Set[str] = {".", "/"}

    def _check_dir(self, dir_name):
        if dir_name not in self.dirs and dir_name != "":
            raise FileNotFoundError(
                f"mock - Directory {dir_name} not found, {self.dirs}"
            )

    def open(self, name, mode="r", **kwargs) -> MockFile:
        dir_name = os.path.dirname(name)
        self._check_dir(dir_name)

        if name not in self.files:
            if mode in ("w", "a"):
                self.files[name] = MockFileData(data=b"")
            else:
                raise FileNotFoundError(f"File {name} not found")

        return MockFile(self.files[name], mode=mode)

    def chdir(self, dir_name):
        self._check_dir(dir_name)
        self.current_dir = dir_name

    # def chown(self):
    #     ...

    # def chmod(self):
    #     ...

    def remove(self, file_path):
        if file_path not in self.files:
            raise FileNotFoundError(f"File {file_path} not found")
        self.files.pop(file_path)

    def rename(self, old_path, new_path):
        if old_path not in self.files:
            raise FileNotFoundError(f"File {old_path} not found")
        if new_path in self.files:
            raise FileExistsError(f"File {new_path} already exists")
        self.files[new_path] = self.files.pop(old_path)

    # def renames(self):
    #     ...

    # def replace(self):
    #     ...

    def rmdir(self, dir_path):
        if dir_path not in self.dirs:
            raise FileNotFoundError(f"Directory {dir_path} not found")
        self.dirs.remove(dir_path)

    def mkdir(self, dir_path, **kwargs):
        if dir_path in self.dirs:
            raise FileExistsError(f"Directory {dir_path} already exists")
        if dir_path in self.files:
            raise FileExistsError(f"File {dir_path} already exists")

        self._check_dir(os.path.dirname(dir_path))
        self.dirs.add(dir_path)

    def makedirs(self, dir_path, mode=0o777, exist_ok=False):
        if dir_path in self.files:
            raise FileExistsError(f"File {dir_path} already exists")

        splits = dir_path.split(os.path.sep)
        for i in range(len(splits)):
            dir_name = os.path.sep.join(splits[:i])
            if dir_name in self.files:
                if not exist_ok:
                    raise FileExistsError(f"File {dir_name} already exists")
            else:
                self.dirs.add(dir_name)

    def getcwd(self):
        return self.current_dir

    def getcwdb(self):
        return self.current_dir.encode("utf-8")
