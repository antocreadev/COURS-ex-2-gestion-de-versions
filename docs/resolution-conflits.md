# Résoudre un conflit de merge

Un conflit n'est **pas une erreur**. C'est Git qui dit : « deux personnes ont
modifié les mêmes lignes, je ne peux pas décider à votre place ».

---

## Quand cela arrive

```
        ┌──● C  (main : un collègue a modifié stats.py ligne 42)
main ───┤
        └──● D  (votre branche : vous avez modifié stats.py ligne 42)
```

```bash
git switch ma-branche
git merge main
```

```
Auto-merging src/tpgit/stats.py
CONFLICT (content): Merge conflict in src/tpgit/stats.py
Automatic merge failed; fix conflicts and then commit the result.
```

---

## La marche à suivre

### 1. Voir l'ampleur des dégâts

```bash
git status
```

```
Unmerged paths:
  both modified:   src/tpgit/stats.py
```

Seuls les fichiers listés sous *Unmerged paths* sont à traiter.

### 2. Ouvrir le fichier

```python
def ecart_type(valeurs: Sequence[float]) -> float:
<<<<<<< HEAD
    # votre version (la branche sur laquelle vous êtes)
    centre = sum(valeurs) / len(valeurs)
=======
    # la version qui arrive (main)
    centre = moyenne(valeurs)
>>>>>>> main
```

| Marqueur | Signification |
|---|---|
| `<<<<<<< HEAD` | début de **votre** version |
| `=======` | séparateur |
| `>>>>>>> main` | fin de la version **entrante** |

### 3. Décider

Quatre issues possibles, et **c'est à vous de choisir** :

1. garder votre version ;
2. garder celle de `main` ;
3. **garder les deux** (fréquent : deux fonctions différentes ajoutées au même
   endroit) ;
4. écrire une troisième version qui combine les deux intentions.

Le piège classique est de choisir mécaniquement « la mienne ». Demandez-vous
*pourquoi* l'autre version existe : elle corrige peut-être un bug que vous
réintroduisez.

### 4. Nettoyer

Le fichier final ne doit contenir **aucun** marqueur. Le hook
`check-merge-conflict` vous arrêtera si vous en oubliez un, mais relisez quand
même.

### 5. Valider

```bash
git add src/tpgit/stats.py
git status                 # plus rien sous "Unmerged paths" ?
make check                 # ⭐ le code fusionné fonctionne-t-il vraiment ?
git merge --continue
git push
```

> **L'étape `make check` n'est pas optionnelle.** Un fichier sans marqueur peut
> être parfaitement incohérent : Git fusionne du texte, pas du sens.

---

## En cas de panique

```bash
git merge --abort      # annule le merge, retour à l'état d'avant
git rebase --abort     # équivalent pendant un rebase
```

Vous ne perdez rien. Recommencez au calme.

---

## Outils

```bash
git diff --name-only --diff-filter=U    # lister les fichiers en conflit
git checkout --ours  fichier.py         # prendre votre version en entier
git checkout --theirs fichier.py        # prendre la version entrante en entier
git mergetool                           # ouvrir un outil graphique de fusion
```

> Attention : pendant un **rebase**, `--ours` et `--theirs` sont inversés par
> rapport au merge (le rebase rejoue vos commits *sur* l'autre branche). En cas
> de doute, éditez le fichier à la main.

VS Code affiche des boutons *Accept Current / Accept Incoming / Accept Both*
directement dans le fichier : c'est le plus simple pour démarrer.

---

## Comment en avoir moins

| Pratique | Effet |
|---|---|
| Des branches **courtes** (1 à 3 jours) | moins de divergence accumulée |
| Des PR **petites** | moins de lignes en collision |
| `git merge main` **régulièrement** dans votre branche | des conflits petits et fréquents plutôt qu'un gros à la fin |
| Se répartir les fichiers en début de séance | évite les collisions frontales |
| Ne pas reformater du code non concerné par votre PR | évite les conflits artificiels |

Un conflit est proportionnel au temps pendant lequel deux branches ont vécu
séparément. C'est l'argument central de l'intégration *continue*.
