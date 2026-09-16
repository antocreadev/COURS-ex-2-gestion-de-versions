#!/usr/bin/env bash
# Exécute un outil depuis l'environnement virtuel du projet, que celui-ci soit
# activé ou non.
#
# Utilisé par les hooks Git (voir .pre-commit-config.yaml) : Git ne lance pas
# les hooks dans votre shell, il ne « voit » donc pas un `source .venv/bin/activate`
# fait dans votre terminal. Sans ce script, un `git push` échouerait sur
# « Executable `pytest` not found » dès que le venv n'est pas activé.
#
# Usage :  ./scripts/dans-le-venv.sh <outil> [arguments...]

set -euo pipefail

RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTIL="${1:-}"
[ -n "$OUTIL" ] || { echo "Usage : $0 <outil> [arguments...]" >&2; exit 1; }
shift

# .venv/bin sur macOS et Linux, .venv/Scripts sur Windows (Git Bash).
for dossier in "$RACINE/.venv/bin" "$RACINE/.venv/Scripts" "$RACINE/venv/bin" "$RACINE/venv/Scripts"; do
  for candidat in "$dossier/$OUTIL" "$dossier/$OUTIL.exe"; do
    [ -x "$candidat" ] && exec "$candidat" "$@"
  done
done

# À défaut, l'outil est peut-être installé globalement (c'est le cas dans la CI).
command -v "$OUTIL" >/dev/null 2>&1 && exec "$OUTIL" "$@"

cat >&2 <<TEXTE
✖ « $OUTIL » est introuvable.

  Ni dans l'environnement virtuel du projet, ni dans votre PATH.
  Créez l'environnement puis réessayez :

      make install

  (ou, sans make :  python -m venv .venv && .venv/bin/pip install -e ".[dev]")
TEXTE
exit 1
