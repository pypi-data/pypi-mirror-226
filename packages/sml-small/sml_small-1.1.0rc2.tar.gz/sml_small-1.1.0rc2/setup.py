# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sml_small',
 'sml_small.editing',
 'sml_small.editing.totals_and_components',
 'sml_small.utils']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.5,<2.0.0']

setup_kwargs = {
    'name': 'sml-small',
    'version': '1.1.0rc2',
    'description': 'SML Small (Python Pandas methods)',
    'long_description': '# SML-PYTHON-SMALL\n\n##### Statistical Methods Library for Python Pandas methods used in the **S**tatistical **P**roduction **P**latform (SPP).\n\nThis library contains pandas statistical methods that are *only suitable* for \nuse on *small* datasets which can safely be processed in-memory.\n\nFor documentation, please refer to the method-specific documentation in the \ndocs directory.\n\n\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
