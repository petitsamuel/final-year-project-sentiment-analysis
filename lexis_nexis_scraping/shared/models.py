import string

punctuation = r'«»‹›' + string.punctuation

# Actual Lexicon Model
class FEELLexiconItem():
    def __init__(self, id, word, polarity, joy, fear, sadness, anger, surprise, disgust):
        self.id = id
        self.word = word  
        self.polarity = polarity  
        self.joy = joy  
        self.fear = fear  
        self.sadness = sadness  
        self.anger = anger  
        self.surprise = surprise  
        self.disgust = disgust  
    
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
    # The data below  was depreated
    testsRealises = 'testsRealises'
    testsPositifs = 'testsPositifs'
