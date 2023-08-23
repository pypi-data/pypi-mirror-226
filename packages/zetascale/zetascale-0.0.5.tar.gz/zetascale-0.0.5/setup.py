# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zeta',
 'zeta.models',
 'zeta.nn',
 'zeta.nn.architecture',
 'zeta.nn.attention',
 'zeta.nn.modules',
 'zeta.nn.modules.xmoe',
 'zeta.nn.utils',
 'zeta.training',
 'zeta.training.utils']

package_data = \
{'': ['*']}

install_requires = \
['einops',
 'fairscale==0.4.0',
 'pytest',
 'timm==0.6.13',
 'torch>=1.8,<2.0',
 'triton']

setup_kwargs = {
    'name': 'zetascale',
    'version': '0.0.5',
    'description': 'Transformers at zeta scales',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Zeta - A Library for Zetascale Transformers\n[![Docs](https://readthedocs.org/projects/zeta/badge/)](https://zeta.readthedocs.io)\n\nDocs for [Zeta](https://github.com/kyegomez/zeta).\n\n<p>\n  <a href="https://github.com/kyegomez/zeta/blob/main/LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>\n  <a href="https://pypi.org/project/zeta"><img alt="MIT License" src="https://badge.fury.io/py/zeta.svg" /></a>\n</p>\n\nZeta is a PyTorch-powered library, forged in the heart of the Halo array, that empowers researchers and developers to scale up Transformers efficiently and effectively. It leverages seminal research advancements to enhance the generality, capability, and stability of scaling Transformers while optimizing training efficiency.\n\n## Installation\n\nTo install:\n```\npip install zetascale\n```\n\nTo get hands-on and develop it locally:\n```\ngit clone https://github.com/kyegomez/zeta.git\ncd zeta\npip install -e .\n```\n\n## Initiating Your Journey\n\nCreating a model empowered with the aforementioned breakthrough research features is a breeze. Here\'s how to quickly materialize a BERT-like encoder:\n\n```python\n>>> from zeta import EncoderConfig\n>>> from zeta import Encoder\n\n>>> config = EncoderConfig(vocab_size=64000)\n>>> model = Encoder(config)\n\n>>> print(model)\n```\n\n\n## Acknowledgments\n\nZeta is a masterpiece inspired by elements of [FairSeq](https://github.com/facebookresearch/fairseq) and [UniLM](https://github.com/kyegomez/unilm).\n\n## Citations\n\nIf our work here in Zeta has aided you in your journey, please consider acknowledging our efforts in your work. You can find relevant citation details in our [Citations Document](citations.md).\n\n## Contributing\n\nWe\'re always thrilled to welcome new ideas and improvements from the community. Please check our [Contributor\'s Guide](contributing.md) for more details about contributing.\n\n\n* Create an modular omni-universal Attention class with flash multihead attention or regular mh or dilated attention -> then integrate into Decoder/ DecoderConfig\n\n\n',
    'author': 'Zeta Team',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/zeta',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
