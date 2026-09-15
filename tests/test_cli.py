"""Tests de l'interface en ligne de commande."""

import json

import pytest

from tpgit.cli import main


def test_moyenne_texte(capsys):
    code = main(["moyenne", "12", "14", "10"])
    sortie = capsys.readouterr().out
    assert code == 0
    assert "12.0/20" in sortie
    assert "Assez bien" in sortie


def test_moyenne_json(capsys):
    code = main(["moyenne", "10", "20", "--coefficients", "1", "3", "--json"])
    donnees = json.loads(capsys.readouterr().out)
    assert code == 0
    assert donnees == {"moyenne": 17.5, "mention": "Très bien", "admis": True}


def test_stats_json(capsys):
    code = main(["stats", "8", "12", "16", "--json"])
    donnees = json.loads(capsys.readouterr().out)
    assert code == 0
    assert donnees["effectif"] == 3
    assert donnees["moyenne"] == 12.0


def test_stats_texte(capsys):
    assert main(["stats", "10", "14"]) == 0
    assert "moyenne" in capsys.readouterr().out


def test_erreur_de_saisie_renvoie_code_1(capsys):
    code = main(["moyenne", "25"])
    assert code == 1
    assert "Erreur" in capsys.readouterr().err


def test_sans_sous_commande_quitte_en_erreur():
    with pytest.raises(SystemExit) as info:
        main([])
    assert info.value.code == 2
