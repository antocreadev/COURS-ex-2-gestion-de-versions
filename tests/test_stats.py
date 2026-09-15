"""Tests du module tpgit.stats."""

import pytest

from tpgit.stats import Resume, ecart_type, etendue, mediane, resume


class TestMediane:
    def test_effectif_impair(self):
        assert mediane([3, 1, 2]) == pytest.approx(2.0)

    def test_effectif_pair(self):
        assert mediane([1, 2, 3, 4]) == pytest.approx(2.5)

    def test_serie_vide(self):
        with pytest.raises(ValueError, match="vide"):
            mediane([])


class TestEtendue:
    def test_etendue_simple(self):
        assert etendue([4, 18, 11]) == pytest.approx(14.0)

    def test_valeurs_identiques(self):
        assert etendue([10, 10]) == pytest.approx(0.0)

    def test_serie_vide(self):
        with pytest.raises(ValueError, match="vide"):
            etendue([])


class TestEcartType:
    def test_serie_constante(self):
        assert ecart_type([10, 10, 10]) == pytest.approx(0.0)

    def test_valeur_connue(self):
        assert ecart_type([2, 4, 4, 4, 5, 5, 7, 9]) == pytest.approx(2.0)

    def test_serie_vide(self):
        with pytest.raises(ValueError, match="vide"):
            ecart_type([])


class TestResume:
    def test_champs_du_resume(self):
        synthese = resume([8, 12, 16])
        assert isinstance(synthese, Resume)
        assert synthese.effectif == 3
        assert synthese.moyenne == pytest.approx(12.0)
        assert synthese.mediane == pytest.approx(12.0)
        assert synthese.minimum == pytest.approx(8.0)
        assert synthese.maximum == pytest.approx(16.0)

    def test_resume_est_immuable(self):
        synthese = resume([10, 12])
        with pytest.raises(AttributeError):
            synthese.moyenne = 20  # type: ignore[misc]

    def test_serie_vide(self):
        with pytest.raises(ValueError, match="vide"):
            resume([])
