# The Chess Manager

### programme permettant de géré des tournois d'echecs

#### version de python 3.10.2

### instalation
Pour créer l'environnement virtuel, placez-vous dans le dossier du projet, puis exécutez la commande suivante :
```
python -m venv env
```

Activé le ensuite en executant la commande suivante sous windows :
powershell :
```
env\Scripts\activate
```
Bash :
```
source env\Scripts\activate
```

Mac\Linux :
```
source env/bin/activate
```

Installer les dépendances :
```
pip install -r requirements.txt
```
### lancement
D
```
cd Source/
```
Vous pouvez maintenant lancer le programme :
```
python P2_WebScraping.py
```
### Verification avec flake8-html
Pour lancer la vérification, lancer la commande suivante :
```
flake8 --format=html --max-line-length=119 --htmldir=flake-report
```
Le rapport se trouvera dans le dossier flake-report