// Used to clean, deduplicate custom built lexicons for virus, vaccine and death.

const lexicon_virus = `
administration test
antibiotique
aplatir courbe
asymptomatique
auto-immun
auto-isolement
bactérie
cas actif
cas confirmé
cas confirmer
cas contact
charge viral
clinique de dépistage
confinement
confiné
contamination
contaminer
coronavirus
couvre-feu
covid-19
distanciation social
déconfinement
déconfiner
déconfiné
déficit immunitaire
dépistage
dépister
désinfectant
désinfecter
epidémie
epidémiologie
faux négatif
faux positif
fermeture frontière
fièvre
foyer infection
germe
germes
geste barrière
hospitalisation
immunisation
immuniser
immunité
immunodéprimé
infecter
infection
insuffisance respiratoire
isolement
isoler
lits soins intensifs
masque
mesure sanitaires
mutation
muter
nasal
oms
pandémie
pandémique
pathogène
patient zéro
pneumonie
quarantaine
réanimation
symptôme
taux de mortalité
test antigénique
transmission
viral
virologie
virus
vulnérable
écraser courbe
épidémie
laver main
restriction
`;

const lexicon_death = `
agonie
cadavre
caveau
cendres
cercueil
cimetière
commémoration
condoléances
crypte
crématoire
crématorium
cénotaphe
deuil
disparaître
disparition
décimer
décès
décéder
défunt
dépouille
ensevelir
ensevelissement
enterrement
enterrer
extinction
exécution
fatal
fossoyeur
funeste
funèbre
funérailles
funéraire
génocide
homicide
hôpital
incinération
incinérer
inerte
inhumation
lugubre
maladie
martyre
meurtre
mort
mortel
mourant
mourir
obsèques
pierre tombale
périr
avoir quitter
ressusciter
résurrection
succomber
sépulture
s’éteindre
tombe
tombeau
trépas
trépasser
tuer
victime
âme
épitaphe
éteindre`;

const lexicon_vaccine = `
adjuvant
administrer
anticorps
antigène
antiviral
immunisation
immuniser
immunité
immunoglobine
injection
pathogène
vaccin
vaccinal
vaccination
vacciner
virologue
dose
astrazeneca
pfizer
moderna
janssen
vaxzevria
johnson&johnson
curevac
spoutnik v
biontech
sanofi
arn`;

function clean_and_deduplicate(data) {
    const arr = data.toLowerCase().split('\n').filter(d => !!d).map(d => d.trim());
    const dedup = [...new Set(arr)].sort();
    return dedup.join('\n');
}

const virus = clean_and_deduplicate(lexicon_virus)
const vaccine = clean_and_deduplicate(lexicon_vaccine)
const death = clean_and_deduplicate(lexicon_death)

// Output these to files using CLI piping >
// console.log(virus)
// console.log(vaccine)
console.log(death)