# from pprint import pprint

from __future__ import annotations

import jsondiff
from pytest_regressions.data_regression import DataRegressionFixture

import gdsfactory as gf
from gdsfactory.cross_section import cross_section

gdspath = gf.PATH.gdsdir / "mzi2x2.gds"


def test_read_gds_hash2() -> None:
    c = gf.import_gds(gdspath)

    h = "7b4e39541c3886c9651b4bb37282f502ffc222eecc6fe116d85d8930815e51b6"
    assert c.hash_geometry() == h, f"h = {c.hash_geometry()!r}"


def test_read_gds_with_settings2(data_regression: DataRegressionFixture) -> None:
    c = gf.import_gds(gdspath, read_metadata=True, unique_names=False)
    data_regression.check(c.to_dict())


def test_import_gds_hierarchy() -> None:
    """Ensures we can load it from GDS + YAML and get the same component
    settings."""
    splitter = gf.components.mmi1x2(cross_section=cross_section)
    c1 = gf.components.mzi(splitter=splitter, cross_section=cross_section)
    # c1.write_gds(gdspath=gdspath, with_metadata=True)
    c2 = gf.import_gds(gdspath, read_metadata=True, unique_names=False)

    d1 = c1.to_dict()
    d2 = c2.to_dict()

    # we change the name, so there is no cache conflicts
    d1.pop("name")
    d2.pop("name")
    # d1.pop("ports")
    # d2.pop("ports")
    # c1.pprint()
    # c2.pprint()

    d = jsondiff.diff(d1, d2)

    # from pprint import pprint
    # pprint(d1)
    # pprint(d2)
    # pprint(d)
    assert len(d) == 0, d


def test_mix_cells_from_gds_and_from_function2() -> None:
    """Ensures not duplicated cell names.

    when cells loaded from GDS and have the same name as a function with
    @cell decorator

    """
    c = gf.Component("test_mix_cells_from_gds_and_from_function")
    _ = c << gf.components.mzi()
    _ = c << gf.import_gds(gdspath)
    _ = c.write_gds()


def _write() -> None:
    splitter = gf.components.mmi1x2(cross_section=cross_section)
    c1 = gf.components.mzi(splitter=splitter, cross_section=cross_section)
    c1.write_gds(gdspath=gdspath, with_metadata=True)


if __name__ == "__main__":
    _write()
    test_read_gds_hash2()
    # test_import_gds_hierarchy()
    # test_read_gds_with_settings2()
    # splitter = gf.components.mmi1x2(cross_section=cross_section)
    # c1 = gf.components.mzi(splitter=splitter, cross_section=cross_section)
    # c1.write_gds(gdspath=gdspath, with_metadata=True)
    # c2 = gf.import_gds(gdspath, read_metadata=True, unique_names=False)

    # d1 = c1.to_dict()
    # d2 = c2.to_dict()
    # d = jsondiff.diff(d1, d2)
