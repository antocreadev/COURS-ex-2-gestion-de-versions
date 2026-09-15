# Mise en place — guide enseignant

## 1. Créer le dépôt modèle

```bash
gh repo create antocreadev/COURS-ex-2-gestion-de-versions --public --source=. --push
gh repo edit antocreadev/COURS-ex-2-gestion-de-versions --enable-discussions --template
```

L'option `--template` transforme le dépôt en **modèle** : chaque étudiant ou
binôme peut générer son propre dépôt avec un historique propre.

```bash
# côté étudiant
gh repo create mon-tp-git --template antocreadev/COURS-ex-2-gestion-de-versions --private --clone
```

### Deux organisations possibles

| Modèle | Avantage | Inconvénient |
|---|---|---|
| **Un dépôt par binôme** (via *template*) | chacun merge ses PR, moins de collisions | pas de collaboration entre binômes |
| **Un dépôt commun pour la promo** | vraies revues croisées, vrais conflits | il faut arbitrer les merges |

Recommandation : *template* pour le **TP 1**, dépôt commun pour les **TP 2 et 3**.

---

## 2. Ce qu'il reste éventuellement à adapter

Tout est déjà réglé pour `antocreadev/COURS-ex-2-gestion-de-versions`. Restent
deux détails facultatifs :

| Fichier | Quoi |
|---|---|
| `LICENSE` | le nom de l'établissement (ligne « Copyright ») |
| `.github/ISSUE_TEMPLATE/config.yml` | l'URL des Discussions — valide uniquement si vous les activez (`gh repo edit --enable-discussions`) |

Ajoutez les étudiants comme **collaborateurs** pour qu'ils puissent pousser des
branches et ouvrir des PR sur le dépôt commun :

```bash
gh api -X PUT repos/antocreadev/COURS-ex-2-gestion-de-versions/collaborators/LOGIN_ETUDIANT \
  -f permission=push
```

> `permission=push` (rôle *Write*) suffit : avec la protection de `main` du §3,
> ils pourront créer des branches et des PR, mais **pas** pousser sur `main`.
> Ne donnez pas `maintain` ou `admin`, qui permettent de contourner la
> protection.

---

## 3. Protéger `main`

C'est **indispensable** : sans cela, les étudiants pousseront directement sur
`main` et tout le dispositif pédagogique s'effondre.

