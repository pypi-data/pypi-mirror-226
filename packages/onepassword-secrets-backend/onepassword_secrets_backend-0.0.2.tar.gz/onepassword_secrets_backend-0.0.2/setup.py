from distutils.core import setup

setup(
    name='onepassword_secrets_backend',
    packages=['onepassword_secrets_backend'],
    version='0.0.2',
    license='MIT',
    description='README.md',
    author='nmg-infra',
    url='https://github.com/namogoo/onepassword_secrets_backend',
    download_url='https://github.com/namogoo/onepassword_secrets_backend/archive/refs/tags/0.0.2.tar.gz',
    keywords=['1password', 'onepassword', 'secrets', 'backend', 'airflow'],
    install_requires=[
        'onepasswordconnectsdk==1.3.0',
        'apache-airflow>=2.5.1',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
