import setuptools

setuptools.setup(
    name="streamlit-code-editor",
    version="0.1.9",
    author="Anas Bouzid",
    author_email="anasbouzid@gmail.com",
    description="React-ace editor customized for Streamlit",
    long_description="React-ace component with custom themes wrapped with customizable interface elements for better integration as a Streamlit code editor",
    long_description_content_type="text/plain",
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
