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
['bitsandbytes',
 'einops',
 'fairscale==0.4.0',
 'pytest',
 'timm',
 'torch',
 'triton',
 'typing']

setup_kwargs = {
    'name': 'zetascale',
    'version': '0.2.7',
    'description': 'Transformers at zeta scales',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Zeta - Seamlessly Create Zetascale Transformers\n\n\n[![Docs](https://readthedocs.org/projects/zeta/badge/)](https://zeta.readthedocs.io)\n\n<p>\n  <a href="https://github.com/kyegomez/zeta/blob/main/LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>\n  <a href="https://pypi.org/project/zetascale"><img alt="MIT License" src="https://badge.fury.io/py/zetascale.svg" /></a>\n</p>\n\nCreate Ultra-Powerful Multi-Modality Models Seamlessly and Efficiently\n\n## Installation\n\nTo install:\n```\npip install zetascale\n```\n\nTo get hands-on and develop it locally:\n```\ngit clone https://github.com/kyegomez/zeta.git\ncd zeta\npip install -e .\n```\n\n## Initiating Your Journey\n\nCreating a model empowered with the aforementioned breakthrough research features is a breeze. Here\'s how to quickly materialize the renowned Flash Attention\n\n```python\nimport torch\nfrom zeta import FlashAttention\n\nq = torch.randn(2, 4, 6, 8)\nk = torch.randn(2, 4, 10, 8)\nv = torch.randn(2, 4, 10, 8)\n\nattention = FlashAttention(causal=False, dropout=0.1, flash=True)\noutput = attention(q, k, v)\n\nprint(output.shape) \n\n```\n\n\n## Acknowledgments\n\nZeta is a masterpiece inspired by LucidRains\'s repositories and elements of [FairSeq](https://github.com/facebookresearch/fairseq) and [UniLM](https://github.com/kyegomez/unilm).\n\n## Citations\n\nIf our work here in Zeta has aided you in your journey, please consider acknowledging our efforts in your work. You can find relevant citation details in our [Citations Document](citations.md).\n\n## Contributing\nWe\'re dependent on you for contributions, it\'s only Kye maintaining this repository and it\'s very difficult and with that said any contribution is infinitely appreciated by not just me but by Zeta\'s users who dependen on this repository to build the world\'s\nbest AI models\n\n* Head over to the project board to look at open features to implement or bugs to tackle\n\n\n## Todo\n* Head over to the project board to look at open features to implement or bugs to tackle\n',
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
