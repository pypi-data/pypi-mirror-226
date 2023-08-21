# -*- coding:utf-8 -*-


from setuptools import setup, find_packages

setup(
    name='zhuque',
    version='1.0.1',
    description='zhuque graph platform',
    author='zhuque',
    author_email='zhuquezhitu@zhejianglab.com',
    packages=find_packages(),
    py_modules=['zhuque_graph.nn.pytorch.model.NodeClassificationWgGNNModel','zhuque_graph.nn.pytorch.model.LinkPredictionWgGNNModel'],
    requires=[],  # 定义依赖
    license='GPL 3.0'
)


# python setup.py sdist
# python setup.py bdist_wheel
# twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
