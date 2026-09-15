#!/usr/bin/env bash
# Transforme ce clone en VOTRE dépôt GitHub, prêt pour le TP.
#
# Usage :
#   ./scripts/creer-mon-depot.sh <nom-du-depot> [login1] [login2] ...
#
# Exemples :
#   ./scripts/creer-mon-depot.sh tp-gestion-de-versions camille-durand
#   ./scripts/creer-mon-depot.sh tp-gestion-de-versions camille-durand yanis-b
#
# Indiquez les logins GitHub des AUTRES membres de votre équipe (binôme,
# trinôme...) : ils seront ajoutés en collaborateurs et pourront vous relire.
#
# Ce que fait le script :
#   1. renomme l'ancien dépôt distant en « depart » (pour pouvoir le mettre à jour)
#   2. crée VOTRE dépôt public sur GitHub et y pousse l'historique
#   3. ajoute les coéquipiers en collaborateurs
#   4. protège la branche main
#   5. crée les étiquettes et les issues de départ
#
# Prérequis : gh CLI authentifié (gh auth login)

set -euo pipefail

NOM="${1:-}"
shift || true
COEQUIPIERS=("$@")

if [ -z "$NOM" ]; then
  echo "Usage : $0 <nom-du-depot> [login1] [login2] ..." >&2
  exit 1
fi

command -v gh >/dev/null || { echo "gh n'est pas installé : https://cli.github.com" >&2; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "Lancez d'abord : gh auth login" >&2; exit 1; }

MOI="$(gh api user --jq .login)"
DEPOT="$MOI/$NOM"

echo "Compte GitHub  : $MOI"
echo "Dépôt à créer  : $DEPOT (public)"
if [ "${#COEQUIPIERS[@]}" -eq 0 ]; then
  echo "Coéquipiers    : aucun"
else
  echo "Coéquipiers    : ${COEQUIPIERS[*]}"
fi
echo
read -r -p "Continuer ? [o/N] " reponse
[[ "$reponse" == "o" || "$reponse" == "O" ]] || { echo "Annulé."; exit 0; }

# --- 1. Garder une référence vers le dépôt de départ ----------------------
if git remote get-url origin >/dev/null 2>&1; then
  git remote rename origin depart
  echo "→ ancien distant renommé en « depart »"
fi

# --- 2. Créer le dépôt et pousser -----------------------------------------
echo "→ création du dépôt..."
gh repo create "$NOM" --public --source=. --remote=origin --push
echo "   https://github.com/$DEPOT"

# --- 3. Coéquipiers --------------------------------------------------------
# Le test sur la taille est nécessaire : avec `set -u`, bash 3.2 (celui de
# macOS) refuse d'expanser "${tableau[@]}" quand le tableau est vide.
if [ "${#COEQUIPIERS[@]}" -gt 0 ]; then
  for login in "${COEQUIPIERS[@]}"; do
    gh api -X PUT "repos/$DEPOT/collaborators/$login" -f permission=push >/dev/null
    echo "→ $login invité en collaborateur (droit d'écriture)"
  done
fi

# --- 4. Réglages des Pull Requests ----------------------------------------
echo "→ réglages des PR (squash uniquement, suppression auto des branches)..."
gh api -X PATCH "repos/$DEPOT" \
  -F allow_squash_merge=true \
  -F allow_merge_commit=false \
  -F allow_rebase_merge=false \
  -F delete_branch_on_merge=true \
  -f squash_merge_commit_title=PR_TITLE \
  -f squash_merge_commit_message=PR_BODY >/dev/null

# --- 5. Protection de main -------------------------------------------------
# Seul sur le dépôt, on n'exige AUCUNE approbation : GitHub interdit d'approuver
# ses propres PR, vous seriez bloqué. Dès qu'il y a au moins un coéquipier, on
# passe à 1. La CI, elle, reste obligatoire dans tous les cas.
APPROBATIONS=0
[ "${#COEQUIPIERS[@]}" -gt 0 ] && APPROBATIONS=1

echo "→ protection de main (approbations requises : $APPROBATIONS)..."
gh api -X PUT "repos/$DEPOT/branches/main/protection" \
  -F 'required_status_checks[strict]=true' \
  -f 'required_status_checks[contexts][]=CI OK' \
  -f 'required_status_checks[contexts][]=Conventions de PR' \
  -F "required_pull_request_reviews[required_approving_review_count]=$APPROBATIONS" \
  -F 'required_pull_request_reviews[dismiss_stale_reviews]=true' \
  -F 'required_conversation_resolution=true' \
  -F 'enforce_admins=false' \
  -F 'allow_force_pushes=false' \
  -F 'allow_deletions=false' \
  -F 'restrictions=null' >/dev/null

# --- 6. Issues de départ ---------------------------------------------------
echo "→ création des étiquettes et des issues..."
"$(dirname "$0")/creer_issues.sh" "$DEPOT" <<< "o"

cat <<TEXTE

────────────────────────────────────────────────────────────────
Votre dépôt est prêt : https://github.com/$DEPOT

  origin  → votre dépôt      (vous poussez ici)
  depart  → le dépôt de cours (lecture seule, pour récupérer des mises à jour)

Vos coéquipiers ont reçu une invitation par mail : une fois acceptée, ils
clonent CE dépôt (et non celui du cours) :
  gh repo clone $DEPOT

Prochaine étape :
  make install && make hooks && make check
  gh issue list --label "bonne-première-issue"
────────────────────────────────────────────────────────────────
TEXTE
