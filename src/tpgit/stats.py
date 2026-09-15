"""Statistiques descriptives sur une série de notes."""

import math
from collections.abc import Sequence
from dataclasses import dataclass

from tpgit.notes import moyenne


@dataclass(frozen=True)
class Resume:
    """Synthèse statistique d'une série de notes.

    Attributes:
        effectif: Nombre de notes.
        moyenne: Moyenne arithmétique.
        mediane: Valeur médiane.
        ecart_type: Écart-type de la population.
        minimum: Note la plus basse.
        maximum: Note la plus haute.
    """

    effectif: int
    moyenne: float
    mediane: float
    ecart_type: float
    minimum: float
    maximum: float


def mediane(valeurs: Sequence[float]) -> float:
    """Calcule la médiane d'une série.

    Args:
        valeurs: Les valeurs à analyser.

    Returns:
        La médiane : la valeur centrale, ou la moyenne des deux valeurs
        centrales si l'effectif est pair.

    Raises:
        ValueError: Si la série est vide.

    Examples:
        >>> mediane([3, 1, 2])
        2.0
    """
    if not valeurs:
        raise ValueError("La série est vide.")
    triees = sorted(valeurs)
    milieu = len(triees) // 2
    if len(triees) % 2 == 1:
        return float(triees[milieu])
    return (triees[milieu - 1] + triees[milieu]) / 2


def etendue(valeurs: Sequence[float]) -> float:
    """Calcule l'étendue (maximum moins minimum) d'une série.

    Args:
        valeurs: Les valeurs à analyser.

    Returns:
        L'écart entre la plus grande et la plus petite valeur.

    Raises:
        ValueError: Si la série est vide.

    Examples:
        >>> etendue([4, 18, 11])
        14.0
    """
    if not valeurs:
        raise ValueError("La série est vide.")
    return float(max(valeurs) - min(valeurs))


def ecart_type(valeurs: Sequence[float]) -> float:
    """Calcule l'écart-type de la population.

    Args:
        valeurs: Les valeurs à analyser.

    Returns:
        La racine carrée de la variance.

    Raises:
        ValueError: Si la série est vide.

    Examples:
        >>> ecart_type([10, 10, 10])
        0.0
    """
    if not valeurs:
        raise ValueError("La série est vide.")
    centre = sum(valeurs) / len(valeurs)
    variance = sum((valeur - centre) ** 2 for valeur in valeurs) / len(valeurs)
    return math.sqrt(variance)


def resume(notes: Sequence[float]) -> Resume:
    """Produit la synthèse statistique complète d'une série de notes.

    Args:
        notes: Les notes, chacune comprise entre 0 et 20.

    Returns:
        Un objet :class:`Resume` immuable.

    Raises:
        ValueError: Si la série est vide.

    Examples:
        >>> resume([10, 14]).moyenne
        12.0
    """
    return Resume(
        effectif=len(notes),
        moyenne=moyenne(notes),
        mediane=mediane(notes),
        ecart_type=ecart_type(notes),
        minimum=float(min(notes)),
        maximum=float(max(notes)),
    )
