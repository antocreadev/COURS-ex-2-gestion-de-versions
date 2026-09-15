"""Tests du module tpgit.notes."""

import pytest

from tpgit.notes import NoteInvalideError, est_admis, mention, moyenne, moyenne_ponderee


class TestMoyenne:
    def test_moyenne_simple(self):
        assert moyenne([12, 14, 10]) == pytest.approx(12.0)

    def test_moyenne_une_seule_note(self):
        assert moyenne([15.5]) == pytest.approx(15.5)

    def test_moyenne_liste_vide_leve_une_erreur(self):
        with pytest.raises(ValueError, match="vide"):
            moyenne([])

    @pytest.mark.parametrize("note", [-0.1, 20.1, 100])
    def test_note_hors_bareme_leve_une_erreur(self, note):
        with pytest.raises(NoteInvalideError, match="hors barème"):
            moyenne([note])


class TestMoyennePonderee:
    def test_ponderation_simple(self):
        assert moyenne_ponderee([10, 20], [1, 3]) == pytest.approx(17.5)

    def test_coefficients_egaux_equivaut_a_la_moyenne(self):
        notes = [8, 12, 16]
        assert moyenne_ponderee(notes, [2, 2, 2]) == pytest.approx(moyenne(notes))

    def test_longueurs_differentes(self):
        with pytest.raises(ValueError, match="longueurs différentes"):
            moyenne_ponderee([10, 12], [1])

    @pytest.mark.parametrize("coefficients", [[0, 1], [-1, 2]])
    def test_coefficient_non_strictement_positif(self, coefficients):
        with pytest.raises(ValueError, match="strictement positifs"):
            moyenne_ponderee([10, 12], coefficients)


class TestMention:
    @pytest.mark.parametrize(
        ("valeur", "attendu"),
        [
            (0, "Insuffisant"),
            (9.99, "Insuffisant"),
            (10, "Passable"),
            (11.99, "Passable"),
            (12, "Assez bien"),
            (13.99, "Assez bien"),
            (14, "Bien"),
            (15.99, "Bien"),
            (16, "Très bien"),
            (20, "Très bien"),
        ],
    )
    def test_bornes_des_mentions(self, valeur, attendu):
        assert mention(valeur) == attendu

    def test_mention_hors_bareme(self):
        with pytest.raises(NoteInvalideError):
            mention(21)


class TestEstAdmis:
    @pytest.mark.parametrize(("valeur", "attendu"), [(9.99, False), (10.0, True), (18, True)])
    def test_seuil_par_defaut(self, valeur, attendu):
        assert est_admis(valeur) is attendu

    def test_seuil_personnalise(self):
        assert est_admis(11, seuil=12) is False
