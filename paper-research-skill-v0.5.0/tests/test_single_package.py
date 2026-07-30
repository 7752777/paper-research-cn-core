from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class SinglePackageTests(unittest.TestCase):
    def test_package_exposes_only_the_primary_skill(self) -> None:
        import install

        self.assertEqual(install.SKILL_NAMES, ("paper-research-cn-core",))
        self.assertEqual(install.discover_skills(ROOT), ["paper-research-cn-core"])

    def test_prune_legacy_removes_only_known_split_skills(self) -> None:
        import install

        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary)
            for name in (*install.LEGACY_SKILL_NAMES, "unrelated-skill"):
                (destination / name).mkdir()

            actions = install.prune_legacy(destination, dry_run=False)

            self.assertEqual({item["skill"] for item in actions}, set(install.LEGACY_SKILL_NAMES))
            self.assertTrue((destination / "unrelated-skill").is_dir())
            self.assertTrue(all(not (destination / name).exists() for name in install.LEGACY_SKILL_NAMES))


if __name__ == "__main__":
    unittest.main()
