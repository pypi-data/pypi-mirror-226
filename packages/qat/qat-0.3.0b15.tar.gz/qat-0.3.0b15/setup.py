# (c) Copyright 2023, Qat’s Authors

import os, setuptools
  
setuptools.setup(
    name="qat",
    author="Quentin Derouault",
    author_email="quentin.derouault@gmail.com",
    url="https://gitlab.com/testing-tool/qat",
    version=os.environ.get('QAT_VERSION'),
    description="Qat library",
    packages=[
        "qat",
        "qat.internal",
        "qat.bin",
        "qat.bin.plugins", 
        "qat.gui", 
        "qat.gui.images", 
        "qat.templates", 
        "qat.templates.demo", 
        "qat.templates.scripts", 
        "qat.templates.steps"],
    package_dir={
        '': 'client'
    },
    package_data={
        'qat.bin': ['*', 'plugins/*'],
        'qat.gui': ['images/*'],
        'qat.templates': ['*', '*/*']
    },
    include_package_data=True,
    exclude_package_data={'qat.bin': ['plugins']},
    entry_points={
        'console_scripts': [
            'qat-gui = qat.gui.launcher:open_gui',
            'qat-create-suite = qat.templates.generator:create_suite',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: C++",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: BDD"
    ],
    python_requires='>=3.9',
    install_requires=[
        'behave',
        'sv_ttk',
    ]
)
