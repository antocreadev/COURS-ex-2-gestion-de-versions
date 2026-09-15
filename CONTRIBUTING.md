# Contribuer à ce projet

Ce document est le **contrat de contribution**. Dans un vrai projet, il est lu
une fois puis suivi mécaniquement. Ici, il est aussi un support de cours : chaque
règle est justifiée.

---

## 1. Avant de coder

### Prendre une issue

On ne commence pas par le code, on commence par **se mettre d'accord sur le
problème**. Choisissez une issue, commentez-la (`je prends`) et assignez-vous.
Cela évite que deux personnes écrivent le même code en parallèle.

Si le besoin n'existe pas encore en issue : créez-la d'abord. Une PR qui arrive
sans issue oblige le relecteur à découvrir *en même temps* le problème et la
solution — c'est la principale cause de relecture pénible.

### Partir d'un `main` à jour

```bash
git switch main
git pull --ff-only
```

> `--ff-only` refuse de créer un commit de merge silencieux. Si la commande
> échoue, c'est que votre `main` local a divergé : c'est une information utile,
> pas un obstacle.

---

## 2. La branche

```bash
git switch -c <type>/<description-courte-en-kebab-case>
```

| Préfixe | Pour |
|---|---|
| `feat/` | nouvelle fonctionnalité |
| `fix/` | correction de bug |
| `docs/` | documentation |
| `test/` | tests seuls |
| `refactor/` | réécriture sans changement de comportement |
| `chore/` | outillage, dépendances |

```bash
git switch -c feat/calcul-variance        # ✅
git switch -c fix/coefficients-negatifs   # ✅
git switch -c ma-branche                  # ❌
git switch -c test                        # ❌
```

**Une branche = une intention.** Si en cours de route vous corrigez autre chose,
faites-en une seconde branche et une seconde PR.

---

## 3. Développer

### Le cycle test → code

1. Écrivez d'abord un test qui échoue et qui décrit le comportement attendu.
2. Écrivez le code minimal qui le fait passer.
3. Nettoyez (nommage, docstring), les tests restant verts.

```bash
pytest tests/test_stats.py -k variance -v   # ne joue que ce qui vous intéresse
```

### Les règles de code appliquées automatiquement

| Règle | Outil | Vérifiée par |
|---|---|---|
| Formatage (100 colonnes, guillemets, imports triés) | `ruff format` | hook + CI |
| Style et pièges (PEP 8, variables mortes, comprehensions) | `ruff check` | hook + CI |
| Annotations de type partout | `ruff` (ANN) + `mypy --strict` | hook + CI |
| Docstring Google sur toute fonction publique | `ruff` (D) | hook + CI |
| Couverture ≥ 90 % | `pytest-cov` | CI |

Vous n'avez rien à retenir de tout cela : lancez `make check`.

---

## 4. Commiter

### Format imposé

```
<type>(<portée>): <description>

[corps facultatif, après une ligne vide]

[pied de page facultatif : Closes #12, BREAKING CHANGE: …]
```

Contraintes vérifiées par le hook `commit-msg` :

- type parmi `feat fix docs style refactor perf test build ci chore revert` ;
- description **à l'impératif**, en **minuscule**, **sans point final** ;
- première ligne ≤ **72 caractères** ;
- ligne vide obligatoire entre le sujet et le corps.

```bash
git commit -m "feat(stats): ajoute le calcul de la variance"
git commit -m "fix(notes): rejette les coefficients nuls"
git commit -m "test(cli): couvre la sortie JSON de la commande stats"
```

Message plus long :

```bash
git commit -m "fix(notes): corrige la moyenne pondérée sur coefficients décimaux" \
           -m "La division entière tronquait le résultat pour les coefficients
non entiers. On force désormais un calcul en flottants.

Closes #17"
```

### Granularité

Un commit = **un pas cohérent**, qui laisse le dépôt dans un état fonctionnel.
Ni « je commite chaque sauvegarde », ni « je commite une fois à la fin ».

```bash
git add -p        # sélectionne morceau par morceau ce qui entre dans le commit
git status        # vérifiez TOUJOURS ce que vous êtes en train de commiter
```

---

## 5. Pousser et ouvrir la Pull Request

```bash
git push -u origin feat/calcul-variance
```

Le hook `pre-push` lance les tests : un push refusé ici, c'est une CI rouge
évitée.

