# TP 2 — Faire échouer la CI, lire les logs, corriger

**Durée :** ~1 h

## Objectif

Une CI n'est utile que si l'on sait **lire son échec**. Ici, vous cassez la CI
*volontairement*, une fois par type d'échec, pour apprendre à reconnaître
chaque message.

Travaillez sur **une seule branche**, en poussant à chaque étape.

```bash
git switch main && git pull --ff-only
git switch -c chore/exploration-ci
git push -u origin chore/exploration-ci
gh pr create --title "chore(ci): exploration des échecs de CI" \
             --body "PR d'exploration : je casse volontairement la CI pour apprendre à lire ses échecs. Ne pas merger." \
             --draft
```

> La PR est en **brouillon** : personne ne la relira, mais la CI tourne.

Pour chaque cas ci-dessous, remplissez le tableau de synthèse à la fin.

---

## Cas 1 — Erreur de formatage

```python
# dans src/tpgit/stats.py
def   mediane( valeurs ) :
```

```bash
git commit -am "chore: casse le formatage" && git push
gh run watch
```

**Questions**
1. Quel job échoue ? À quelle étape exactement ?
2. Quelle commande locale reproduit l'échec en 2 secondes ?
3. Quelle commande le corrige automatiquement ?

**Correction :** `make format`, puis recommiter.

---

## Cas 2 — Erreur de lint (variable inutilisée)

```python
def mediane(valeurs: Sequence[float]) -> float:
    inutile = 42
    ...
```

**Questions**
1. Quel code de règle ruff apparaît (`F841`, `ARG001`… ) ?
2. Pourquoi ruff signale-t-il cela alors que le code *fonctionne* ?
3. Dans la PR, où apparaît l'erreur en plus des logs ?
   *(indice : `--output-format=github` produit des annotations directement dans
   l'onglet « Files changed »)*

---

## Cas 3 — Erreur de type

```python
def mediane(valeurs: Sequence[float]) -> str:   # le retour est un float !
```

**Questions**
1. Quel outil attrape l'erreur ? Les **tests** l'auraient-ils attrapée ?
2. Quel est l'intérêt d'un contrôle de types *en plus* des tests ?

---

## Cas 4 — Test en échec

```python
def mediane(valeurs: Sequence[float]) -> float:
    return 0.0  # implémentation cassée
```

**Questions**
1. Combien de jobs deviennent rouges ? Pourquoi plusieurs ?
2. Dans les logs de pytest, retrouvez la ligne `assert` fautive, la valeur
   attendue et la valeur obtenue.
3. `fail-fast: false` est réglé dans la matrice. Qu'observe-t-on grâce à cela ?

---

## Cas 5 — Couverture insuffisante

Ajoutez une fonction **non testée** :

```python
def note_sur_100(note: float) -> float:
    """Convertit une note sur 20 en note sur 100.

    Args:
        note: La note sur 20.

    Returns:
        La note ramenée sur 100.
    """
    if note < 0:
        raise ValueError("Note négative.")
    return note * 5
```

**Questions**
1. Quel est le message exact de pytest ?
2. Dans le rapport `term-missing`, quelles lignes sont signalées ?
3. Écrivez le minimum de tests pour repasser au-dessus de 90 %.
4. **Question de fond :** 100 % de couverture signifie-t-il « sans bug » ?
   Trouvez un contre-exemple sur cette fonction.

---

## Cas 6 — Convention de PR non respectée

Renommez votre PR en `mise à jour` :

```bash
gh pr edit --title "mise à jour"
```

**Questions**
1. Quel workflow échoue ? Pourquoi *ce* contrôle ne peut-il pas être un hook Git ?
2. Videz la description de la PR : que se passe-t-il ?
3. Remettez un titre et une description valides ; la CI se relance-t-elle
   toute seule ?

---

## Cas 7 — Contourner les hooks

```bash
git switch -c chore/contournement
echo "x=1" >> src/tpgit/stats.py
git commit -am "n importe quoi" --no-verify
git push --no-verify
```

**Questions**
1. Le commit passe-t-il en local ? Et la CI, que dit-elle ?
2. Formulez en une phrase la différence de nature entre un **hook** et la **CI**.
3. Pourquoi garde-t-on quand même les hooks, s'ils sont contournables ?

---

## Synthèse à rendre

| Cas | Job en échec | Étape | Commande locale équivalente | Correction |
|---|---|---|---|---|
| 1. Formatage | | | | |
| 2. Lint | | | | |
| 3. Types | | | | |
| 4. Test | | | | |
| 5. Couverture | | | | |
| 6. Convention de PR | | | | |
| 7. `--no-verify` | | | | |

**Question finale.** Classez ces sept contrôles du moins cher au plus cher à
corriger, selon le moment où l'erreur est détectée (dans l'éditeur, au commit,
au push, dans la CI, en production). Que vous inspire ce classement sur la place
à donner à chaque outil ?

---

## Nettoyage

```bash
gh pr close --delete-branch
git switch main && git pull --ff-only && git fetch --prune
```
