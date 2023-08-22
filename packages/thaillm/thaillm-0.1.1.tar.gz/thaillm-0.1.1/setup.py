from setuptools import setup,find_packages
 
with open("README.md", "r") as fh:
    long_description = fh.read() 

setup(name='thaillm',
    version='0.1.1',
    description='Thai large language model(LLM)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    author='bablueza',
    author_email='bablueza@gmail.com',
    license='MIT',
    packages = find_packages(where="src"),
    package_dir = {"": "src"},
    include_package_data=True,
    install_requires= ['transformers','sentencepiece'],
    python_requires='>=3.8')