from .regex_helpers import compile_regex_from_lexicon
import string

punctuation = r'«»‹›' + string.punctuation


class SpecialisedLexicons():
    def __init__(self, death, virus, vaccine):
        self.death = death
        self.virus = virus
        self.vaccine = vaccine

        self.death_regexp = compile_regex_from_lexicon(death)
        self.vaccine_regexp = compile_regex_from_lexicon(vaccine)
        self.virus_regexp = compile_regex_from_lexicon(virus)

    def to_dict(self):
        return {
            'lexicons': {
                'death': self.death,
                'vaccine': self.vaccine,
                'virus': self.virus
            },
            'regexp': {
                'death': self.death_regexp.pattern,
                'vaccine': self.vaccine_regexp.pattern,
                'virus': self.virus_regexp.pattern
            }
        }


def map_polarity_to_int(polarimots_polarity):
    if polarimots_polarity == 'POS':
        return 1
    if polarimots_polarity == 'NEG':
        return -1
    return 0


class DikoItem():
    def __init__(self, word, positif, neutral, negative):
        self.word = word.strip('"')
        self.positif = int(positif)
        self.neutral = int(neutral)
        self.negative = int(negative)
        self.weight = None

    def get_vote_count(self):
        return self.positif + self.negative + self.neutral

    def get_vote_count_no_neutral(self):
        return self.positif + self.neutral

    def compute_score(self, variation):
        total = self.get_vote_count()
        # Z-Score without normalisation
        self.weight = (total/variation) * \
            ((self.positif - self.negative) / total)

    def to_dict(self):
        return {
            'word': self.word,
            'positif': self.positif,
            'neutral': self.neutral,
            'negative': self.negative,
            'weight': self.weight
        }


class PolarimotsItem():
    def __init__(self, id, word, word_type, polarity, reliability):
        self.id = int(id)
        self.word = word.strip('"')
        self.word_type = word_type.strip('"')
        self.polarity = map_polarity_to_int(polarity.strip('"'))
        self.reliability = float(reliability.strip('"%').replace(',', '.'))

        if self.reliability == 100:
            self.reliability = 1

    def to_dict(self):
        return {
            'id': self.id,
            'word': self.word,
            'word_type': self.word_type,
            'polarity': self.polarity,
            'reliability': self.reliability,
        }


# Actual Lexicon Model
class FEELLexiconItem():
    def __init__(self, id, word, polarity, joy, fear, sadness, anger, surprise, disgust):
        self.id = int(id)
        self.word = word
        self.polarity = polarity
        self.joy = int(joy)
        self.fear = int(fear)
        self.sadness = int(sadness)
        self.anger = int(anger)
        self.surprise = int(surprise)
        self.disgust = int(disgust)

    def to_dict(self):
        return {
            'id': self.id,
            'word': self.word,
            'polarity': self.polarity,
            'joy': self.joy,
            'fear': self.fear,
            'sadness': self.sadness,
            'anger': self.anger,
            'surprise': self.surprise,
            'disgust': self.disgust
        }


# Enums for FEEL
class LexiconModel():
    def __init__(self, index, name):
        self.index = index
        self.name = name


class FEELModel():
    id = LexiconModel(name='id', index=0)
    word = LexiconModel(name='word', index=1)
    polarity = LexiconModel(name='polarity', index=2)
    joy = LexiconModel(name='joy', index=3)
    fear = LexiconModel(name='fear', index=4)
    sadness = LexiconModel(name='sadness', index=5)
    anger = LexiconModel(name='anger', index=6)
    surprise = LexiconModel(name='surprise', index=7)
    disgust = LexiconModel(name='disgust', index=8)


# Model used to load data from the FR Gov Synthese dataset
class GouvSyntheseModel():
    casConfirmes = 'casConfirmes'
    deces = 'deces'
    decesEhpad = 'decesEhpad'
    reanimation = 'reanimation'
    hospitalises = 'hospitalises'
    gueris = 'gueris'
    date = 'date'
    nouvellesHospitalisations = 'nouvellesHospitalisations'
    nouvellesReanimations = 'nouvellesReanimations'
    nouvellesPremieresInjections = 'nouvellesPremieresInjections'
    cumulPremieresInjections = 'cumulPremieresInjections'
    stockNombreTotalDoses = 'stockNombreTotalDoses'
    stockNombreDosesPfizer = 'stockNombreDosesPfizer'
    stockNombreDosesModerna = 'stockNombreDosesModerna'
    livraisonsCumulNombreTotalDoses = 'livraisonsCumulNombreTotalDoses'
    livraisonsCumulNombreDosesPfizer = 'livraisonsCumulNombreDosesPfizer'
    livraisonsCumulNombreDosesModerna = 'livraisonsCumulNombreDosesModerna'
    totalPrisesRendezVousSemaine = 'totalPrisesRendezVousSemaine'
    prisesRendezVousSemaineRang1 = 'prisesRendezVousSemaineRang1'
    prisesRendezVousSemaineRang2 = 'prisesRendezVousSemaineRang2'
    stockEhpadNombreDosesPfizer = 'stockEhpadNombreDosesPfizer'
    # The data below  was deprecated
    testsRealises = 'testsRealises'
    testsPositifs = 'testsPositifs'
