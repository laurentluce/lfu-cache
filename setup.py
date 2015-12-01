from distutils.core import setup

setup(
    name='LFUCache',
    version='0.1',
    packages=['lfucache',],
    license='MIT',
    long_description='Cache with LFU eviction scheme implemented in Python with complexity O(1) for insertion, access and deletion.',
)
