from setuptools import setup

setup(
    name = 'Codeforces',
    version = '0.1',
    py_modules = ['idne', 'parse'],
    install_requires = [
        'Click','robobrowser', 'requests'
    ],
    entry_points = '''
        [console_scripts]
        idne = idne:cli
		parse = parse:main
    ''',
)
