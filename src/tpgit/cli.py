"""Interface en ligne de commande du projet.

Exemples d'utilisation::

    tpgit moyenne 12 14 8
    tpgit moyenne 10 20 --coefficients 1 3
    tpgit stats 12 14 8 16 --json
"""

import argparse
import json
import sys
from collections.abc import Sequence
from dataclasses import asdict

from tpgit import __version__
from tpgit.notes import est_admis, mention, moyenne, moyenne_ponderee
from tpgit.stats import resume


def construire_parseur() -> argparse.ArgumentParser:
    """Construit le parseur d'arguments de la commande ``tpgit``.

    Returns:
        Le parseur configuré, avec ses sous-commandes.
    """
    parseur = argparse.ArgumentParser(
        prog="tpgit",
        description="Outils de calcul de notes (support du TP cycle de contribution).",
    )
    parseur.add_argument("--version", action="version", version=f"tpgit {__version__}")
    sous_commandes = parseur.add_subparsers(dest="commande", required=True)

    p_moyenne = sous_commandes.add_parser("moyenne", help="Calcule la moyenne d'une série de notes")
    p_moyenne.add_argument("notes", type=float, nargs="+", help="Notes entre 0 et 20")
    p_moyenne.add_argument(
        "--coefficients",
        type=float,
        nargs="+",
        default=None,
        help="Coefficients associés aux notes (moyenne pondérée)",
    )
    p_moyenne.add_argument("--json", action="store_true", help="Sortie au format JSON")

    p_stats = sous_commandes.add_parser("stats", help="Affiche la synthèse statistique")
    p_stats.add_argument("notes", type=float, nargs="+", help="Notes entre 0 et 20")
    p_stats.add_argument("--json", action="store_true", help="Sortie au format JSON")

    return parseur


def _commande_moyenne(args: argparse.Namespace) -> str:
    """Exécute la sous-commande ``moyenne``.

    Args:
        args: Les arguments analysés.

    Returns:
        Le texte à afficher.
    """
    valeur = (
        moyenne_ponderee(args.notes, args.coefficients)
        if args.coefficients
        else moyenne(args.notes)
    )
    donnees = {
        "moyenne": round(valeur, 2),
        "mention": mention(valeur),
        "admis": est_admis(valeur),
    }
    if args.json:
        return json.dumps(donnees, ensure_ascii=False)
    statut = "admis" if donnees["admis"] else "ajourné"
    return f"Moyenne : {donnees['moyenne']}/20 — {donnees['mention']} ({statut})"


def _commande_stats(args: argparse.Namespace) -> str:
    """Exécute la sous-commande ``stats``.

    Args:
        args: Les arguments analysés.

    Returns:
        Le texte à afficher.
    """
    synthese = resume(args.notes)
    donnees = {
        cle: round(val, 2) if isinstance(val, float) else val
        for cle, val in asdict(synthese).items()
    }
    if args.json:
        return json.dumps(donnees, ensure_ascii=False)
    return "\n".join(f"{cle:<10} : {valeur}" for cle, valeur in donnees.items())


def main(argv: Sequence[str] | None = None) -> int:
    """Point d'entrée de la commande ``tpgit``.

    Args:
        argv: Les arguments de la ligne de commande (``sys.argv[1:]`` par défaut).

    Returns:
        Le code de sortie : ``0`` en cas de succès, ``1`` en cas d'erreur de saisie.
    """
    parseur = construire_parseur()
    args = parseur.parse_args(argv)

    actions = {"moyenne": _commande_moyenne, "stats": _commande_stats}
    try:
        sortie = actions[args.commande](args)
    except ValueError as erreur:
        print(f"Erreur : {erreur}", file=sys.stderr)
        return 1
    print(sortie)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
