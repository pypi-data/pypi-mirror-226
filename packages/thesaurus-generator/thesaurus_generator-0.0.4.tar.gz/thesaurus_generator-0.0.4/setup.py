from distutils.core import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='thesaurus_generator',
    packages=['thesaurus_generator'],
    version='0.0.4',
    license='MIT',
    description='An automatic thesaurus generator.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='José Alonso González',
    author_email='pegondo99@gmail.com',
    url='https://github.com/pegondo/thesaurus_generator',
    download_url='https://github.com/pegondo/thesaurus_generator/archive/refs/tags/0.0.4.tar.gz',
    keywords=['thesaurus', 'generation', 'automatic', 'nlp'],
    install_requires=[            # TODO: I get to this in a second
        'tensorflow_hub',
        'yake',
        'keybert',
        'pytextrank',
        'rake_nltk',
        'sentence_transformers',
        'nltk',
        'scikit-learn',
        'es_core_news_lg',
        'stanza',
        'pathlib',
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
