from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name = 'rabbitmq-cli',
    version = '0.0.1',
    author = 'Brahian Ocampo',
    author_email = 'baocampo@bancolombia.com.co',
    license = 'GNU General Public License v3.0',
    # TODO: Add description
    description = '<short description for the tool>',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/brianou7/rabbitmqcli',
    py_modules = ['executor', 'app'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.9',
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        rabbitmq-cli=executor:cli
    '''
)
