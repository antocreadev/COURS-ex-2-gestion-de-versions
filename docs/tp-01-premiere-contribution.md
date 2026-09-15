# TP 1 — Votre première contribution de bout en bout

**Durée :** ~2 h · **Binômes :** oui (mais chacun ouvre sa propre PR)

## Objectif

Parcourir **une fois en entier** le cycle : issue → branche → code → commits →
push → PR → CI → revue → corrections → merge → ménage.

À la fin, vous devez avoir :

- une branche nommée selon la convention ;
- au moins 2 commits au format Conventional Commits ;
- une PR verte, décrite, liée à une issue ;
- une revue faite sur la PR de quelqu'un d'autre ;
- votre PR mergée et votre branche supprimée.

---

## Partie A — Installation (15 min)

```bash
git clone <url-du-depot>
cd <depot>
make install
make hooks
make check
```

✅ **Point de contrôle 1 :** `make check` affiche « Tout est vert ».

### Vérifier que les hooks sont bien actifs

Faites délibérément échouer chaque garde-fou, pour savoir à quoi ressemble
l'erreur avant de la rencontrer pour de vrai.

```bash
# 1. Commit interdit sur main
git switch main
echo "# test" >> README.md
git add README.md && git commit -m "docs: test"
```
→ doit être refusé par `no-commit-to-branch`.

```bash
git restore --staged README.md && git restore README.md

# 2. Message de commit non conforme
git switch -c chore/test-hooks
echo "# test" >> README.md && git add README.md
git commit -m "modif"
```
→ doit être refusé par le hook `commit-msg`, avec le format attendu affiché.

```bash
git commit -m "docs: teste les hooks du dépôt"   # ✅ accepté
git switch main && git branch -D chore/test-hooks
```

✅ **Point de contrôle 2 :** vous savez reconnaître un refus de hook.

---

## Partie B — Prendre une issue (10 min)

```bash
gh issue list --label "bonne-première-issue"
```

Choisissez-en **une**, commentez `je prends`, assignez-vous.

> Deux personnes sur la même issue = deux PR en conflit. Vérifiez qu'elle n'est
> pas déjà assignée.

---

## Partie C — Coder (45 min)

```bash
git switch main
git pull --ff-only
git switch -c feat/<votre-sujet>
```

### 1. Écrire le test d'abord

Dans `tests/test_stats.py` (ou le fichier correspondant) :

```python
def test_variance_serie_constante():
    assert variance([10, 10, 10]) == pytest.approx(0.0)
```

```bash
pytest tests/test_stats.py -k variance
```
→ doit échouer (`ImportError` ou `NameError`). **C'est normal et c'est le but** :
un test qui passe avant que le code existe ne teste rien.

```bash
git add tests/test_stats.py
git commit -m "test(stats): décrit le comportement attendu de variance"
```

### 2. Écrire le code

Dans `src/tpgit/stats.py`. Le dépôt exige :

- une **annotation de type** sur chaque paramètre et sur le retour ;
- une **docstring Google** (`Args:`, `Returns:`, `Raises:`, `Examples:`) ;
- la gestion des **cas limites** (série vide, valeurs hors barème…).

Prenez `ecart_type` comme modèle.

```bash
pytest tests/test_stats.py -k variance    # doit passer
make check                                 # doit être vert
git add src/tpgit/stats.py
git commit -m "feat(stats): ajoute le calcul de la variance"
```

### 3. Compléter

- Cas limites : série vide, une seule valeur, valeurs négatives.
- Exporter la fonction dans `src/tpgit/__init__.py` si elle est publique.
- Mettre la documentation à jour si le comportement visible change.

✅ **Point de contrôle 3 :** `make check` est vert et vous avez ≥ 2 commits.

---

## Partie D — Pull Request (15 min)

```bash
git push -u origin feat/<votre-sujet>
gh pr create --fill --web
```

Remplissez le modèle **complètement** :

- titre au format `feat(stats): ajoute le calcul de la variance` ;
- section *Pourquoi* : le besoin, pas la solution ;
- `Closes #<numéro de votre issue>` ;
- *Points d'attention* : dites au relecteur où regarder en priorité ;
- cochez la check-list honnêtement.

```bash
gh pr checks --watch
```

✅ **Point de contrôle 4 :** le check `CI OK` est vert.

> Rouge ? C'est prévu au programme. Lisez le job en échec, reproduisez en local
> (tableau de correspondance dans [`CONTRIBUTING.md`](../CONTRIBUTING.md) §8),
> corrigez, recommitez, repoussez. La CI se relance seule.

---

## Partie E — Revue croisée (30 min)

Échangez les numéros de PR avec un autre binôme.

### En tant que relecteur

```bash
gh pr checkout <numéro>     # récupérer la branche pour la tester
make check
gh pr diff <numéro>
```

Sur GitHub, onglet **Files changed** → commentez **ligne par ligne**. Laissez au
moins **trois** commentaires, dont au moins un vraiment utile (pas « ok »).
Utilisez la grille de [`CONTRIBUTING.md`](../CONTRIBUTING.md) §6, et préfixez
chaque commentaire par `[bloquant]`, `[suggestion]` ou `[question]`.

Terminez par *Request changes* ou *Approve* — avec une phrase de synthèse.

### En tant qu'auteur

Répondez à **chaque** commentaire. Corrigez, puis :

```bash
git commit -m "fix(stats): gère le cas de la série vide"
git push
```

La PR et la CI se mettent à jour automatiquement. Redemandez une revue.

✅ **Point de contrôle 5 :** votre PR est approuvée et verte.

---

## Partie F — Merge et ménage (10 min)

```bash
gh pr merge --squash --delete-branch

git switch main
git pull --ff-only
git branch -d feat/<votre-sujet>
git fetch --prune
git log --oneline -5
```

Observez : vos 3–4 commits de branche sont devenus **un seul** commit sur `main`,
intitulé comme votre PR. Votre issue s'est fermée toute seule grâce au
`Closes #…`.

✅ **Point de contrôle 6 :** `git log --oneline -5` est lisible, `git branch`
ne liste plus votre branche.

---

## Ce qu'on évalue

| Critère | Points |
|---|---|
| Nommage de branche et format des commits | 3 |
| Qualité du code (types, docstring, cas limites) | 4 |
| Tests pertinents, couverture maintenue | 4 |
| Description de la PR (le *pourquoi*, lien vers l'issue) | 3 |
| CI verte sans `--no-verify` ni contournement | 2 |
| Qualité de la revue faite sur la PR d'autrui | 4 |
| **Total** | **20** |

---

## Pour aller plus loin

- Ajoutez un badge de CI dans le README :
  `![CI](https://github.com/ORG/DEPOT/actions/workflows/ci.yml/badge.svg)`
- Regardez une PR de Dependabot et décidez si elle doit être mergée.
- Lancez `git log --oneline --graph --all` : vous *voyez* le cycle que vous venez
  de parcourir.
