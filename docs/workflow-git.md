# Le cycle de contribution, en détail

Ce document reprend le cycle du README étape par étape, avec les commandes, ce
qui se passe côté serveur, et les pièges classiques.

---

## Vue d'ensemble

```
   ┌──────────┐   ┌─────────┐   ┌──────────┐   ┌────┐   ┌───────┐   ┌───────┐
   │  Issue   │──▶│ Branche │──▶│ Commits  │──▶│ PR │──▶│  CI   │──▶│ Revue │
   └──────────┘   └─────────┘   └──────────┘   └────┘   └───────┘   └───────┘
                                      ▲                     │            │
                                      │                     ▼            ▼
                                      └──────────── corrections ◀────────┘
                                                            │
                                                            ▼
                                                   ┌────────────────┐
                                                   │ Merge + ménage │
                                                   └────────────────┘
```

Deux idées à retenir :

1. **`main` est toujours déployable.** On n'y écrit jamais directement ; tout
   passe par une branche et une PR.
2. **La boucle de correction est normale.** Une PR qui reçoit des commentaires
   n'est pas une PR ratée : c'est le mécanisme qui fonctionne.

---

## Étape 0 — Cloner et s'installer (une seule fois)

```bash
git clone https://github.com/antocreadev/COURS-ex-2-gestion-de-versions.git
cd COURS-ex-2-gestion-de-versions
make install
make hooks
make check        # doit être vert AVANT toute modification
```

Si `make check` est déjà rouge sur un dépôt fraîchement cloné, ne codez pas :
signalez-le. Vous ne pourrez pas distinguer vos erreurs de celles d'origine.

Configurez votre identité, elle apparaîtra dans chaque commit :

```bash
git config --global user.name "Prénom Nom"
git config --global user.email "prenom.nom@etu.univ.fr"
git config --global pull.ff only       # pull sans merge implicite
git config --global init.defaultBranch main
```

---

## Étape 1 — L'issue

L'issue répond à : *quel problème, pour qui, et comment saura-t-on que c'est
réglé ?*

```bash
gh issue list                       # voir ce qui est à faire
gh issue view 12                    # lire une issue
gh issue develop 12 --name feat/mediane --checkout   # créer la branche liée
```

La dernière commande est pratique : la branche est automatiquement rattachée à
l'issue, qui se fermera au merge de la PR.

---

## Étape 2 — La branche

```bash
git switch main
git pull --ff-only
git switch -c feat/calcul-mediane
```

**Pourquoi une branche ?** Parce qu'elle isole un travail en cours. Tant que la
branche n'est pas mergée, `main` reste utilisable par tout le monde, et vous
pouvez expérimenter, casser, recommencer.

```bash
git branch -vv       # où en suis-je ? quelle branche suit quoi ?
git switch -         # revenir à la branche précédente
```

---

## Étape 3 — Les commits

```bash
git status                  # réflexe n°1
git diff                    # ce qui n'est pas encore indexé
git add src/tpgit/stats.py tests/test_stats.py
git diff --staged           # ce qui partira dans le commit
git commit -m "feat(stats): ajoute le calcul de la médiane"
```

### Ce qui se passe au moment du `commit`

```
 git commit
     │
     ├─▶ hook pre-commit   : ruff format, ruff check --fix, mypy, hygiène des fichiers
     │        └─ si un fichier est MODIFIÉ par un hook → le commit est ANNULÉ
     │           (c'est voulu : relisez la correction, `git add`, puis recommencez)
     │
     ├─▶ hook commit-msg   : format du message
     │        └─ message non conforme → commit REFUSÉ
     │
     └─▶ le commit est créé
```

Un commit annulé par un hook ne perd rien : vos modifications sont intactes.

```bash
git add -u && git commit -m "feat(stats): ajoute le calcul de la médiane"
```

### Se rattraper

```bash
git commit --amend                    # corriger le dernier commit (message ou contenu)
git commit --amend --no-edit          # y ajouter des fichiers sans changer le message
git restore --staged fichier.py       # désindexer
git restore fichier.py                # annuler les modifications d'un fichier (destructif)
git reset --soft HEAD~1               # défaire le dernier commit, garder les modifications
```

> `--amend` réécrit l'historique. Tant que la branche n'est **pas encore
> poussée**, c'est sans risque. Après un push, cela oblige à un
> `git push --force-with-lease` — à éviter pendant une relecture.

---

## Étape 4 — Pousser

```bash
git push -u origin feat/calcul-mediane
```

