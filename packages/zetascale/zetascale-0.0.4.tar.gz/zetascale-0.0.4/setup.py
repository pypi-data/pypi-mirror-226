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
 'zeta.nn.utils']

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
    'version': '0.0.4',
    'description': 'Transformers at zeta scales',
    'long_description': '# Zeta - A Transgalactic Library for Scalable Transformations\n\n<p>\n  <a href="https://github.com/kyegomez/zeta/blob/main/LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>\n  <a href="https://pypi.org/project/zeta"><img alt="MIT License" src="https://badge.fury.io/py/zeta.svg" /></a>\n</p>\n\nZeta is a PyTorch-powered library, forged in the heart of the Halo array, that empowers researchers and developers to scale up Transformers efficiently and effectively. It leverages seminal research advancements to enhance the generality, capability, and stability of scaling Transformers while optimizing training efficiency.\n\n## Installation\n\nTo install:\n```\npip install zetascale\n```\n\nTo get hands-on and develop it locally:\n```\ngit clone https://github.com/kyegomez/zeta.git\ncd zeta\npip install -e .\n```\n\n## Initiating Your Journey\n\nCreating a model empowered with the aforementioned breakthrough research features is a breeze. Here\'s how to quickly materialize a BERT-like encoder:\n\n```python\n>>> from zeta import EncoderConfig\n>>> from zeta import Encoder\n\n>>> config = EncoderConfig(vocab_size=64000)\n>>> model = Encoder(config)\n\n>>> print(model)\n```\n\nAdditionally, we support the `Decoder` and `EncoderDecoder` architectures:\n\n```python\n# To create a decoder model\n>>> from zeta import DecoderConfig\n>>> from zeta import Decoder\n\n>>> config = DecoderConfig(vocab_size=64000)\n>>> decoder = Decoder(config)\n>>> print(decoder)\n\n# To create an encoder-decoder model\n>>> from zeta import EncoderDecoderConfig\n>>> from zeta import EncoderDecoder\n\n>>> config = EncoderDecoderConfig(vocab_size=64000)\n>>> encdec = EncoderDecoder(config)\n>>> print(encdec)\n```\n\n## Key Features\n\nMost of the transformative features mentioned below can be enabled by simply setting the corresponding parameters in the `config`:\n\n```python\n>>> from zeta import EncoderConfig\n>>> from zeta import Encoder\n\n>>> config = EncoderConfig(vocab_size=64000, deepnorm=True, multiway=True)\n>>> model = Encoder(config)\n\n>>> print(model)\n```\n\nFor a complete overview of our key features, refer to our [Feature Guide](features.md).\n\n## Examples\n\nDiscover how to wield Zeta in a multitude of scenarios/tasks, including but not limited to:\n\n- Language\n  * [Decoder/GPT](examples/fairseq/README.md#example-gpt-pretraining)\n  * [Encoder-Decoder/Neural Machine Translation](examples/fairseq/README.md#example-machine-translation)\n  * [Encoder/BERT](examples/fairseq/README.md#example-bert-pretraining)\n\n- Vision\n  * ViT/BEiT [In progress]\n\n- Speech\n\n- Multimodal\n  * [Multiway Transformers/BEiT-3](https://github.com/kyegomez/unilm/tree/master/beit3)\n\nWe are working tirelessly to expand the collection of examples spanning various tasks (e.g., vision pretraining, speech recognition) and various deep learning frameworks (e.g., [DeepSpeed](https://github.com/kyegomez/DeepSpeed), [Megatron-LM](https://github.com/NVIDIA/Megatron-LM)). Your comments, suggestions, or contributions are welcome!\n\n## Results\n\nCheck out our [Results Page](results.md) to witness Zeta\'s exceptional performance in Stability Evaluations and Scaling-up Experiments.\n\n## Acknowledgments\n\nZeta is a masterpiece inspired by elements of [FairSeq](https://github.com/facebookresearch/fairseq) and [UniLM](https://github.com/kyegomez/unilm).\n\n## Citations\n\nIf our work here in Zeta has aided you in your journey, please consider acknowledging our efforts in your work. You can find relevant citation details in our [Citations Document](citations.md).\n\n## Contributing\n\nWe\'re always thrilled to welcome new ideas and improvements from the community. Please check our [Contributor\'s Guide](contributing.md) for more details about contributing.\n\n\n* Create an modular omni-universal Attention class with flash multihead attention or regular mh or dilated attention -> then integrate into Decoder/ DecoderConfig\n\n\n',
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
