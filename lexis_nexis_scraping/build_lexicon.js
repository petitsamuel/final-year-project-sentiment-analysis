// const lexicon = `asymptomatique
// isolement
// Covid-19
// Contamination
// contaminer
// Distanciation social
// Couvre-feu
// Confinement
// Écraser courbe
// épidémie
// Foyer infection
// Fermeture frontière
// Geste barrière
// Immunité collectif
// OMS
// Pandémie
// patient zéro
// Quarantaine
// Réanimation
// Transmission
// Télétravail
// Virus
// Virologie
// administration test
// anticorps
// antigène
// aplatir courbe
// auto-isolement
// vaccination
// vaccin
// cas confirmer
// cas actif
// cas contact
// charger viral
// clinique de dépistage
// confiné
// coronavirus
// masque
// déconfinement
// déconfiner
// dépistage
// dépister
// désinfectant pour main
// faux négatif
// faux positif
// fièvre
// symptôme
// foyer infection
// hospitalisation
// immunité collectif
// infecter
// infection
// insuffisance respiratoire
// lits soins intensifs
// mesurer sanitaires
// mutation
// muter
// pandémique
// pandémie
// pandémique
// vacciner
// vulnérable
// isoler
// taux de mortalité
// test antigénique
// transmission
// vaccinateur
// Virus
// Epidémie
// Pandémie
// Pathogène
// Epidémiologie
// Anticorps
// Antigène
// Antiviral
// Auto-immun
// Charge viral
// Déficit immunitaire
// Germe
// Germes
// Immunisation
// Immunité
// Immuniser
// Immunodéprimé
// Infection
// viral
// Pneumonie
// Antibiotique
// Bactérie
// ARN
// ADN
// contaminer
// `
const lexicon = `
Agonie
Disparition
Extinction
Décès
Trépas
Tombeau
Disparu
Victime
Dépouille
Défunt
Tombe
Sépulture 
Homicide
Tué
Décédé
Trépassé
Martyre 
Cadavre
Crypte
Cénotaphe
Cercueil
Fossoyeur
Lugubre
Mortel
Fatal
Funeste 
Funèbre 
Funéraire 
Funérailles 
Enterrement
Inhumation
Obsèques
Ensevelissement
Épitaphe
Deuil 
Condoléances 
Mourir 
mort
Décéder
Trépasser 
Périr
Disparaître 
Succomber 
S’éteindre 
Ensevelir 
Décimer 
Génocide
Cimetière  
cadavre
défunt
cadavre
résurrection
tombeau
cercueil
agonie
dépouille
deuil
décès
meurtre
ressusciter
exécution
tombe
funèbre
cimetière
mourir
décéder
mourant	
décédé	
mort	
décédée
défunt
qui nous a quitté
âme
décès
maladie
hôpital	
cercueil
cendres
incinérer
incinération
crématoire 
crématorium
enterrer
cimetière
tombe
tombeau
pierre	tombale
funérailles
obsèques
commémoration
deuil
condoléances
éteint
décédé
inerte
Incinération 
Caveau
Tombe 
obsèques`
let arr = lexicon.toLowerCase().split('\n').filter(d => !!d).map(d => d.trim());
let dedup = [...new Set(arr)].sort()
console.log(dedup.join('\n'))