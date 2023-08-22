import setuptools

setuptools.setup(
    name="monita_icons",
    packages=["monita_icons"],
    data_files={"./monita_icons/vendor_map.json": ["vendor_map.json"]},
    include_package_data=True,
    version="0.2.13",
)
