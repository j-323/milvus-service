from langdetect import detect, DetectorFactory
from textblob import TextBlob
import textstat
import spacy
from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel
from app.core.config import settings

DetectorFactory.seed = 0
nlp = spacy.load(settings.analysis.spacy_model)

def analyze_text(text: str) -> dict:
    lang = detect(text)

    tb = TextBlob(text)
    sentiment = {
        "polarity": tb.sentiment.polarity,
        "subjectivity": tb.sentiment.subjectivity
    }

    readability = {
        "flesch_reading_ease": textstat.flesch_reading_ease(text),
        "flesch_kincaid_grade": textstat.flesch_kincaid_grade(text)
    }

    doc = nlp(text)
    entities = [
        {"text": ent.text, "label": ent.label_, "start": ent.start_char, "end": ent.end_char}
        for ent in doc.ents
    ]

    tokens = [tok.lemma_ for tok in doc if tok.is_alpha and not tok.is_stop]
    dictionary = Dictionary([tokens])
    corpus = [dictionary.doc2bow(tokens)]
    lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=settings.analysis.num_topics)
    topics = [
        {"topic_id": tid, "terms": [t for t,_ in lda.show_topic(tid)], "score": p}
        for tid, p in lda[corpus[0]]
    ]

    word_count = len(tokens)
    unique_word_count = len(set(tokens))
    lexical_diversity = unique_word_count / word_count if word_count else 0

    return {
        "language": lang,
        "sentiment": sentiment,
        "readability": readability,
        "entities": entities,
        "topics": topics,
        "word_count": word_count,
        "unique_word_count": unique_word_count,
        "lexical_diversity": lexical_diversity
    }