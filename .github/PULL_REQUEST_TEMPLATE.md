<!--
  Le titre de la PR doit suivre Conventional Commits.
  Exemple : feat(stats): ajoute le calcul de la médiane
-->

## Pourquoi ?

<!-- Le problème ou le besoin. Une PR sans « pourquoi » est impossible à relire. -->

Closes #

## Quoi ?

<!-- Ce que change cette PR, en quelques puces. -->

-
-

## Comment tester ?

```bash
make check
# puis, manuellement :
```

## Points d'attention pour la relecture

<!-- Ce sur quoi vous voulez vraiment un avis : un choix d'implémentation,
     un nom de fonction, un cas limite dont vous n'êtes pas sûr. -->

-

## Check-list

- [ ] `make check` passe en local
- [ ] Les nouveaux comportements sont couverts par des tests
- [ ] Les messages de commit suivent Conventional Commits
- [ ] La documentation (README, docstrings) est à jour
- [ ] La PR est limitée à **un seul** sujet
- [ ] Aucun fichier généré, secret ou `print()` de débogage n'a été commité
