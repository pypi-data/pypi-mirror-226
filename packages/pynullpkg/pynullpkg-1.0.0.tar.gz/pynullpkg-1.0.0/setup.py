from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='pynullpkg',
    version='1.0.0',
    packages=['pynullpkg'],
    url='https://github.com/mminichino/python-test-package',
    license='MIT License',
    author='Michael Minichino',
    python_requires='>=3.6',
    install_requires=[
        'attrs',
    ],
    author_email='info@unix.us.com',
    description='Python Test Package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=["devops", "pytest"],
    classifiers=[
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: MIT License",
          "Intended Audience :: Developers",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Topic :: Software Development :: Libraries",
          "Topic :: Software Development :: Libraries :: Python Modules"],
)
