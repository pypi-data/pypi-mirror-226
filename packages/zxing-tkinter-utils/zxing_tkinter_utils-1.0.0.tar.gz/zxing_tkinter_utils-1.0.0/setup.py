from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()
"""
项目名称，版本，描述。
主页markdown内容。
需要上传的模块。
开源协议。
"""
setup(
	name='zxing_tkinter_utils',
	version='1.0.0',
	description='tkinter实用工具',
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=['zxing_tkinter_utils'],
	license="MIT"
)
