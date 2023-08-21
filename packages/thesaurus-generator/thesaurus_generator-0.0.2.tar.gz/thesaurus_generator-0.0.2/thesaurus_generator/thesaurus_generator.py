import tensorflow_hub as hub
import yake
from keybert import KeyBERT
import pytextrank
from rake_nltk import Rake
from sentence_transformers import SentenceTransformer, util
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import es_core_news_lg
import stanza
import pathlib
import json
import logging

import pandas as pd
import numpy as np
from collections import Counter
from re import search

# import spacy
import nltk
nltk.download('stopwords')
nltk.download('punkt')


class _TokenPair:
    """
    Class to define the pair of tokens that are inside the thesaurus.
    """

    def __init__(self, token_1, token_2):
        self.token_1 = token_1
        self.token_2 = token_2

    def __eq__(self, obj):
        if isinstance(obj, _TokenPair):
            return (self.token_1 is obj.token_1 and self.token_2 is obj.token_2) or (self.token_1 is obj.token_2 and self.token_2 is obj.token_1)
        return False

    def __str__(self):
        return f'{self.token_1} & {self.token_2}'


class ThesaurusGenerator:
    """
    Class to automatically generate thesaurus from a given text.

    Attributes:
        - `thesaurus` is the generated thesaurus. It will be None until `generate` is called.
        - `terms` is the list of extracted terms.
        - `filtered_terms` is the list of terms after filtered.
        - `token_pair_similarities` is a list of all the terms pairs and their similarity.

    Here is a summary of the configuration supported:
    - `verbose` defines if logs describing the process will appear or not.
    - `use_spacy` defines if you want the pipeline to use Spacy's pipeline or not. It is True by default, and should be
    True unless you have an incompatibility with Spacy: https://spacy.io/
    - `use_spacy` defines if you want the pipeline to use Stanza's pipeline or not. It is True by default, and should be
    True unless you have an incompatibility with Stanza: https://www.stanza.es/
    - `key_terms` defines the configuration to extract the most important terms from the text. If its value is `'auto'`,
    then the default configuration will be used. Here is the format of the configuration:
        - `config` defines the configuration used to extract the most important terms of each length. This piece of
        configuraiton is an array of objects, where the object at index `i` defines the configuration used to extract
        terms formed by `i-1` words. It must contain three objects. Here is what each object must contain:
            - `criteria` defines the criteria used to extract the key words. It can be `tf-idf`, which will point the 
            relevance of each term based on a TF-iDF index; `text-relevance`, which will point the relevance of each term
            according to the similarity between the embedding of the whole text and the embedding of the term; or `both`,
            which is the average of each metric.
            - `ratio` defines the ratio of the elements with the highest score that will be kept. E.g: a ratio of 0.05
            indicates that the 5% of the terms with the higher score will be kept.
            - `remove_stop_words` defines a criteria to remove stop words. The possible values are `None`, which indicates
            that the stop words will not be removed; `'hard'` that indicates that the terms that contain any stop word will
            be discarted; and `'soft'` that only discards the terms that are totally formed by stop words.
        - `stop_words` is a list with stop words to be considered.
    - `key_terms_from_models` defines the configuration used to extract the key terms using external models. If the value is
    `'auto'`, the default configuration is loaded. Here is a description of the configuration:
        - `models` defines the models to be used in a string format with the models separated using a comma. E.g:
        `textrank,keybert,yake`. The models available are count, keybert, rake, spacy, textrank and yake.
        - `verbose` defines if the model will log the amount of terms that were extracted using every model.
        - `count.ratio` defines the ratio of terms to be kept when using the count model. This model considers more important
        the terms that are most repeated in the text.
        - `keybert` defines the configurations to use for this model. As KeyBERT (https://github.com/MaartenGr/KeyBERT) model
        has a wide variarity of configuration, this piece of configuration supports an array of configurations, that will be
        used to extract terms using the model and will be joined once all the configurations are run. Here is the format of the
        configuration. Each element must contain an object with the following configuration: `diversity`, `nr_candidates`,
        `num_terms`, `use_maxsum` and `use_mmr`. Here you can find the meaning of each property: https://github.com/MaartenGr/KeyBERT
        - `rake.ratio` defines the ratio of terms to be kept when using the rake model. This model considers more important
        the terms that are most repeated in the text. https://pypi.org/project/rake-nltk/
        - `spacy.ratio` defines the ratio of terms to be kept when using the spacy model. This model considers more important
        the terms that are most repeated in the text. https://spacy.io/
        - `textrank.ratio` defines the ratio of terms to be kept when using the textrank model. This model considers more important
        the terms that are most repeated in the text. https://github.com/davidadamojr/TextRank
        - `yake.ratio` defines the ratio of terms to be kept when using the yake model. This model considers more important
        the terms that are most repeated in the text. https://pypi.org/project/yake/
    - `special_characters` is a list of characters that when a term contains them it will be removed. You can provide an
    empty array to disable this feature.
    - `filter_terms` defines the criteria used to discard the irrelevant terms. If its value is `'auto'`, then the default
    configuration will be used. Here is the format of the configuration:
        - `criteria` defines the criteria to filter terms. If the value is `'included'`, then the terms that match the patterns
        in `included_pos_tagging` will be included; and if its value is `'excluded'`, then the terms that do not match the
        patterns in `excluded_pos_tagging` will be discarted.
        - `pos_tagging_groups` defines a mapping between keywords and Spacy POS tagging terms (https://web.archive.org/web/20190206204307/https://www.clips.uantwerpen.be/pages/mbsp-tags).
        - `included_pos_tagging` is a list of patterns that will be included in the terms extracted. Each element is a list of
        elements used as keys in `pos_tagging_groups`.
        - `excluded_pos_tagging` is a list of patterns that will be excluded in the terms extracted. Each element is a list of
        elements used as keys in `pos_tagging_groups`.
    - `similarity` defines the similarity measure between the terms that appear in the generated thesaurus. If its value is
    `'auto'`, then the default configuration will be used. Here is the format of the configuration:
        - `metric` is the metric used to calculate the similarity. It can be `'spacy'`, which uses the document similarity
        defined by Spacy (https://spacy.io/api/doc); `'transformers'`, which uses the similarity defined in sentence_transformers
        (https://pypi.org/project/sentence-transformers/); or `'tfhub'`, which uses the similarity defined in this TF-hub model:
        https://tfhub.dev/google/universal-sentence-encoder/4
        - `remove_stop_words` if the stop words in the terms are removed before running the metric.
    - `thesaurus_similarity_threshold` defines the minumum score of relevance needed between two terms to be included in the
    generated thesaurus.

    Here is the default configuration:
    ```json
    {
        'verbose': False,
        'use_spacy': True,
        'use_stanza': True,
        'key_terms':
            {
                'config':
                            [
                                {
                                    'criteria': 'text-relevance',
                                    'ratio': 0.05,
                                    'remove_stop_words': 'soft'
                                },
                                {
                                    'criteria': 'text-relevance',
                                    'ratio': 0.05,
                                    'remove_stop_words': 'soft'
                                },
                                {
                                    'criteria': 'text-relevance',
                                    'ratio': 0.02,
                                    'remove_stop_words': 'soft'
                                }
                            ],
               'stop_words': `nltk.corpus.stopwords.words('spanish')`
            },
        'key_terms_from_models':
            {
                'models': 'textrank,keybert,yake',
                'verbose': False,
                'count': {'ratio': 0.2},
                'keybert':
                    [
                        {
                            'diversity': 0.5,
                            'nr_candidates': 20,
                            'num_terms': 15,
                            'use_maxsum': False,
                            'use_mmr': False
                        },
                        {
                            'diversity': 0.5,
                            'nr_candidates': 20,
                            'num_terms': 15,
                            'use_maxsum': True,
                            'use_mmr': False
                        },
                        {
                            'diversity': 0.7,
                            'nr_candidates': 20,
                            'num_terms': 15,
                            'use_maxsum': False,
                            'use_mmr': True
                        },
                        {
                            'diversity': 0.2,
                            'nr_candidates': 20,
                            'num_terms': 15,
                            'use_maxsum': False,
                            'use_mmr': True
                        }
                    ],
                'rake': {'ratio': 0.1},
                'spacy': {'ratio': 0.1},
                'textrank': {'ratio': 0.2},
                'yake': {'num_terms': 125}
            },
        'special_characters': ['𝒇', '𝑓', '𝒈', 'α'],
        'filter_terms':
            {
                'criteria': 'included',
                'pos_tagging_groups':
                    {
                        'ADJ': ['ADJ'],
                        'ADV': ['ADV'],
                        'DET': ['DET', 'ADP', 'SCONJ', 'CCONJ'],
                        'NOUN': ['NOUN', 'PROPN', 'NUM'],
                        'OTHER': ['PUNCT', 'SPACE', 'PART', 'SYM', 'INTJ', 'X'],
                        'PRON': ['PRON'],
                        'VERB': ['VERB', 'AUX']
                    }
                'excluded_pos_tagging':
                    [
                        ['PRON'],
                        ['ADJ'],
                        ['DET'],
                        ['ADV'],
                        ['OTHER'],
                        ['DET', 'NOUN'],
                        ['*', 'DET'],
                        ['DET', 'VERB'],
                        ['DET', 'PRON'],
                        ['DET', 'ADJ'],
                        ['DET', 'ADV'],
                        ['DET', 'OTHER'],
                        ['DET', 'DET', '*'],
                        ['*', 'DET', 'DET'],
                        ['*', '*', 'DET']
                    ],
                'included_pos_tagging':
                    [
                        ['NOUN'],
                        ['NOUN', 'ADJ'],
                        ['NOUN', 'ADV', 'ADJ'],
                        ['NOUN', 'DET', 'NOUN']
                    ],
            },
        'similarity':
            {
                'metric': 'transformers',
                'remove_stop_words': True
            },
        'thesaurus_similarity_threshold': 0.8  
    }
    ```
    """

    def __init__(self, config={
        'verbose': False,
        'use_spacy': True,
        'use_stanza': True,
        'key_terms': 'auto',
        'key_terms_from_models': 'auto',
        'special_characters': ['𝒇', '𝑓', '𝒈', 'α'],
        'filter_terms': 'auto',
        'similarity': 'auto',
        'thesaurus_similarity_threshold': 0.8
    }):
        # Assign and validate the configuration provided.
        self.__config = config
        self.__build_config()
        self.__validate_config()

        # Load the models
        self.__spacy_nlp = es_core_news_lg.load(
        ) if self.__config['use_spacy'] else None
        self.__stanza_nlp = stanza.Pipeline(
            lang='es', processors='tokenize,depparse,lemma,pos') if self.__config['use_stanza'] else None

    def __build_config(self):
        """Compliments the configuration in self.__config."""
        if 'key_terms' in self.__config and self.__config['key_terms'] == 'auto':
            self.__config['key_terms'] = {
                'config': [
                    # 1-word terms:
                    {
                        'ratio': 0.05,
                        'criteria': 'text-relevance',
                        'remove_stop_words': 'soft'
                    },
                    # 2-words terms:
                    {
                        'ratio': 0.05,
                        'criteria': 'text-relevance',
                        'remove_stop_words': 'soft'
                    },
                    # 3-words terms:
                    {
                        'ratio': 0.02,
                        'criteria': 'text-relevance',
                        'remove_stop_words': 'soft'
                    },
                ],
                'stop_words': stopwords.words('spanish')
            }

        if 'key_terms_from_models' in self.__config and self.__config['key_terms_from_models'] == 'auto':
            self.__config['key_terms_from_models'] = {
                'models': 'textrank,keybert,yake',
                'spacy': {
                    'ratio': 0.1
                },
                'rake': {
                    'ratio': 0.1
                },
                'textrank': {
                    'ratio': 0.2
                },
                'count': {
                    'ratio': 0.2
                },
                'keybert': [
                    {
                        'num_terms': 15,
                        'use_maxsum': False,
                        'nr_candidates': 20,
                        'use_mmr': False,
                        'diversity': 0.5,
                    },
                    {
                        'num_terms': 15,
                        'use_maxsum': True,
                        'nr_candidates': 20,
                        'use_mmr': False,
                        'diversity': 0.5,
                    },
                    {
                        'num_terms': 15,
                        'use_maxsum': False,
                        'nr_candidates': 20,
                        'use_mmr': True,
                        'diversity': 0.7
                    },
                    {
                        'num_terms': 15,
                        'use_maxsum': False,
                        'nr_candidates': 20,
                        'use_mmr': True,
                        'diversity': 0.2
                    }
                ],
                'yake': {
                    'num_terms': 125
                },
                'verbose': False
            }

        if 'special_characters' not in self.__config:
            self.__config['special_characters'] = []

        if 'filter_terms' in self.__config and self.__config['filter_terms'] == 'auto':
            self.__config['filter_terms'] = {
                'criteria': 'included',
                'pos_tagging_groups': {
                    'NOUN': [
                        'NOUN',
                        'PROPN',
                        'NUM'
                    ],
                    'PRON': ['PRON'],
                    'ADJ': ['ADJ'],
                    'DET': [
                        'DET',
                        'ADP',
                        'SCONJ',
                        'CCONJ'
                    ],
                    'VERB': [
                        'VERB',
                        'AUX'
                    ],
                    'ADV': ['ADV'],
                    'OTHER': [
                        'PUNCT',
                        'SPACE',
                        'PART',
                        'SYM',
                        'INTJ',
                        'X'
                    ]
                },
                'included_pos_tagging': [
                    # 1-term
                    ['NOUN'],
                    # 2-terms
                    ['NOUN', 'ADJ'],
                    # 3-terms
                    ['NOUN', 'ADV', 'ADJ'],
                    ['NOUN', 'DET', 'NOUN'],
                ],
                'excluded_pos_tagging': [
                    # 1-term:
                    ['PRON'],
                    ['ADJ'],
                    ['DET'],
                    ['ADV'],
                    ['OTHER'],
                    # 2-terms:
                    ['DET', 'NOUN'],
                    ['*', 'DET'],
                    ['DET', 'VERB'],
                    ['DET', 'PRON'],
                    ['DET', 'ADJ'],
                    ['DET', 'ADV'],
                    ['DET', 'OTHER'],
                    # 3-terms:
                    ['DET', 'DET', '*'],
                    ['*', 'DET', 'DET'],
                    ['*', '*', 'DET'],
                ]
            }

        if 'similarity' in self.__config and self.__config['similarity'] == 'auto':
            self.__config['similarity'] = {
                'remove_stop_words': True,
                'metric': 'transformers'
            }

    def __validate_config(self):
        """Validates the configuration in self.__config"""
        assert self.__config is not None, 'The configuration must be provided'

        assert 'verbose' in self.__config, '`verbose` configuration must be provided'

        assert 'use_spacy' in self.__config, '`use_spacy` configuration must be provided'
        assert self.__config['use_spacy'] == True or self.__config['use_spacy'] == True, '`use_spacy` must be either True or False'

        assert 'use_stanza' in self.__config, '`use_stanza` configuration must be provided'
        assert self.__config['use_stanza'] == True or self.__config['use_stanza'] == True, '`use_stanza` must be either True or False'

        assert 'key_terms' in self.__config, '`key_terms` configuration must be provided'
        assert 'stop_words' in self.__config['key_terms'], '`key_terms.stop_words` configuration must be provided'
        assert 'config' in self.__config['key_terms'], '`key_terms.config` configuration must be provided'
        assert isinstance(
            self.__config['key_terms']['config'], list), '`key_terms` must be a list'
        for config in self.__config['key_terms']['config']:
            assert 'ratio' in config, '`key_terms` elements must define a ratio'
            assert 'criteria' in config, '`key_terms` elements must define a criteria'
            criteria = config['criteria']
            assert criteria == "tf-id" or criteria == "text-relevance" or "both", "The criteria must be `tf-id`, `text-relevance` or `both`"
            assert 'remove_stop_words' in config, '`key_terms` elements must define a remove_stop_words'
            remove_stop_words = config['remove_stop_words']
            assert remove_stop_words == None or remove_stop_words == "soft" or remove_stop_words == "hard", "`remove_stop_words` should be either `soft` or `hard` or `None`"

        assert 'key_terms_from_models' in self.__config, '`key_terms_from_models` configuration must be provided'
        assert self.__config['key_terms_from_models']['verbose'] is not None, 'You must provide the verbosity level for key_terms_from_models'
        assert self.__config['key_terms_from_models']['models'] is not None, 'You must provide the models for key_terms_from_models'
        models = self.__config['key_terms_from_models']['models'].split(',')
        for model in models:
            assert model == 'spacy' or model == 'rake' or model == 'textrank' or model == 'count' or model == 'keybert' or model == 'yake', 'The models provided for key_terms_from models are not valid'
        assert 'spacy' in self.__config['key_terms_from_models'], '`key_terms_from_models.spacy` configuration must be provided'
        assert 'ratio' in self.__config['key_terms_from_models'][
            'spacy'], '`key_terms_from_models.spacy.ratio` configuration must be provided'
        assert 'rake' in self.__config['key_terms_from_models'], '`key_terms_from_models.rake` configuration must be provided'
        assert 'ratio' in self.__config['key_terms_from_models'][
            'rake'], '`key_terms_from_models.rake.ratio` configuration must be provided'
        assert 'textrank' in self.__config['key_terms_from_models'], '`key_terms_from_models.textrank` configuration must be provided'
        assert 'ratio' in self.__config['key_terms_from_models'][
            'textrank'], '`key_terms_from_models.textrank.ratio` configuration must be provided'
        assert 'count' in self.__config['key_terms_from_models'], '`key_terms_from_models.count` configuration must be provided'
        assert 'ratio' in self.__config['key_terms_from_models'][
            'count'], '`key_terms_from_models.count.ratio` configuration must be provided'
        assert 'keybert' in self.__config['key_terms_from_models'], '`key_terms_from_models.keybert` configuration must be provided'
        assert isinstance(self.__config['key_terms_from_models']['keybert'],
                          list), '`key_terms_from_models.keybert` must be a list'
        for config in self.__config['key_terms_from_models']['keybert']:
            assert 'num_terms' in config, '`key_terms_from_models.keybert.num_terms` configuration must be provided'
            assert 'use_maxsum' in config, '`key_terms_from_models.keybert.use_maxsum` configuration must be provided'
            assert 'nr_candidates' in config, '`key_terms_from_models.keybert.nr_candidates` configuration must be provided'
            assert 'use_mmr' in config, '`key_terms_from_models.keybert.use_mmr` configuration must be provided'
            assert 'diversity' in config, '`key_terms_from_models.keybert.diversity` configuration must be provided'
        assert 'yake' in self.__config['key_terms_from_models'], '`key_terms_from_models.yake` configuration must be provided'
        assert 'num_terms' in self.__config['key_terms_from_models'][
            'yake'], '`key_terms_from_models.yake.num_terms` configuration must be provided'

        assert 'special_characters' in self.__config, '`special_characters` configuration must be provided'

        assert 'filter_terms' in self.__config, '`filter_terms` configuration must be provided'
        assert 'criteria' in self.__config['filter_terms'], '`filter_terms.criteria` configuration must be provided'
        criteria = self.__config['filter_terms']['criteria']
        assert criteria == "excluded" or criteria == "included", "`criteria` must be either 'included' or 'excluded'"
        assert 'pos_tagging_groups' in self.__config[
            'filter_terms'], '`filter_terms.pos_tagging_groups` configuration must be provided'
        assert 'included_pos_tagging' in self.__config[
            'filter_terms'], '`filter_terms.included_pos_tagging` configuration must be provided'
        assert 'excluded_pos_tagging' in self.__config[
            'filter_terms'], '`filter_terms.excluded_pos_tagging` configuration must be provided'

        assert 'similarity' in self.__config, '`similarity` configuration must be provided'
        assert 'remove_stop_words' in self.__config[
            'similarity'], '`remove_stop_words` configuration for `similarity` must be provided'
        assert 'metric' in self.__config['similarity'], '`metric` configuration for `similarity` must be provided'
        metric = self.__config['similarity']['metric']
        assert metric == 'spacy' or metric == 'transformers' or metric == 'tfhub', "The 'metric' must be 'spacy' or 'transformers' or 'tfhub'"

        assert 'thesaurus_similarity_threshold' in self.__config, '`thesaurus_similarity_threshold` configuration must be provided'
        threshold = self.__config['thesaurus_similarity_threshold']
        assert threshold >= 0 and threshold <= 1, "`thesaurus_similarity_threshold` must be between 0 and 1."

    def __get_terms(self, text, terms_size=1, use_sentences=False):
        """
        Returns a list of dictionaries with the most important terms in the given text
        and their TF-iDF ratio: {'term': term, 'tf-idf': tfidf}
        terms_size determines size of the terms. 
        The list of words returned is ordered by importance ratio.
        If use_sentences is True, the text should be a list of sentences instead
        """
        vectorizer_input = text if use_sentences else [text]
        vectorizer = TfidfVectorizer(
            lowercase=True, ngram_range=(terms_size, terms_size))
        X = vectorizer.fit_transform(vectorizer_input)

        df = pd.DataFrame(
            X.toarray(), columns=vectorizer.get_feature_names_out())

        most_relevant_terms_df = df.sort_values(by=0, axis=1, ascending=False)
        # MIND: Changed the approach
        most_relevant_terms_tuples = [{'term': term, 'tf-idf': np.mean(tfidf) if use_sentences else float(
            tfidf)} for (term, tfidf) in most_relevant_terms_df.iteritems()]

        return most_relevant_terms_tuples

    def __get_unique_terms_from_list(self, l):
        """
        Returns a list with the unique elements of the given list.
        Unlike when using `list(set(l))`, the order of the elements
        is kept.
        """
        res = []
        for element in l:
            if element not in res:
                res.append(element)
        return res

    def __get_term_relevance_in_text(self, doc, term, is_single_word=False):
        """
        Returns the relevance of the given term in the text
        of the given doc.
        text_doc must be a SpaCy document of the text to analyze.
        """
        term_doc = self.__spacy_nlp(term)
        if is_single_word:
            term_doc = term_doc[0]
        return doc.similarity(term_doc)

    def __is_term_stop_word(self, term, criteria="soft"):
        """
        Returns whether the given term is considered to be a stop words.
        If the criteria is 'soft', then all the words in the terms must be 
        stop words for the term to be considered a stop word. If the criteria
        is 'hard', then the terms must contain only one stop word to be considered
        a stop word.
        """
        # Load configuration.
        stop_words = self.__config['key_terms']['stop_words']

        words = term.split(' ')
        if criteria == "soft":
            return all(word in stop_words for word in words)
        if criteria == "hard":
            return any(word in stop_words for word in words)
        return None

    def __get_most_relevant_terms(self, terms, ratio, criteria, remove_stop_words):
        """
        Receives a list of terms that must be ordered by relevance
        and returns a list with the most important terms.
        The ratio defines the percentage of the terms to keep.
        This method uses TFiDF. This means that the words
        with the highest TFiDF value are considered the most important.
        If `remove_stop_words` is True, then the stop words will be removed.
        """
        if remove_stop_words is not None:
            terms = [term for term in terms if not self.__is_term_stop_word(
                term['term'], criteria=remove_stop_words)]

        res = []
        for term in terms:
            metrics = []
            if criteria == 'tf-idf' or criteria == 'both':
                metrics.append(term['tf-idf'])
            if criteria == 'text-relevance' or criteria == 'both':
                metrics.append(term['text-relevance'])
            relevance = np.mean(metrics)
            res.append({'term': term['term'], 'relevance': relevance})

        res.sort(key=lambda x: -x['relevance'])
        index = int(len(res)*ratio)
        return res[:index]

    def __get_two_word_terms(self, doc):
        """
        Returns a list of two-words terms using the given Stanza's
        pipeline.
        """
        terms = []
        for sent in doc.sentences:
            for dep in sent.dependencies:
                if dep[1] == 'amod':
                    terms.append(f'{dep[0].text} {dep[2].text}')
        return terms

    def __get_key_terms_spacy(self, text, doc):
        """
        Returns the key terms in the text according to the given Spacy doc.
        https://spacy.io/api/doc
        """
        # Load config.
        ratio = self.__config['key_terms_from_models']['spacy']['ratio']

        terms = []
        pos_tag = ['PROPN', 'ADJ', 'NOUN']
        for token in doc:
            if (token.text in self.__spacy_nlp.Defaults.stop_words or token.text in punctuation):
                continue
            if (token.pos_ in pos_tag):
                terms.append(token.text)

        index = int(len(terms)*ratio)
        key_terms = Counter(terms).most_common(index)
        return [entry[0] for entry in key_terms]

    def __get_key_terms_rake(self, text):
        """
        Returns the key terms in the given text according to Rake.
        https://pypi.org/project/rake-nltk/
        """
        # Load config.
        ratio = self.__config['key_terms_from_models']['rake']['ratio']

        r = Rake(language='spanish')
        r.extract_keywords_from_text(text)

        keywords = r.get_ranked_phrases()

        index = int(len(keywords)*ratio)
        return keywords[:index]

    def __get_key_terms_textrank(self, text):
        """
        Returns a list with the key terms of the given text according to textrank.
        https://pypi.org/project/pytextrank/
        """
        # Load config.
        ratio = self.__config['key_terms_from_models']['textrank']['ratio']

        # Add PyTextRank to the spaCy pipeline
        self.__spacy_nlp.add_pipe("textrank")
        doc = self.__spacy_nlp(text.lower())

        index = int(len(doc._.phrases)*ratio)
        res = [entry.text for entry in doc._.phrases[:index]]

        # Remove PyTextRank from the spaCy pipeline
        self.__spacy_nlp.remove_pipe("textrank")
        return res

    def __get_key_terms_count(self, text):
        """
        Returns a list of the most repeated words in the given text.
        """
        # Load config.
        ratio = self.__config['key_terms_from_models']['count']['ratio']

        filtered_words = [
            word for word in text.split() if word not in SPANISH_STOP_WORDS]
        counted_words = Counter(filtered_words)
        index = int(len(counted_words)*ratio)
        most_common_terms = counted_words.most_common(index)
        return [entry[0] for entry in most_common_terms]

    def __get_key_words_keybert(self,
                                text,
                                min_keyphrase_ngram_range=1,
                                max_keyphrase_ngram_range=3,
                                num_terms=150,
                                use_maxsum=False,
                                nr_candidates=20,
                                use_mmr=False,
                                diversity=0.5):
        """
        Returns a list of the key terms according to keyBERT model.
        https://pypi.org/project/keybert/
        """

        kw_model = KeyBERT()
        keywords = kw_model.extract_keywords(text,
                                             keyphrase_ngram_range=(min_keyphrase_ngram_range,
                                                                    max_keyphrase_ngram_range),
                                             top_n=num_terms,
                                             use_maxsum=use_maxsum,
                                             nr_candidates=nr_candidates,
                                             use_mmr=use_mmr,
                                             diversity=diversity)
        return [entry[0] for entry in keywords]

    def __get_key_terms_yake(self, text, max_term_size=3):
        """
        Returns a list of the key terms according to Yake's model.
        https://pypi.org/project/yake/
        """
        # Load config.
        num_terms = self.__config['key_terms_from_models']['yake']['num_terms']

        kw_extractor = yake.KeywordExtractor(
            lan='es', n=max_term_size, top=num_terms)
        keywords = kw_extractor.extract_keywords(text.lower())
        return [entry[0] for entry in keywords]

    def __get_key_terms_using_models(self, text, spacy_doc=None):
        """
        Returns a list of the most important terms in the given text according to the models
        in the configuration.
        """
        # Load the configuration.
        verbose = self.__config['key_terms_from_models']['verbose']
        models = self.__config['key_terms_from_models']['models'].split(',')

        key_terms = []
        if 'spacy' in models and spacy_doc is not None:
            key_terms_spacy = self.__get_key_terms_spacy(text, spacy_doc)
            if verbose:
                print(f'Added {len(key_terms_spacy)} - spacy')
            key_terms.extend(key_terms_spacy)
        if 'rake' in models:
            key_terms_rake = self.__get_key_terms_rake(text)
            if verbose:
                print(f'Added {len(key_terms_rake)} - rake')
            key_terms.extend(key_terms_rake)
        if 'textrank' in models:
            key_terms_textrank = self.__get_key_terms_textrank(text)
            if verbose:
                print(f'Added {len(key_terms_textrank)} - textrank')
            key_terms.extend(key_terms_textrank)
        if 'count' in models:
            key_terms_count = self.__get_key_terms_count(text)
            if verbose:
                print(f'Added {len(key_terms_count)} - count')
            key_terms.extend(key_terms_count)
        if 'keybert' in models:
            # Load the configuration.
            configs = self.__config['key_terms_from_models']['keybert']
            key_terms_keybert = []
            for config in configs:
                terms = self.__get_key_words_keybert(text, num_terms=config['num_terms'], use_maxsum=config['use_maxsum'],
                                                     nr_candidates=config['nr_candidates'], use_mmr=config['use_mmr'], diversity=config['diversity'])
                key_terms_keybert.extend(terms)
            if verbose:
                print(f'Added {len(key_terms_keybert)} - keybert')
            key_terms.extend(key_terms_keybert)
        if 'yake' in models:
            key_terms_yake = self.__get_key_terms_yake(text, max_term_size=3)
            if verbose:
                print(f'Added {len(key_terms_yake)} - yake')
            key_terms.extend(key_terms_yake)

        key_terms = self.__get_unique_terms_from_list(key_terms)
        if verbose:
            print(f'Total: {len(key_terms)}')
        return key_terms

    def __token_contains_special_character(self, token):
        """Returns in the token contains a special character or not."""
        # Load the config.
        special_characters = self.__config['special_characters']

        for special_character in special_characters:
            if search(special_character, token):
                return True
        return False

    def __remove_special_characters(self, tokens):
        """Removes the terms that contain special characters"""
        return [token for token in tokens if not self.__token_contains_special_character(token)]

    def __pos_tag_terms(self, terms):
        """
        Receives a list of terms and a Spacy nlp, and returns the
        pos-tagging of the given list of terms.
        The format of the returned dictionary is:
        {
            'term': {
                'pos': [<pos-tagging>]
            }
        }
        """
        res = {}
        for term in terms:
            doc = self.__spacy_nlp(term)
            pos = [token.pos_ for token in doc]
            res[term] = pos

        return res

    def __get_group_of_pos_tag(self, pos_tag):
        """
        Using the tagging groups in the configuration, returns the group of the given tag.
        """
        # Load configuration.
        pos_tagging_groups = self.__config['filter_terms']['pos_tagging_groups']

        for key, tags in pos_tagging_groups.items():
            if pos_tag in tags:
                return key
        return None

    def __are_groups_equivalent(self, group_1, group_2):
        """Returns if two groups of terms are equivalent. The key '*' is considered to match every pattern."""
        if len(group_1) != len(group_2):
            return False

        for index, element_1 in enumerate(group_1):
            element_2 = group_2[index]
            if element_1 != element_2 and element_1 != "*" and element_2 != "*":
                return False
        return True

    def __is_group_included(self, pos_group):
        """Returns if the given pos group is included in the included_pos_tagging"""
        # Load configuration.
        pos_tagging_to_include = self.__config['filter_terms']['included_pos_tagging']

        for included_group in pos_tagging_to_include:
            if self.__are_groups_equivalent(included_group, pos_group):
                return True
        return False

    def __is_group_excluded(self, pos_group):
        """Returns if the given pos group is included in the excluded_pos_tagging"""
        # Load configuration.
        pos_tagging_to_exclude = self.__config['filter_terms']['excluded_pos_tagging']

        for excluded_group in pos_tagging_to_exclude:
            if are_groups_equivalent(excluded_group, pos_group):
                return True
        return False

    def __filter_terms(self, pos_tagging):
        """Filters the terms that do not match the valid patterns"""
        # Load the configuration.
        criteria = self.__config['filter_terms']['criteria']

        is_valid = (lambda x: not self.__is_group_excluded(
            x)) if criteria == "excluded" else (lambda x: self.__is_group_included(x))

        res = []
        for term, pos in pos_tagging.items():
            pos_group = [self.__get_group_of_pos_tag(tag) for tag in pos]
            if is_valid(pos_group):
                res.append(term)
        return res

    def __remove_stop_words_from_text(self, text):
        """Removes the stop words from the given text."""
        doc = self.__spacy_nlp(text)
        filtered_tokens = [token for token in doc if not token.is_stop]
        return ' '.join([token.text for token in filtered_tokens])

    def __get_tokens_similarity(self, nlp, token_1, token_2):
        """Returns the similarity between the given tokens according to the provided Spacy nlp."""
        remove_stop_words = self.__config['similarity']['remove_stop_words']
        metric = self.__config['similarity']['metric']

        if remove_stop_words:
            token_1 = self.__remove_stop_words_from_text(token_1)
            token_2 = self.__remove_stop_words_from_text(token_2)

        if metric == 'spacy':
            doc_1 = nlp(token_1)
            doc_2 = nlp(token_2)
            return doc_1.similarity(doc_2)

        if metric == 'transformers':
            model = SentenceTransformer('distilbert-base-nli-mean-tokens')
            sentence_embeddings = model.encode([token_1, token_2])
            res = util.pytorch_cos_sim(
                sentence_embeddings[0], sentence_embeddings[1])
            return float(res.numpy()[0][0])

        if metric == 'tfhub':
            model = hub.load(
                "https://tfhub.dev/google/universal-sentence-encoder/4")
            sentence_embeddings = model([token_1, token_2])
            res = util.pytorch_cos_sim(sentence_embeddings.numpy()[
                                       0], sentence_embeddings.numpy()[1])
            return res.numpy()[0][0]

        return None

    def __get_token_pairs_similarities(self, tokens):
        """
        Returns a structure containing information about the similarity of
        the tokens given.

        The returning array's elements have the following format:
        {
            "token_1": <token_1>,
            "token_2": <token_2>,
            "similarity": <similarity>
        }

        It sorts the entries by similarity before returning them.
        """
        nlp = es_core_news_lg.load()

        res = []
        already_analyzed_tokens = []
        for token_1 in tokens:
            for token_2 in tokens:
                if token_1 != token_2:
                    entry = _TokenPair(token_1, token_2)
                    if entry not in already_analyzed_tokens:
                        similarity = self.__get_tokens_similarity(
                            nlp, token_1, token_2)
                        res.append(
                            {"token_1": token_1, "token_2": token_2, "similarity": similarity})
                        already_analyzed_tokens.append(entry)
        res.sort(key=lambda element: element["similarity"], reverse=True)
        return res

    def __filter_thesaurus_by_threshold(self, thesaurus):
        """
        Receives a thesaurus and returns another one with only similarities
        greater or equal to the given threshold.
        """
        # Load the configuration.
        threshold = self.__config['thesaurus_similarity_threshold']

        return [entry for entry in thesaurus if entry["similarity"] >= threshold]

    def generate(self, path):
        """Generates a thesaurus of the text in the given path and returns it."""
        # Verbose
        v = logging.info if self.__config['verbose'] else lambda x: None

        # Load the text of the path.
        text = pathlib.Path(path).read_text(encoding="utf-8")
        v('Text loaded.')

        # Load the docs.
        if self.__spacy_nlp is not None:
            spacy_doc = self.__spacy_nlp(text.lower())
        if self.__stanza_nlp is not None:
            stanza_doc = self.__stanza_nlp(text.lower())
        v('Models loaded.')

        # Get the key terms with one word.
        one_word_terms = self.__get_terms(text, terms_size=1)
        one_word_terms = self.__get_unique_terms_from_list(one_word_terms)
        one_word_terms = [
            {
                'term': entry['term'],
                'tf-idf': entry['tf-idf'],
                'text-relevance': self.__get_term_relevance_in_text(spacy_doc, entry['term'], is_single_word=True)
            } for entry in one_word_terms
        ]
        most_relevant_one_word_terms = self.__get_most_relevant_terms(
            one_word_terms, self.__config['key_terms']['config'][0]['ratio'], self.__config['key_terms']['config'][0]['criteria'], self.__config['key_terms']['config'][0]['remove_stop_words'])
        v('Extracted key terms with one word.')

        # Get the key terms with two words.
        all_two_word_terms = self.__get_terms(text, terms_size=2)
        all_two_word_terms = self.__get_unique_terms_from_list(
            all_two_word_terms)
        all_two_word_terms = [
            {
                'term': entry['term'],
                'text-relevance': self.__get_term_relevance_in_text(spacy_doc, entry['term'])
            } for entry in all_two_word_terms
        ]
        most_relevant_all_two_word_terms = self.__get_most_relevant_terms(
            all_two_word_terms, self.__config['key_terms']['config'][1]['ratio'], self.__config['key_terms']['config'][1]['criteria'], self.__config['key_terms']['config'][1]['remove_stop_words'])
        amod_two_words_terms = self.__get_two_word_terms(stanza_doc)
        amod_two_words_terms = self.__get_unique_terms_from_list(
            amod_two_words_terms)
        most_relevant_amod_two_word_terms = amod_two_words_terms
        most_relevant_two_word_terms = [
            entry['term'] for entry in most_relevant_all_two_word_terms] + most_relevant_amod_two_word_terms
        most_relevant_two_word_terms = self.__get_unique_terms_from_list(
            most_relevant_two_word_terms)
        v('Extracted key terms with two words.')

        # Get the key terms with three words.
        three_words_terms = self.__get_terms(text, terms_size=3)
        three_words_terms = self.__get_unique_terms_from_list(
            three_words_terms)
        three_words_terms = [
            {
                'term': entry['term'],
                'tf-idf': entry['tf-idf'],
                'text-relevance': self.__get_term_relevance_in_text(spacy_doc, entry['term'])
            } for entry in three_words_terms
        ]
        most_relevant_three_word_terms = self.__get_most_relevant_terms(
            three_words_terms, self.__config['key_terms']['config'][2]['ratio'], self.__config['key_terms']['config'][2]['criteria'], self.__config['key_terms']['config'][2]['remove_stop_words'])
        v('Extracted key terms with three words.')

        # Get the key terms from the models.
        models_key_terms = self.__get_key_terms_using_models(text)
        v('Extracted key terms from models.')

        # Get the most relevant terms.
        most_relevant_terms = [term['term'] for term in most_relevant_one_word_terms] + most_relevant_two_word_terms + [
            term['term'] for term in most_relevant_three_word_terms] + models_key_terms
        most_relevant_terms = self.__get_unique_terms_from_list(
            most_relevant_terms)
        v('Defined most relevant terms.')

        # Remove the special characters from the terms.
        terms_no_special_characters = self.__remove_special_characters(
            most_relevant_terms)
        self.terms = terms_no_special_characters
        v('Defined terms to be analysed and saved in the `terms` attribute.')

        # Filter the terms.
        pos_tagging = self.__pos_tag_terms(terms_no_special_characters)
        filtered_terms = self.__filter_terms(pos_tagging)
        self.filtered_terms = filtered_terms
        v('Filtered terms and saved in the `filtered_terms` attribute.')

        # Get the similarities between the terms.
        token_pairs_similarities = self.__get_token_pairs_similarities(
            filtered_terms)
        self.token_pairs_similarities = token_pairs_similarities
        v('Obtained similarities between terms and saved in the `token_pairs_similarities` attribute.')

        # Generate the thesaurus.
        thesaurus = self.__filter_thesaurus_by_threshold(
            token_pairs_similarities)
        self.thesaurus = thesaurus
        v('Generated thesaurus and saved in the `thesaurus` attribute.')

        return thesaurus

    def __normalize_thesaurus(self, thesaurus):
        """Formats the given thesaurus by removing its accents."""
        tilde, no_tilde = 'áéíóúü', 'aeiouu'
        trans = str.maketrans(tilde, no_tilde)
        res = []
        for entry in thesaurus:
            token_1 = entry['token_1'].translate(trans)
            token_2 = entry['token_2'].translate(trans)
            res.append({
                'token_1': token_1,
                'token_2': token_2,
                'similarity': entry['similarity'],
            })
        return res

    def save_thesaurus(self, path, ensure_ascii=True, normalize=True):
        """Saves the given generated thesaurus in a JSON format in the given path."""
        assert hasattr(
            self, 'thesaurus'), 'the thesaurus must be already generated. Try calling `generate` before'

        data = self.__normalize_thesaurus(
            self.thesaurus) if normalize else self.thesaurus
        with open(path, 'w') as file:
            json.dump(data, file, ensure_ascii=ensure_ascii)
            file.close()


if __name__ == "__main__":
    t = ThesaurusGenerator()
    thesaurus = t.generate('./topics/topic_2.txt')
    t.save_thesaurus('thesaurus.json')
