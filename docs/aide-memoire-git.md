# Aide-mémoire Git

Les commandes réellement utilisées dans ce TP. À garder ouvert pendant la séance.

## Configuration initiale (une fois par machine)

```bash
git config --global user.name "Prénom Nom"
git config --global user.email "prenom.nom@etu.univ.fr"
git config --global init.defaultBranch main
git config --global pull.ff only            # jamais de merge implicite au pull
git config --global push.autoSetupRemote true   # plus besoin de -u au premier push
git config --global core.editor "code --wait"   # ou nano, vim…
```

## Se repérer

```bash
git status                 # le réflexe à avoir toutes les 2 minutes
git log --oneline -10
git log --oneline --graph --all --decorate   # voir la topologie des branches
git diff                   # modifications non indexées
git diff --staged          # ce qui partira au prochain commit
git branch -vv             # branches locales et leur branche distante
git show <sha>             # contenu d'un commit
```

## Branches

```bash
git switch main
git pull --ff-only
git switch -c feat/ma-fonctionnalite    # créer + basculer
git switch -                            # revenir à la branche précédente
git branch -d feat/ma-fonctionnalite    # supprimer (sûr : refuse si non mergée)
git branch -D feat/ma-fonctionnalite    # forcer la suppression
git fetch --prune                       # nettoyer les branches distantes disparues
```

## Enregistrer

```bash
git add fichier.py
git add -p                              # choisir morceau par morceau
git add -u                              # tous les fichiers déjà suivis
git commit -m "feat(stats): ajoute la médiane"
git commit --amend                      # corriger le dernier commit (non poussé !)
git commit --amend --no-edit
```

## Annuler

| Je veux… | Commande |
|---|---|
| désindexer un fichier | `git restore --staged fichier.py` |
| jeter mes modifications d'un fichier | `git restore fichier.py` ⚠️ destructif |
| défaire le dernier commit, garder le travail | `git reset --soft HEAD~1` |
| défaire le dernier commit et l'indexation | `git reset HEAD~1` |
| tout jeter jusqu'au dernier commit | `git reset --hard HEAD` ⚠️ destructif |
| annuler un commit déjà poussé | `git revert <sha>` (crée un commit inverse) |
| retrouver un commit « perdu » | `git reflog` |

> `revert` est la seule méthode acceptable sur une branche partagée : elle ne
> réécrit pas l'historique.

## Mettre de côté

```bash
git stash push -m "wip: essai médiane"
git stash list
git stash pop            # réapplique et retire de la pile
git stash drop
```

## Synchroniser

```bash
git fetch origin                 # récupère sans rien modifier localement
git pull --ff-only               # met à jour si aucune divergence
git pull --rebase                # rejoue mes commits au-dessus du distant
git push
git push -u origin ma-branche    # premier push d'une nouvelle branche
git push --force-with-lease      # force « prudent » : refuse d'écraser le travail d'autrui
```

> Ne jamais utiliser `git push --force` tout court. `--force-with-lease` vérifie
> d'abord que personne n'a poussé entre-temps.

## Intégrer main dans ma branche

```bash
git switch main && git pull --ff-only
git switch ma-branche
git merge main              # recommandé pendant une relecture
# ou
git rebase main             # historique linéaire, réécrit mes commits
```

## Conflits

```bash
git status                      # liste les fichiers en conflit
# ... éditer, supprimer les marqueurs <<<<<<< ======= >>>>>>> ...
git add fichier-resolu.py
git merge --continue            # ou git rebase --continue
git merge --abort               # tout annuler et revenir en arrière
```

## Enquêter

```bash
git blame fichier.py            # qui a écrit quelle ligne, et dans quel commit
git log -S "moyenne_ponderee"   # commits qui ajoutent/suppriment ce texte
git log -p fichier.py           # historique détaillé d'un fichier
git bisect start                # recherche dichotomique du commit fautif
git bisect bad && git bisect good <sha>
```

## GitHub CLI (`gh`)

```bash
gh auth login
gh repo clone antocreadev/COURS-ex-2-gestion-de-versions

gh issue list
gh issue view 12
gh issue develop 12 --checkout        # crée la branche liée à l'issue

gh pr create --fill --web
gh pr list
gh pr status
gh pr checks                          # état de la CI de ma PR
gh pr view 34 --web
gh pr diff 34
gh pr checkout 34                     # récupérer la PR d'un coéquipier pour la tester
gh pr review 34 --approve
gh pr review 34 --request-changes -b "Il manque un test sur la série vide."
gh pr merge --squash --delete-branch

gh run list
gh run view --log-failed              # lire uniquement ce qui a échoué dans la CI
gh run watch                          # suivre la CI en direct
```

## Commandes du projet

```bash
make install   # environnement + dépendances
make hooks     # hooks Git
make format    # reformate
make lint      # style
make types     # mypy
make test      # tests + couverture
make check     # ⭐ tout, comme la CI
make clean
```