Le hook `pre-push` lance la suite de tests. S'il refuse, c'est une CI rouge
évitée et quelques minutes gagnées.

```bash
git push --no-verify        # court-circuite le hook — à n'utiliser qu'en connaissance de cause
```

---

## Étape 5 — La Pull Request

```bash
gh pr create --fill --web
gh pr status                # état de mes PR
gh pr checks                # état de la CI
gh pr view --web
```

Une PR, ce n'est pas « du code à intégrer », c'est **une demande d'accord**. Le
diff est le support de la discussion ; la description en est l'argumentaire.

### Ce qui se déclenche automatiquement

| Déclencheur | Effet |
|---|---|
| Ouverture de la PR | workflows `CI` et `Pull Request` démarrent |
| Nouveau push sur la branche | la CI se relance, l'exécution précédente est annulée |
| Modification du titre / de la description | le workflow `Pull Request` se relance |
| Fichiers touchés | `CODEOWNERS` désigne les relecteurs |

---

## Étape 6 — La CI

Quatre jobs (voir [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)) :

| Job | Rôle |
|---|---|
| `Lint & types` | ruff check, ruff format, mypy — rapide, échoue tôt |
| `Tests (Python 3.11 / 3.12 / 3.13)` | pytest + couverture, en parallèle sur 3 versions |
| `pre-commit` | rejoue tous les hooks sur **tout** le dépôt |
| `CI OK` | agrège les précédents ; c'est **ce check** qui est requis pour merger |

**Pourquoi un job `CI OK` ?** Parce que la protection de branche exige des noms
de checks figés. Avec une matrice, les noms changent dès qu'on ajoute une
version de Python. Un job d'agrégation donne un point d'entrée stable.

**Pourquoi tester sur 3 versions ?** Parce que « ça marche sur ma machine » n'est
pas une garantie. La matrice rend explicite le contrat de compatibilité.

Lire un échec :

```bash
gh run list --branch feat/calcul-mediane
gh run view --log-failed          # ne montre que ce qui a échoué
```

---

## Étape 7 — La revue et les corrections

Vous recevez des commentaires. Vous corrigez **sur la même branche** :

```bash
# ... corrections ...
git commit -m "test(stats): couvre le cas de l'effectif pair"
git push
```

La PR se met à jour toute seule, la CI se relance, le relecteur voit uniquement
ce qui a changé depuis sa dernière lecture.

Si `main` a avancé pendant ce temps :

```bash
git switch main && git pull --ff-only
git switch feat/calcul-mediane
git merge main            # ou : git rebase main
```

→ conflits éventuels : voir [`resolution-conflits.md`](resolution-conflits.md).

**`merge` ou `rebase` ?**

|  | `git merge main` | `git rebase main` |
|---|---|---|
| Historique | conserve tout, ajoute un commit de merge | linéaire, rejoue vos commits au-dessus |
| Réécrit vos commits | non | oui |
| Pendant une relecture | ✅ recommandé | ❌ perturbe le relecteur |
| Sur une branche perso non poussée | ✅ | ✅ recommandé |

En cas de doute, dans ce TP : **`merge`**.

---

## Étape 8 — Le merge

Quand la CI est verte et la PR approuvée :

```bash
gh pr merge --squash --delete-branch
```

*Squash* : les N commits de la branche deviennent **un** commit sur `main`,
intitulé comme la PR. C'est pour cela que le titre de la PR est vérifié.

---

## Étape 9 — Le ménage

```bash
git switch main
git pull --ff-only
git branch -d feat/calcul-mediane     # refuse si la branche n'est pas mergée : c'est un garde-fou
git fetch --prune
```

Une liste de branches propre est un indicateur de santé du dépôt.

---

## Les pièges les plus fréquents

| Symptôme | Cause | Solution |
|---|---|---|
| `fatal: refusing to merge unrelated histories` | dépôt initialisé deux fois | repartir d'un clone propre |
| `Updates were rejected` au push | la branche distante a avancé | `git pull --rebase` puis repousser |
| Le commit est « annulé » sans erreur claire | un hook a reformaté un fichier | `git add -u` puis recommiter |
| CI rouge, local vert | version de Python différente | regarder quel job de la matrice échoue |
| `.venv/` apparaît dans `git status` | `.gitignore` ignoré car le fichier est déjà suivi | `git rm -r --cached .venv` |
| Travaux en cours à mettre de côté | — | `git stash push -m "wip"` puis `git stash pop` |
