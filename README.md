# TP — Le cycle de contribution à un projet

[![CI](https://github.com/antocreadev/COURS-ex-2-gestion-de-versions/actions/workflows/ci.yml/badge.svg)](https://github.com/antocreadev/COURS-ex-2-gestion-de-versions/actions/workflows/ci.yml)

> Dépôt support de cours (L3 Informatique).
> Objectif : vivre **une fois en entier** le cycle qu'on retrouve dans toutes les
> équipes de développement professionnelles.

```
issue → branche → commits → push → Pull Request → CI → revue → corrections → merge → nettoyage
```

Le code métier (une petite bibliothèque de calcul de notes) est volontairement
trivial. **Ce n'est pas le sujet.** Le sujet, c'est tout ce qu'il y a autour :
les conventions, l'automatisation locale (hooks), l'automatisation distante (CI)
et la revue par les pairs.

---

## 1. Démarrage rapide

Ce dépôt est le **point de départ**, pas votre terrain de jeu : vous n'avez pas
le droit d'y pousser. Vous allez en faire **votre propre dépôt**, sur votre
compte GitHub — c'est là que vivront vos branches, vos PR, votre CI et vos
revues.

**Un seul dépôt par équipe** (binôme, trinôme…) : l'un de vous le crée, les
autres y sont ajoutés en collaborateurs. Il faut être au moins deux, car GitHub
interdit d'approuver sa propre Pull Request.

```bash
# 1. Récupérer le projet de départ
git clone https://github.com/antocreadev/COURS-ex-2-gestion-de-versions.git tp-gestion-de-versions
cd tp-gestion-de-versions

# 2. En faire VOTRE dépôt GitHub (crée le dépôt, pousse, protège main, crée les issues)
gh auth login                                             # une seule fois par machine
./scripts/creer-mon-depot.sh tp-gestion-de-versions LOGIN_COEQUIPIER_1 [LOGIN_COEQUIPIER_2 ...]

# 3. Créer l'environnement et installer le projet + les outils de qualité
make install

# 4. Installer les hooks Git (très important : voir §4)
make hooks

# 5. Vérifier que tout est vert chez vous, comme dans la CI
make check
```

Si `make check` est vert, vous êtes prêt à contribuer.

<details>
<summary>Ce que fait exactement <code>creer-mon-depot.sh</code> (et comment le faire à la main)</summary>

```bash
git remote rename origin depart          # on garde un lien vers le dépôt de cours
gh repo create tp-gestion-de-versions --public --source=. --remote=origin --push

# vos coéquipiers doivent pouvoir pousser et vous relire (une ligne chacun)
gh api -X PUT repos/VOUS/tp-gestion-de-versions/collaborators/COEQUIPIER -f permission=push

# squash uniquement, suppression automatique des branches mergées
gh api -X PATCH repos/VOUS/tp-gestion-de-versions \
  -F allow_squash_merge=true -F allow_merge_commit=false \
  -F allow_rebase_merge=false -F delete_branch_on_merge=true

# main devient inaccessible en écriture directe
gh api -X PUT repos/VOUS/tp-gestion-de-versions/branches/main/protection \
  -F 'required_status_checks[strict]=true' \
  -f 'required_status_checks[contexts][]=CI OK' \
  -f 'required_status_checks[contexts][]=Conventions de PR' \
  -F 'required_pull_request_reviews[required_approving_review_count]=1' \
  -F 'required_conversation_resolution=true' \
  -F 'enforce_admins=false' -F 'allow_force_pushes=false' -F 'restrictions=null'

./scripts/creer_issues.sh VOUS/tp-gestion-de-versions
```

Après quoi vous avez **deux dépôts distants** :

| Nom | Pointe vers | Vous pouvez… |
|---|---|---|
| `origin` | votre dépôt | pousser des branches, ouvrir des PR |
| `depart` | le dépôt de cours | seulement lire (`git fetch depart`) |
</details>

<details>
<summary>Sans <code>gh</code> : créer le dépôt depuis le site</summary>

1. github.com → **New repository** → nom `tp-gestion-de-versions`, **Public**,
   **sans** README ni .gitignore (le dépôt doit être vide).
2. Puis, dans votre clone :
   ```bash
   git remote rename origin depart
   git remote add origin https://github.com/VOTRE-LOGIN/tp-gestion-de-versions.git
   git push -u origin main
   ```
3. Settings → Collaborators → ajouter vos coéquipiers.
4. Settings → Branches → Add branch ruleset (voir la liste des cases à cocher
   dans [`docs/mise-en-place-enseignant.md`](docs/mise-en-place-enseignant.md) §3).
</details>

<details>
<summary>Sans <code>make</code> (Windows / PowerShell)</summary>

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install --install-hooks
ruff check . ; ruff format --check . ; mypy ; pytest
```
</details>

### Récupérer une mise à jour du dépôt de cours

Si l'enseignant corrige quelque chose après que vous avez créé votre dépôt :

```bash
git fetch depart
git switch -c chore/mise-a-jour-depart
git merge depart/main
make check
git push -u origin chore/mise-a-jour-depart   # puis PR, comme d'habitude
```

---

## 2. Ce que contient ce dépôt

| Fichier / dossier | Rôle |
|---|---|
| `src/tpgit/` | Le code métier (notes, statistiques, CLI) |
| `tests/` | Les tests `pytest` |
| `pyproject.toml` | **Une seule** source de config : projet, ruff, mypy, pytest, coverage |
| `.pre-commit-config.yaml` | Les hooks Git exécutés **avant** chaque commit |
| `scripts/creer-mon-depot.sh` | Transforme ce clone en **votre** dépôt GitHub configuré |
| `scripts/verifier_message_commit.py` | Hook `commit-msg` : valide le format des messages |
| `.github/workflows/ci.yml` | La CI : lint, types, tests, couverture |
| `.github/workflows/pr.yml` | Contrôles propres à la Pull Request (titre, taille) |
| `.github/PULL_REQUEST_TEMPLATE.md` | Le formulaire pré-rempli de toute PR |
| `.github/ISSUE_TEMPLATE/` | Les formulaires de création d'issue |
| `.github/CODEOWNERS` | Qui est automatiquement demandé en revue |
| `CONTRIBUTING.md` | Le contrat de contribution — **à lire avant de coder** |
| `docs/` | Le cours : workflow, aide-mémoire, conflits, TP |

---

## 3. Le cycle, en 10 étapes

```
  main ─────●──────────────────────────────────────●────────▶
            │                                      ▲
            │ 2. git switch -c feat/mediane        │ 9. merge (squash)
            ▼                                      │
   feat/... ●───●───●────────●──────────●──────────┘
             3.  4.  5.push   6.PR+CI   8.corrections
                                  │
                                  ▼
                            7. revue par un pair
```

1. **Prendre une issue.** On ne code jamais « dans le vide » : une issue décrit
   le besoin et sert de référence pour la discussion.
2. **Créer une branche** à partir d'un `main` à jour :
   ```bash
   git switch main && git pull --ff-only
   git switch -c feat/calcul-mediane
   ```
   Nommage : `feat/…`, `fix/…`, `docs/…`, `refactor/…`, `test/…`, `chore/…`.
3. **Développer par petits pas.** Un test qui échoue, puis le code qui le fait
   passer. Commiter souvent.
4. **Commiter** avec un message conventionnel — le hook `commit-msg` refuse le reste :
   ```bash
   git commit -m "feat(stats): ajoute le calcul de la médiane"
   ```
   Au moment du commit, les hooks `pre-commit` reformatent et relisent votre code.
5. **Pousser** la branche :
   ```bash
   git push -u origin feat/calcul-mediane
   ```
6. **Ouvrir la Pull Request.** Le modèle se remplit tout seul : décrivez le
   *pourquoi*, pas seulement le *quoi*. La CI démarre immédiatement.
   ```bash
   gh pr create --fill --web    # ou via l'interface GitHub
   ```
7. **Attendre la CI et la revue.** Une PR rouge ne se relit pas : corrigez d'abord.
8. **Corriger.** Vous répondez aux commentaires, vous poussez de nouveaux commits
   sur la **même** branche : la PR et la CI se mettent à jour automatiquement.
9. **Merger** une fois la CI verte et la revue approuvée (*squash and merge* :
   une PR = un commit propre sur `main`).
10. **Nettoyer** :
    ```bash
    git switch main && git pull --ff-only
    git branch -d feat/calcul-mediane
    ```

> Détail complet, avec les commandes et les pièges : [`docs/workflow-git.md`](docs/workflow-git.md).

---

## 4. Trois niveaux d'automatisation

C'est le cœur pédagogique du dépôt : **la même vérification est jouée à trois
endroits**, de plus en plus tard, et de plus en plus coûteuse à corriger.

| Niveau | Quand | Quoi | Coût d'un échec |
|---|---|---|---|
| **1. Local, à la demande** | `make check` | tout | quelques secondes |
| **2. Hooks Git** | à chaque `git commit` | format, lint, message | quelques secondes |
| **3. CI (GitHub Actions)** | à chaque `push` / PR | tout, sur 3 versions de Python | plusieurs minutes, publiquement |

**La règle :** ce que fait la CI doit pouvoir être joué en local *à l'identique*.
C'est exactement ce que garantit `make check` ici. Une CI qu'on ne peut pas
reproduire chez soi est une CI qu'on subit.

### Les hooks installés

| Hook | Déclenchement | Effet |
|---|---|---|
| `ruff-format` | `pre-commit` | reformate le code (et **annule** le commit pour que vous relisiez) |
| `ruff-check --fix` | `pre-commit` | corrige les erreurs de lint réparables, signale les autres |
| `trailing-whitespace`, `end-of-file-fixer` | `pre-commit` | hygiène des fichiers |
| `check-merge-conflict` | `pre-commit` | empêche de commiter des `<<<<<<<` oubliés |
| `no-commit-to-branch` | `pre-commit` | **interdit de commiter directement sur `main`** |
| `verifier_message_commit.py` | `commit-msg` | impose le format Conventional Commits |
| `pytest` | `pre-push` | refuse de pousser une branche dont les tests échouent |

> Un hook peut être court-circuité (`git commit --no-verify`). C'est volontaire :
> un hook est une **aide**, pas une sécurité. La vraie barrière, c'est la CI, qui
> tourne sur un serveur que vous ne contrôlez pas. Retenez la différence.

---

## 5. Les conventions du dépôt

### Messages de commit — [Conventional Commits](https://www.conventionalcommits.org/fr/)

```
<type>(<portée facultative>): <description à l'impératif, en minuscule>
```

| Type | Usage |
|---|---|
| `feat` | nouvelle fonctionnalité |
| `fix` | correction de bug |
| `docs` | documentation seule |
| `test` | ajout ou correction de tests |
| `refactor` | réécriture sans changement de comportement |
| `perf` | amélioration de performance |
| `style` | mise en forme seule |
| `build`, `ci`, `chore` | outillage, dépendances, config |

```bash
git commit -m "feat(stats): ajoute le calcul de la variance"       # ✅
git commit -m "fix(notes): rejette les coefficients négatifs"      # ✅
git commit -m "corrections diverses"                               # ❌ refusé
git commit -m "Ajout"                                              # ❌ refusé
```

Pourquoi ? Parce qu'un historique lisible permet de générer un CHANGELOG, de
retrouver *quand* un bug est apparu (`git bisect`), et de comprendre une
décision six mois plus tard.

### Qualité du code

- **Ruff** formate et relit (PEP 8, imports, docstrings Google, annotations de type).
- **Mypy** en mode `strict` : toute fonction publique est typée.
- **Pytest** avec un seuil de couverture à **90 %** : une fonctionnalité sans
  test fait échouer la CI.

---

## 6. Commandes utiles

```bash
make install    # environnement virtuel + dépendances
make hooks      # installe les hooks Git (pre-commit, commit-msg, pre-push)
make format     # reformate le code
make lint       # linter (sans modifier les fichiers)
make types      # vérification statique des types
make test       # tests + couverture
make check      # ⭐ tout ce que fait la CI, en local
make clean      # supprime les caches
make aide       # liste les cibles disponibles
```

---

## 7. Travaux pratiques

| TP | Sujet |
|---|---|
| [TP 1](docs/tp-01-premiere-contribution.md) | Votre première contribution de bout en bout |
| [TP 2](docs/tp-02-ci-rouge.md) | Faire échouer la CI volontairement, lire les logs, corriger |
| [TP 3](docs/tp-03-revue-et-conflits.md) | Relire la PR d'un coéquipier, résoudre un conflit de merge |

Ressources : [`docs/workflow-git.md`](docs/workflow-git.md) ·
[`docs/aide-memoire-git.md`](docs/aide-memoire-git.md) ·
[`docs/resolution-conflits.md`](docs/resolution-conflits.md) ·
[`CONTRIBUTING.md`](CONTRIBUTING.md)

---

## 8. Pour l'enseignant

Voir [`docs/mise-en-place-enseignant.md`](docs/mise-en-place-enseignant.md) :
configuration du dépôt modèle, protection de `main`, création en masse des
issues de départ (`scripts/creer_issues.sh`), et grille d'évaluation.

## Licence

MIT — voir [`LICENSE`](LICENSE).
