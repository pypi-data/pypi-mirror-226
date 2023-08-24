from setuptools import setup, find_packages

setup(
    name='df-xfyun-speech',
    version='0.1.0',
    author='Liu Lei',
    author_email='liu.lei@dfrobot.com',
    description='对讯飞语音合成\\识别WS API的封装',
    packages=find_packages(),
    python_requires='>=3.7.2',  # 设置适当的 Python 版本要求
    install_requires=[
        'websocket-client>=1.0.0',
    ],
)
