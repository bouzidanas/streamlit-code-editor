import setuptools
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "PROJECT.md").read_text()


setuptools.setup(
    name="streamlit-code-editor",
    version="0.1.12",
    author="Anas Bouzid",
    author_email="anasbouzid@gmail.com",
    description="React-ace editor customized for Streamlit",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/bouzidanas/streamlit-code-editor",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
    ],
)
