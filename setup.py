try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='LFUCache',
    description='Cache with LFU eviction scheme.',
    version='1.0.0',
    packages=['lfucache',],
    license='MIT',
    author='Laurent Luce',
    author_email='laurentluce49@yahoo.com',
    url='https://github.com/laurentluce/lfu-cache',
    keywords='lfu cache insertion access deletion',
    long_description='Cache with LFU eviction scheme implemented in Python with complexity O(1) for insertion, access and deletion.',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)
