from distutils.core import setup
setup(
    name='thesaurus_generator',
    packages=['thesaurus_generator'],
    version='0.0.2',
    license='MIT',
    description='An automatic thesaurus generator.',
    author='José Alonso González',
    author_email='pegondo99@gmail.com',
    url='https://github.com/pegondo/thesaurus_generator',
    download_url='https://github.com/pegondo/thesaurus_generator/archive/refs/tags/0.0.2.tar.gz',
    keywords=['thesaurus', 'generation', 'automatic', 'nlp'],
    install_requires=[            # TODO: I get to this in a second
        'tensorflow_hub',
        'yake',
        'keybert',
        'pytextrank',
        'rake_nltk',
        'sentence_transformers',
        'nltk',
        'sklearn',
        'es_core_news_lg',
        'stanza',
        'pathlib',
        'json',
        'logging',
        'pandas',
        'numpy',
        'collections',
        're',
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.9',
    ],
)