> **Deux particularités des dépôts personnels** (par opposition aux dépôts
> d'organisation) :
>
> 1. **Vous ne pouvez pas approuver vos propres PR.** GitHub l'interdit. Si vous
>    laissez « Required approvals : 1 », vos propres PR de maintenance seront
>    bloquées. Deux solutions : vous exclure via *Bypass list* (vous restez
>    soumis à la CI, mais pas à la revue), ou faire approuver par un étudiant.
>    Les étudiants, eux, s'approuvent entre eux : la règle joue pleinement.
> 2. **La protection de branche n'est gratuite que sur un dépôt public.** Sur un
>    dépôt personnel privé, il faut GitHub Pro. Gardez le dépôt de cours
>    **public**.

Réglages → Branches → *Add branch ruleset* sur `main` :

- ☑️ Require a pull request before merging
  - Required approvals : **1**
  - ☑️ Dismiss stale approvals when new commits are pushed
  - ☐ Require review from Code Owners — **à laisser décoché** ici : le seul
    *code owner* du dépôt, c'est vous, et vous ne pouvez pas vous approuver
- ☑️ Require status checks to pass
  - checks requis : **`CI OK`** et **`Conventions de PR`**
  - ☑️ Require branches to be up to date before merging
- ☑️ Require conversation resolution before merging
- ☑️ Block force pushes
- *Bypass list* : vous seul, et uniquement si vous devez merger vos propres
  PR de maintenance. **Jamais** les étudiants.

Dans Réglages → General → Pull Requests :

- ☑️ Allow squash merging — *Default message : Pull request title*
- ☐ Allow merge commits
- ☐ Allow rebase merging
- ☑️ Automatically delete head branches

En ligne de commande :

```bash
gh api -X PUT repos/antocreadev/COURS-ex-2-gestion-de-versions/branches/main/protection \
  -f 'required_status_checks[strict]=true' \
  -f 'required_status_checks[contexts][]=CI OK' \
  -f 'required_status_checks[contexts][]=Conventions de PR' \
  -F 'enforce_admins=false' \
  -F 'required_pull_request_reviews[required_approving_review_count]=1' \
  -F 'required_pull_request_reviews[dismiss_stale_reviews]=true' \
  -F 'restrictions=null' \
  -F 'required_conversation_resolution=true' \
  -F 'allow_force_pushes=false'
```

---

## 4. Créer les issues de départ

```bash
./scripts/creer_issues.sh antocreadev/COURS-ex-2-gestion-de-versions
```

Le script crée les étiquettes puis une douzaine d'issues calibrées, de
*Facile* à *Difficile*, avec critères d'acceptation. Prévoyez **plus d'issues
que d'étudiants** pour qu'ils aient un vrai choix.

---

## 5. Déroulé conseillé

| Séance | Contenu | Livrable |
|---|---|---|
| **1** (2 h) | Démo du cycle au tableau, puis [TP 1](tp-01-premiere-contribution.md) | 1 PR mergée + 1 revue par étudiant |
| **2** (1 h) | [TP 2](tp-02-ci-rouge.md) — lire et corriger une CI rouge | tableau de synthèse |
| **3** (1 h 30) | [TP 3](tp-03-revue-et-conflits.md) — revue et conflits | PR fusionnée après conflit + débriefing |

### Points à marteler

1. **`main` est sacré.** Toute modification passe par une PR.
2. **La CI n'est pas un obstacle, c'est un filet.** Elle dit non *avant* que le
   bug atteigne les autres.
3. **Un hook n'est pas une sécurité** (contournable par `--no-verify`), la CI
   oui — elle tourne sur une machine que l'étudiant ne contrôle pas.
4. **Une revue n'est pas un jugement de personne.** On commente le code, pas
   l'auteur.
5. **Plus tôt l'erreur est détectée, moins elle coûte.** C'est toute la
   justification de l'échelle éditeur → hook → CI.

---

## 6. Évaluation

Éléments objectifs, vérifiables dans le dépôt :

```bash
# Historique des commits d'un étudiant
git log --author="Nom" --oneline

# PR ouvertes, mergées, et leur taille
gh pr list --state merged --author "login" --json number,title,additions,deletions

# Revues effectuées par un étudiant
gh api "search/issues?q=repo:antocreadev/COURS-ex-2-gestion-de-versions+reviewed-by:login+type:pr" --jq '.total_count'

# Taux d'échec de CI
gh run list --limit 100 --json conclusion --jq '[.[].conclusion] | group_by(.) | map({(.[0]): length}) | add'
```

Barème détaillé en fin de [TP 1](tp-01-premiere-contribution.md).

---

## 7. Extensions possibles

Le dépôt est conçu pour être enrichi progressivement.

| Thème | Piste |
|---|---|
| **Publication (CD)** | workflow `release.yml` déclenché sur un tag, build + publication sur TestPyPI |
| **Sémantique de version** | `release-please` ou `commitizen` — montre l'intérêt réel des Conventional Commits |
| **Sécurité** | `pip-audit`, CodeQL, `gitleaks` en hook et en CI |
| **Qualité** | badge de couverture, `--cov-fail-under` progressif, mutation testing (`mutmut`) |
| **Conteneurs** | `Dockerfile` + build dans la CI + cache de couches |
| **Performance de CI** | mesurer le temps des jobs, jouer sur le cache, `paths-ignore` |
| **Environnements** | `environment:` GitHub + approbation manuelle avant déploiement |
| **Autres hooks** | `prepare-commit-msg` qui préremplit le type depuis le nom de branche |
