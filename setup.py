from setuptools import setup, find_packages

setup(
    name='CloudVoy',
    version='1.0.0',
    description='A library to upload YouTube videos to Instagram Reels automatically.',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'google-api-python-client',
        'yt-dlp',
        'boto3',
        'requests',
        'python-dotenv'
    ],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
