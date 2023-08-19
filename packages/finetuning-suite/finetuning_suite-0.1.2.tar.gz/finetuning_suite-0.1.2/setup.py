# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['finetuning_suite']

package_data = \
{'': ['*']}

install_requires = \
['datasets', 'peft', 'torch', 'transformers']

setup_kwargs = {
    'name': 'finetuning-suite',
    'version': '0.1.2',
    'description': 'A fine-tuning suite based on Transformers and LoRA.',
    'long_description': 'None',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
