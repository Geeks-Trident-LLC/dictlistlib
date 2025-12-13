"""Module containing the attributes for dictlistlib."""

from os import path

import compare_versions
import dateutil
import yaml

__version__ = '0.4.0a0'
version = __version__
__edition__ = 'Community'
edition = __edition__

__all__ = [
    'version',
    'edition',
    'Data'
]


class Data:
    # main app
    main_app_text = 'dictlistlib {}'.format(version)

    # packages
    compare_versions_text = 'compare_versions v{}'.format(compare_versions.__version__)
    compare_versions_link = 'https://pypi.org/project/compare_versions/'

    python_dateutil_text = 'python-dateutil v{}'.format(dateutil.__version__)   # noqa
    python_dateutil_link = 'https://pypi.org/project/python_dateutil/'

    pyyaml_text = 'pyyaml v{}'.format(yaml.__version__)
    pyyaml_link = 'https://pypi.org/project/PyYAML/'

    # company
    company = 'Geeks Trident LLC'
    company_url = 'https://www.geekstrident.com/'

    # URL
    repo_url = 'https://github.com/Geeks-Trident-LLC/dictlistlib'
    documentation_url = path.join(repo_url, 'blob/develop/README.md')
    license_url = path.join(repo_url, 'blob/develop/LICENSE')

    # License
    years = '2022-2040'
    license_name = 'BSD-3-Clause License'
    copyright_text = 'Copyright @ {}'.format(years)
    with open("LICENSE", encoding="utf-8") as f:
        license = f.read()

    @classmethod
    def get_dependency(cls):
        dependencies = dict(
            compare_versions=dict(
                package=cls.compare_versions_text,
                url=cls.compare_versions_link
            ),
            dateutil=dict(
                package=cls.python_dateutil_text,
                url=cls.python_dateutil_link
            ),
            pyyaml=dict(
                package=cls.pyyaml_text,
                url=cls.pyyaml_link
            )
        )
        return dependencies
