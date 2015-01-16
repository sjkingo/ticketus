from setuptools import find_packages, setup

from ticketus import __version__ as version

setup(
    name='ticketus',
    version=version,
    license='BSD',
    author='Sam Kingston',
    author_email='sam@sjkwi.com.au',
    description='Ticketus is a simple, no-frills ticketing system for helpdesks.',
    url='https://github.com/sjkingo/ticketus',
    install_requires=[
        'Django >= 1.6.10',
        'IMAPClient',
        'django-grappelli',
        'email-reply-parser',
        'mistune',
        'psycopg2',
        'python-dateutil',
    ],
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=['ticketus_settings']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python',
        'Topic :: Communications :: Email',
        'Topic :: Software Development :: Bug Tracking',
        'Topic :: System :: Systems Administration',
    ],
    scripts=[
        'import_scripts/ticketus_import_freshdesk',
        'import_scripts/ticketus_import_github',
        'bin_scripts/ticketus_mailgw_imap4',
        'bin_scripts/ticketus-admin',
    ],
)
