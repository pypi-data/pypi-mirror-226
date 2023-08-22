# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gpt4', 'gpt4.utils']

package_data = \
{'': ['*']}

install_requires = \
['SentencePiece',
 'accelerate',
 'datasets',
 'deepspeed',
 'einops',
 'lion-pytorch',
 'matplotlib',
 'numpy',
 'torch',
 'transformers']

setup_kwargs = {
    'name': 'gpt4-torch',
    'version': '0.0.1',
    'description': 'GPT4 - Pytorch',
    'long_description': '# GPT4\nThe open source implementation of the base model behind GPT-4 from OPENAI [Language + Multi-Modal]\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/gpt3',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
