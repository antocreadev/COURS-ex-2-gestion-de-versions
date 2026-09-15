# TP 3 — Revue de code et conflits de merge

**Durée :** ~1 h 35 · **Par groupes de 2 binômes** (A et B), sur **un seul** dépôt

## Objectif

1. Provoquer un vrai conflit de merge et le résoudre proprement.
2. Mener une revue de code structurée et argumentée.

---

## Mise en place (5 min)

Ce TP demande **quatre personnes sur un seul dépôt**. Choisissez le dépôt du
binôme A ; son propriétaire y ajoute les deux membres du binôme B :

```bash
gh api -X PUT repos/PROPRIETAIRE_A/tp-gestion-de-versions/collaborators/LOGIN_B1 -f permission=push
gh api -X PUT repos/PROPRIETAIRE_A/tp-gestion-de-versions/collaborators/LOGIN_B2 -f permission=push
```

Le binôme B accepte l'invitation, puis clone ce dépôt :

```bash
gh repo clone PROPRIETAIRE_A/tp-gestion-de-versions tp-conflits
cd tp-conflits && make install && make hooks && make check
```

Tout le monde travaille désormais sur le **même** `main`. C'est exactement la
situation qui produit des conflits — et c'est le but.

---

## Partie A — Provoquer un conflit (30 min)

Le conflit n'arrive pas par hasard : il arrive quand deux branches modifient les
**mêmes lignes**. On va donc le fabriquer.

### 1. Les deux binômes partent du même point

```bash
git switch main && git pull --ff-only
```

- **Binôme A :** `git switch -c feat/mention-europeenne`
- **Binôme B :** `git switch -c feat/mention-numerique`

### 2. Les deux modifient la fonction `mention`

Dans `src/tpgit/notes.py`, tous deux réécrivent le corps de `mention` :

- **A** renvoie des libellés européens : `"F"`, `"E"`, `"D"`, `"C"`, `"B"`, `"A"`.
- **B** renvoie un entier de 0 à 5 (et adapte l'annotation de retour).

Chacun met à jour les tests correspondants, vérifie `make check`, commite et
pousse.

### 3. A merge en premier

Le binôme A ouvre sa PR, la fait relire par B, et la merge.

### 4. B se met à jour

```bash
git switch main && git pull --ff-only
git switch feat/mention-numerique
git merge main
```

💥 **Conflit.**

### 5. Résoudre

Suivez [`docs/resolution-conflits.md`](resolution-conflits.md).

**Ce n'est pas qu'une manipulation technique : c'est une décision de conception.**
Discutez à quatre : les deux fonctionnalités sont-elles compatibles ? Faut-il

- garder les deux avec des noms différents (`mention`, `mention_europeenne`) ?
- un paramètre `format: Literal["fr", "eu", "numerique"]` ?
- abandonner l'une des deux ?

Implémentez la décision, puis :

```bash
make check                 # obligatoire : le code fusionné doit vraiment marcher
git add src/tpgit/notes.py tests/test_notes.py
git merge --continue
git push
```

**À rendre :** 5 lignes dans la description de la PR expliquant la décision de
conception et pourquoi les autres options ont été écartées.

---

## Partie B — Revue de code approfondie (45 min)

### 1. Introduire des défauts

Chaque binôme crée une branche contenant **quatre défauts volontaires** parmi :

| Type de défaut | Exemple |
|---|---|
| Bug logique | mauvaise borne (`<` au lieu de `<=`) |
| Cas limite non géré | division par zéro sur une liste vide |
| Mauvais nommage | `def calc(x, y)` |
| Code mort | fonction jamais appelée, import inutile |
| Test tautologique | `assert moyenne([10]) == moyenne([10])` |
| Docstring fausse | décrit un comportement que le code n'a pas |
| Complexité inutile | 4 `if` imbriqués pour 2 conditions |

⚠️ Contrainte : **la CI doit rester verte**. C'est le point du TP — un outil
automatique ne voit ni les mauvais noms, ni les tests vides, ni une docstring
mensongère. Seul un humain les voit.

Ouvrez la PR, notez les 4 défauts sur un papier (sans les publier).

### 2. Relire la PR de l'autre binôme

```bash
gh pr checkout <numéro>
make check
gh pr diff <numéro>
```

Objectif : retrouver les 4 défauts. Pour chacun, un commentaire en ligne avec :

- ce qui ne va pas ;
- **pourquoi** c'est un problème (quel cas concret casse) ;
- une proposition ;
- une étiquette : `[bloquant]`, `[suggestion]` ou `[question]`.

Utilisez les **suggestions GitHub** (bloc ```` ```suggestion ````) : l'auteur
applique la correction en un clic.

Concluez par *Request changes* + une synthèse de 3 lignes.

### 3. Corriger et clore

L'auteur répond à chaque commentaire, corrige, pousse, redemande une revue. Le
relecteur approuve. Merge.

---

## Partie C — Débriefing (15 min)

À rendre, une page par groupe :

1. Combien de défauts sur 4 ont été trouvés par les relecteurs ? Lesquels ont
   échappé, et pourquoi ?
2. Lesquels **auraient pu** être attrapés par un outil automatique ? Lesquels
   sont irréductiblement humains ?
3. Le conflit de la partie A : combien de temps pour le résoudre ? Qu'est-ce qui
   l'aurait évité ou réduit ?
4. Une règle que vous ajouteriez au `CONTRIBUTING.md` à la lumière de ce TP.

---

## À retenir

> La CI répond à « est-ce que ça marche ? ».
> La revue répond à « est-ce qu'on veut vivre avec ce code pendant trois ans ? ».
>
> Les deux sont nécessaires ; aucune ne remplace l'autre.
