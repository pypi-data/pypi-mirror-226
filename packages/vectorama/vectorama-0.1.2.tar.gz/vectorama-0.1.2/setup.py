# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vectorama', 'vectorama.api', 'vectorama.tests']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'vectorama',
    'version': '0.1.2',
    'description': '',
    'long_description': '# vectorama-python\n\n## Tests\n\n**Tests will clear out the current database as part of the test flows. Make sure you are only running a test server locally and you are not storing real data.**\n\nTests are intended to be run with a live vectorama server running on `localhost:50051`. We provide a docker-compose file for this purpose. To run the tests, first start the server:\n\n```bash\ndocker-compose up\n```\n\nThen, in a separate terminal, run the tests:\n\n```bash\npoetry run pytest\n```\n',
    'author': 'Pierce Freeman',
    'author_email': 'pierce@freeman.vc',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
