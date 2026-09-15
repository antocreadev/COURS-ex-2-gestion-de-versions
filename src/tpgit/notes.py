"""Calculs portant sur les notes d'un étudiant (barème français sur 20)."""

from collections.abc import Sequence

NOTE_MIN = 0.0
NOTE_MAX = 20.0
SEUIL_ADMISSION = 10.0


class NoteInvalideError(ValueError):
    """Levée lorsqu'une note sort de l'intervalle [0, 20]."""


def _valider(notes: Sequence[float]) -> None:
    """Vérifie qu'une série de notes est utilisable.

    Args:
        notes: Les notes à valider.

    Raises:
        ValueError: Si la série est vide.
        NoteInvalideError: Si une note sort de l'intervalle [0, 20].
    """
    if not notes:
        raise ValueError("La liste de notes est vide.")
    for note in notes:
        if not NOTE_MIN <= note <= NOTE_MAX:
            raise NoteInvalideError(f"Note hors barème : {note} (attendu entre 0 et 20).")


def moyenne(notes: Sequence[float]) -> float:
    """Calcule la moyenne arithmétique d'une série de notes.

    Args:
        notes: Les notes, chacune comprise entre 0 et 20.

    Returns:
        La moyenne, entre 0 et 20.

    Raises:
        ValueError: Si la liste est vide.

    Examples:
        >>> moyenne([12, 14, 10])
        12.0
    """
    _valider(notes)
    return sum(notes) / len(notes)


def moyenne_ponderee(notes: Sequence[float], coefficients: Sequence[float]) -> float:
    """Calcule la moyenne pondérée d'une série de notes.

    Args:
        notes: Les notes, chacune comprise entre 0 et 20.
        coefficients: Les coefficients, strictement positifs, de même longueur.

    Returns:
        La moyenne pondérée.

    Raises:
        ValueError: Si les longueurs diffèrent ou si la somme des coefficients est nulle.

    Examples:
        >>> moyenne_ponderee([10, 20], [1, 3])
        17.5
    """
    _valider(notes)
    if len(notes) != len(coefficients):
        raise ValueError(
            f"{len(notes)} note(s) pour {len(coefficients)} coefficient(s) : longueurs différentes."
        )
    if any(coefficient <= 0 for coefficient in coefficients):
        raise ValueError("Les coefficients doivent être strictement positifs.")
    total = sum(note * coefficient for note, coefficient in zip(notes, coefficients, strict=True))
    return total / sum(coefficients)


def mention(valeur: float) -> str:
    """Donne la mention correspondant à une moyenne.

    Args:
        valeur: La moyenne, entre 0 et 20.

    Returns:
        L'une des mentions : ``Insuffisant``, ``Passable``, ``Assez bien``,
        ``Bien`` ou ``Très bien``.

    Raises:
        NoteInvalideError: Si la moyenne sort de l'intervalle [0, 20].

    Examples:
        >>> mention(15.5)
        'Bien'
    """
    _valider([valeur])
    if valeur < 10:
        return "Insuffisant"
    if valeur < 12:
        return "Passable"
    if valeur < 14:
        return "Assez bien"
    if valeur < 16:
        return "Bien"
    return "Très bien"


def est_admis(valeur: float, seuil: float = SEUIL_ADMISSION) -> bool:
    """Indique si une moyenne atteint le seuil d'admission.

    Args:
        valeur: La moyenne obtenue.
        seuil: Le seuil d'admission (10 par défaut).

    Returns:
        ``True`` si la moyenne est supérieure ou égale au seuil.

    Examples:
        >>> est_admis(9.99)
        False
    """
    return valeur >= seuil
