"""
这个是编写项目的打包配置信息
"""

from setuptools import setup

setup(
    name="pyhedy_current",
    packages=["pyhedy_current"],
    version = '0.0.1',
    # 配置插件模块
    entry_points={"pytest11": ["pyhedy_current = pyhedy_current.current"]},
    # custom PyPI classifier for pytest plugins
    classifiers=["Framework :: Pytest"],
)