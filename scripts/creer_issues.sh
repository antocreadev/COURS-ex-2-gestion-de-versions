#!/usr/bin/env bash
# Crée les étiquettes et les issues de départ du TP.
#
# Usage :  ./scripts/creer_issues.sh [ORG/DEPOT]
# Prérequis : gh CLI authentifié (gh auth login)

set -euo pipefail

DEPOT="${1:-$(gh repo view --json nameWithOwner --jq .nameWithOwner)}"
echo "Dépôt cible : $DEPOT"
read -r -p "Continuer ? [o/N] " reponse
[[ "$reponse" == "o" || "$reponse" == "O" ]] || { echo "Annulé."; exit 0; }

etiquette() {
  gh label create "$1" --repo "$DEPOT" --color "$2" --description "$3" --force >/dev/null
  echo "  étiquette : $1"
}

echo "Création des étiquettes..."
etiquette "bonne-première-issue" "7057ff" "Idéale pour une première contribution"
etiquette "fonctionnalité"       "0e8a16" "Nouveau comportement"
etiquette "bogue"                "d73a4a" "Quelque chose ne fonctionne pas"
etiquette "documentation"        "0075ca" "Documentation à écrire ou corriger"
etiquette "tests"                "fbca04" "Couverture de tests"
etiquette "dépendances"          "cfd3d7" "Mise à jour de dépendances"
etiquette "ci"                   "1d76db" "Intégration continue"
etiquette "facile"               "c2e0c6" "Difficulté : facile"
etiquette "moyenne"              "fef2c0" "Difficulté : moyenne"
etiquette "difficile"            "f9d0c4" "Difficulté : difficile"

CRITERES=$'\n\n### Critères d\'acceptation\n\n- [ ] Branche nommée selon la convention (`feat/…`, `fix/…`, `docs/…`)\n- [ ] Commits au format Conventional Commits\n- [ ] Fonction typée et documentée (docstring Google)\n- [ ] Cas limites testés (série vide, valeurs hors barème…)\n- [ ] `make check` vert, couverture ≥ 90 %\n- [ ] PR décrite, liée à cette issue, relue et approuvée'

issue() {
  local titre="$1" corps="$2" etiquettes="$3"
  gh issue create --repo "$DEPOT" --title "$titre" \
    --body "${corps}${CRITERES}" --label "$etiquettes" >/dev/null
  echo "  issue : $titre"
}

echo "Création des issues..."

issue "feat(stats): ajouter le calcul de la variance" \
"La variance est la moyenne des carrés des écarts à la moyenne. \`ecart_type\` la calcule déjà en interne : il serait plus clair de l'exposer et de réutiliser \`variance\` dans \`ecart_type\`.

**Fichier :** \`src/tpgit/stats.py\`
**Signature attendue :** \`def variance(valeurs: Sequence[float]) -> float\`" \
"bonne-première-issue,fonctionnalité,facile"

issue "feat(stats): ajouter le calcul du mode" \
"Le mode est la valeur la plus fréquente d'une série. Décidez et documentez ce que fait la fonction en cas d'égalité (plusieurs modes) : renvoyer la plus petite ? une liste ?

**Fichier :** \`src/tpgit/stats.py\`" \
"bonne-première-issue,fonctionnalité,facile"

issue "feat(stats): ajouter le calcul des quartiles" \
"Renvoyer Q1, Q2 (médiane) et Q3. Précisez dans la docstring la convention de calcul retenue — il en existe plusieurs.

**Fichier :** \`src/tpgit/stats.py\`" \
"fonctionnalité,moyenne"

issue "feat(notes): ajouter le rattrapage par note minimale" \
"Un étudiant est ajourné si l'une de ses notes est inférieure à un seuil éliminatoire, même si sa moyenne dépasse 10.

**Signature attendue :** \`def est_admis_avec_eliminatoire(notes, seuil_moyenne=10.0, note_eliminatoire=5.0) -> bool\`
**Fichier :** \`src/tpgit/notes.py\`" \
"bonne-première-issue,fonctionnalité,facile"

issue "feat(notes): ajouter la compensation entre unités d'enseignement" \
"Calculer si un ensemble d'UE (chacune avec sa moyenne et son coefficient) se compense pour atteindre 10 de moyenne générale.

**Fichier :** \`src/tpgit/notes.py\`" \
"fonctionnalité,moyenne"

issue "feat(notes): ajouter la fonction de normalisation d'une note" \
"Convertir une note d'un barème quelconque vers le barème /20.

**Signature attendue :** \`def normaliser(note: float, bareme: float) -> float\`
Attention au barème nul ou négatif." \
"bonne-première-issue,fonctionnalité,facile"

issue "feat(cli): ajouter une commande 'bulletin'" \
"Afficher en une seule commande : moyenne, mention, admission et synthèse statistique.

**Fichier :** \`src/tpgit/cli.py\`
Pensez à l'option \`--json\`, comme les autres sous-commandes." \
"fonctionnalité,moyenne"

issue "feat(cli): lire les notes depuis un fichier CSV" \
"Ajouter une option \`--fichier notes.csv\` aux sous-commandes existantes, en alternative aux notes passées en arguments.

Gérez proprement : fichier absent, ligne vide, valeur non numérique. Le message d'erreur doit indiquer le **numéro de ligne** fautif." \
"fonctionnalité,difficile"

issue "feat(cli): ajouter une option --precision" \
"Permettre de choisir le nombre de décimales affichées (2 par défaut).

**Fichier :** \`src/tpgit/cli.py\`" \
"bonne-première-issue,fonctionnalité,facile"

issue "test(notes): couvrir les bornes exactes des mentions" \
"Les bornes 10 / 12 / 14 / 16 doivent être testées **à la valeur exacte** et juste en dessous. Vérifiez que les tests existants ne laissent aucun trou, et ajoutez un test de propriété : pour toute moyenne valide, \`mention\` renvoie toujours l'une des 5 valeurs attendues." \
"bonne-première-issue,tests,facile"

issue "docs: ajouter une section 'Exemples d'utilisation' au README" \
"Illustrer chaque sous-commande de la CLI avec sa sortie réelle, y compris le mode \`--json\` et un cas d'erreur.

**Fichier :** \`README.md\`" \
"bonne-première-issue,documentation,facile"

issue "fix(notes): le message d'erreur des coefficients manque de contexte" \
"Quand un coefficient est invalide, le message ne dit pas **lequel**. Faire apparaître l'indice et la valeur fautive.

**Fichier :** \`src/tpgit/notes.py\`" \
"bonne-première-issue,bogue,facile"

issue "ci: ajouter un contrôle de vulnérabilités des dépendances" \
"Ajouter un job qui exécute \`pip-audit\` dans \`.github/workflows/ci.yml\`.

Question à trancher dans la description de la PR : ce job doit-il **bloquer** le merge, ou seulement avertir ? Justifiez." \
"ci,difficile"

echo
echo "Terminé. Vérifiez : gh issue list --repo $DEPOT"
