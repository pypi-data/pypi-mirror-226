# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cai_causal_graph']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=3.0.0,<4.0.0', 'numpy>=1.18.0,<2.0.0', 'pandas>=1.0.0,<3.0.0']

setup_kwargs = {
    'name': 'cai-causal-graph',
    'version': '0.1.1',
    'description': 'A Causal AI package for causal graphs.',
    'long_description': '# cai-causal-graph\n\n![causaLens logo](cl-logo.png)\n\n## From causaLens, a Causal AI package for causal graphs\nDocumentation, including a quickstart and code reference docs, can be found [here](https://causalgraph.causalens.com/).\n\n[![PyPI version](https://img.shields.io/pypi/v/cai-causal-graph.svg?color=informational)](https://pypi.org/project/cai-causal-graph/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cai-causal-graph.svg?color=informational)](https://pypi.org/project/cai-causal-graph/)\n[![LICENSE](https://img.shields.io/badge/License-Apache_2.0-informational.svg)](https://www.apache.org/licenses/LICENSE-2.0)\n\n![TEST](https://github.com/causalens/cai-causal-graph/workflows/MAIN-CHECKS/badge.svg?branch=main)\n![DEPENDENCIES](https://github.com/causalens/cai-causal-graph/workflows/DEPENDENCIES-CHECKS/badge.svg?branch=main) \n![RELEASE](https://github.com/causalens/cai-causal-graph/workflows/RELEASE/badge.svg) \n![POST-RELEASE](https://github.com/causalens/cai-causal-graph/workflows/POST-RELEASE/badge.svg?branch=main) \n\n[![LINTING: mypy](https://img.shields.io/badge/Linting-mypy-informational.svg)](https://mypy-lang.org/)\n[![SECURITY: bandit](https://img.shields.io/badge/Security-bandit-informational.svg)](https://github.com/PyCQA/bandit)\n![INTERROGATE](interrogate_badge.svg)\n\n> **Note**  \n> The current development cycle of this branch is `v0.1.x` (stable).\n \n## License\n\n`cai-causal-graph` is open source and licensed under the [Apache-2.0 license](https://github.com/causalens/cai-causal-graph/blob/main/LICENSE).\n',
    'author': 'causaLens',
    'author_email': 'opensource@causalens.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://causalgraph.causalens.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.12.0',
}


setup(**setup_kwargs)
