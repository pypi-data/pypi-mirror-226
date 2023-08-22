from distutils.core import setup
setup(
    name = 'brof',
    packages = ['brof'],   
    version = '0.1',     
    license='MIT',        
    description = 'A CLI tool for keeping a file up to date with its copies in different locations',
    author = 'Artur C Segat',
    author_email = 'arturcamerasegat@gmail.com',
    url = 'https://github.com/ArturCSegat/brof',
    download_url = 'https://github.com/ArturCSegat/brof/archive/refs/tags/0.11.tar.gz',
    keywords = ['file', 'file management', 'CLI', 'tool'],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',      # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Intended Audience :: Developers',      
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
