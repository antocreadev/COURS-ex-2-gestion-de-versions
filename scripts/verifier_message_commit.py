#!/usr/bin/env python3
"""Hook ``commit-msg`` : valide le format Conventional Commits.

Appelé automatiquement par Git avec, en argument, le chemin du fichier
contenant le message de commit en cours de rédaction.

Code de sortie ``0`` = message accepté, ``1`` = commit refusé.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

TYPES = (
    "feat",
    "fix",
    "docs",
    "style",
    "refactor",
    "perf",
    "test",
    "build",
    "ci",
    "chore",
    "revert",
)

LONGUEUR_MAX = 72

MOTIF = re.compile(
    r"^(?P<type>" + "|".join(TYPES) + r")"
    r"(?:\((?P<portee>[a-z0-9._\-/]+)\))?"
    r"(?P<rupture>!)?"
    r": (?P<description>.+)$"
)

# Messages générés par Git lui-même : on ne les valide pas.
PREFIXES_IGNORES = ("Merge ", "Revert ", "fixup! ", "squash! ")

ROUGE = "\033[31m"
VERT = "\033[32m"
JAUNE = "\033[33m"
GRAS = "\033[1m"
FIN = "\033[0m"


def refuser(probleme: str, sujet: str) -> int:
    """Affiche une explication lisible puis refuse le commit.

    Args:
        probleme: La raison du refus.
        sujet: La première ligne du message fourni.

    Returns:
        Toujours ``1``, à renvoyer comme code de sortie.
    """
    print(f"\n{ROUGE}{GRAS}✖ Message de commit refusé{FIN}\n")
    print(f"  {GRAS}Reçu   :{FIN} {sujet or '(vide)'}")
    print(f"  {GRAS}Raison :{FIN} {probleme}\n")
    print(f"  {GRAS}Format attendu{FIN} (Conventional Commits) :")
    print(f"    {JAUNE}<type>(<portée facultative>): <description>{FIN}\n")
    print(f"  {GRAS}Types autorisés :{FIN} {', '.join(TYPES)}\n")
    print(f"  {GRAS}Exemples valides :{FIN}")
    print(f"    {VERT}feat(stats): ajoute le calcul de la médiane{FIN}")
    print(f"    {VERT}fix(notes): rejette les coefficients négatifs{FIN}")
    print(f"    {VERT}docs: complète la section installation du README{FIN}\n")
    print(f"  {GRAS}Pour corriger le dernier message :{FIN} git commit --amend\n")
    return 1


def valider(message: str) -> int:
    """Valide un message de commit complet.

    Args:
        message: Le contenu brut du fichier de message.

    Returns:
        ``0`` si le message est conforme, ``1`` sinon.
    """
    lignes = [ligne for ligne in message.splitlines() if not ligne.startswith("#")]
    sujet = lignes[0].strip() if lignes else ""

    if sujet.startswith(PREFIXES_IGNORES):
        return 0

    if not sujet:
        return refuser("le message est vide.", sujet)

    correspondance = MOTIF.match(sujet)
    if correspondance is None:
        return refuser(
            "la première ligne ne suit pas le format « type: description ».",
            sujet,
        )

    if len(sujet) > LONGUEUR_MAX:
        return refuser(
            f"la première ligne fait {len(sujet)} caractères (maximum {LONGUEUR_MAX}). "
            "Mettez les détails dans le corps du message, après une ligne vide.",
            sujet,
        )

    description = correspondance.group("description")
    if description[0].isupper():
        return refuser("la description doit commencer par une minuscule.", sujet)
    if description.endswith("."):
        return refuser("la description ne doit pas se terminer par un point.", sujet)

    if len(lignes) > 1 and lignes[1].strip():
        return refuser("il manque une ligne vide entre le sujet et le corps du message.", sujet)

    return 0


def main(argv: list[str]) -> int:
    """Point d'entrée du hook.

    Args:
        argv: Les arguments, dont le premier est le chemin du fichier de message.

    Returns:
        Le code de sortie du hook.
    """
    if not argv:
        print("Usage : verifier_message_commit.py <fichier-de-message>", file=sys.stderr)
        return 1
    return valider(Path(argv[0]).read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
