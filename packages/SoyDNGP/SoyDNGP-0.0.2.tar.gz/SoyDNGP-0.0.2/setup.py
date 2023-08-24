from setuptools import setup, find_packages
setup(name='SoyDNGP',
      version='0.0.2',
      description='A deeplearning driving bioinformatic toolkit.',
      author='XtLab',
      install_requires=['cupy', 'onnxruntime-gpu', 'torch', 'cudf', 'pyyaml', 'pandas'],
      packages=find_packages(),
      )
