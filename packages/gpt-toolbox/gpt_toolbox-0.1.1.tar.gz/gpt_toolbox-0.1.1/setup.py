from setuptools import setup

setup(
    name='gpt_toolbox',
    version='0.1.1',
    py_modules=['gpt_toolbox'],
    install_requires=[
        "openai",
        "weaviate-client",
        "tiktoken",
        "langchain",
    ]
)