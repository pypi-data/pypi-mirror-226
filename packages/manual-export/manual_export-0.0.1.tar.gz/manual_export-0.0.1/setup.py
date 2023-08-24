
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="manual_export",
    version="0.0.1",
    author="zhangxh1047",
    description="example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="",
    #project_urls={},
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8.6",
)
