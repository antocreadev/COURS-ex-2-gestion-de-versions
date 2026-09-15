"""Petite bibliothèque de calcul de notes, support du TP « cycle de contribution ».

Le code métier est volontairement simple : l'objectif du TP n'est pas
l'algorithmique, mais le *processus* (branche, commit, PR, CI, revue, merge).
"""

from tpgit.notes import est_admis, mention, moyenne, moyenne_ponderee
from tpgit.stats import ecart_type, etendue, mediane, resume

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "ecart_type",
    "est_admis",
    "etendue",
    "mediane",
    "mention",
    "moyenne",
    "moyenne_ponderee",
    "resume",
]
