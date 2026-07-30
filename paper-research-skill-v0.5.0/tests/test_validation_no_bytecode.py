from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class PackageValidationTests(unittest.TestCase):
    def test_validation_does_not_write_bytecode_into_package(self) -> None:
        from validate_package import validate_package

        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "package"
            shutil.copytree(ROOT, package, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

            self.assertEqual(validate_package(package), [])
            self.assertEqual(list(package.rglob("__pycache__")), [])


if __name__ == "__main__":
    unittest.main()
