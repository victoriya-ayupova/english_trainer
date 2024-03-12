import logging

from loguru import logger
import spacy

logger.add('app.log', level=logging.DEBUG)

logger.debug('Before spacy.load')
nlp_en = spacy.load("en_core_web_sm")
logger.debug('After spacy.load')