```bash
gh pr create --fill --web
```

### Ce qu'on attend d'une bonne PR

- **Un titre au format Conventional Commits** (vérifié par la CI).
- **Une description qui explique le *pourquoi***, avec `Closes #<numéro>`.
- **Petite** : viser moins de ~400 lignes de diff. Au-delà, la relecture devient
  superficielle — c'est mesuré, pas une opinion.
- **Verte** : ne demandez pas de relecture tant que la CI est rouge. Si la PR
  n'est pas prête, ouvrez-la en **brouillon** (*draft*).

---

## 6. Relire la PR d'un coéquipier

La revue n'est pas un examen, c'est une **conversation**. Chacun relit au moins
une PR par TP. À trois, faites tourner la relecture en cercle : A relit B, B
relit C, C relit A.

### Grille de relecture

1. **Est-ce que ça répond à l'issue ?** Ni moins, ni plus.
2. **Est-ce que je comprends le code sans explication orale ?**
3. **Les cas limites sont-ils testés ?** (série vide, valeur nulle, négative,
   hors barème, type inattendu)
4. **Les noms disent-ils ce que font les choses ?**
5. **Reste-t-il du code mort, un `print`, un `TODO` sans issue ?**

### Écrire un commentaire utile

| ❌ | ✅ |
|---|---|
| « C'est faux. » | « Si `coefficients` est vide, `sum()` renvoie 0 et on divise par zéro. Un test avec `[]` reproduirait le cas. » |
| « Pas beau. » | « `x` est utilisé pour deux choses différentes ici ; `total` et `effectif` seraient plus clairs. » |
| « Change ça. » | « Suggestion (non bloquant) : `math.fsum` éviterait les erreurs d'arrondi. » |

Distinguez explicitement :
- **bloquant** — doit être corrigé avant merge ;
- **suggestion** — à considérer ;
- **question** — vous voulez comprendre, pas forcément faire changer.

Terminez par une décision claire : *Approuver*, *Demander des changements*, ou
*Commenter*.

### Côté auteur

Répondez à **chaque** commentaire, même par « corrigé en `abc1234` ». Ne
réécrivez pas l'historique (`push --force`) pendant une relecture en cours : le
relecteur perdrait le fil. Poussez des commits supplémentaires ; le *squash* au
merge nettoiera l'historique.

---

## 7. Merger

Conditions (appliquées par la protection de branche) :

- la CI (`CI OK`) est verte ;
- au moins **une** approbation ;
- toutes les conversations sont résolues ;
- la branche est à jour avec `main`.

**Stratégie : *Squash and merge*.** Une PR devient un unique commit sur `main`,
dont le message est le titre de la PR — d'où l'exigence sur le format du titre.
L'historique de `main` reste une suite de changements lisibles.

Puis on nettoie :

```bash
git switch main
git pull --ff-only
git branch -d feat/calcul-variance
git fetch --prune              # supprime les branches distantes déjà mergées
```

---

## 8. Quand la CI est rouge

1. Ouvrez l'onglet **Actions** (ou le check en rouge sous la PR).
2. Dépliez l'étape en échec : **lisez le message d'erreur en entier**.
3. Reproduisez en local : c'est presque toujours possible.

| Job en échec | Commande locale équivalente | Correction |
|---|---|---|
| `Lint & types` → ruff check | `make lint` | `make format`, puis corriger ce qui reste |
| `Lint & types` → ruff format | `make lint` | `make format` |
| `Lint & types` → mypy | `make types` | ajouter/corriger les annotations |
| `Tests (Python 3.x)` | `make test` | corriger le code ou le test |
| couverture < 90 % | `make test` | ajouter des tests sur les lignes listées en `Missing` |
| `pre-commit` | `pre-commit run --all-files` | relancer, puis commiter les fichiers modifiés |
| `Conventions de PR` | — | corriger le **titre** ou la **description** de la PR |

> La CI échoue mais tout passe en local ? Regardez la **version de Python** du
> job en échec : vous utilisez peut-être une syntaxe trop récente.

---

## 9. Ce qui fait refuser une PR

- La CI est rouge.
- Aucun test pour le nouveau comportement.
- La PR mélange plusieurs sujets sans rapport.
- Des fichiers générés (`.venv/`, `__pycache__/`, `.coverage`) sont commités.
- L'historique contient des messages non conventionnels.
- La description est vide ou se résume au titre.
