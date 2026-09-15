# Mise en place — guide enseignant

## 1. Le principe

Ce dépôt est un **point de départ**, pas un espace de travail partagé. Les
étudiants le clonent, puis en font **leur propre dépôt** sur leur compte. Tout
le cycle (branches, PR, CI, revues, merges) se déroule chez eux.

```
  antocreadev/COURS-ex-2-gestion-de-versions     ← vous, en lecture seule pour tous
                     │
          git clone  │
                     ▼
        clone local d'un binôme
                     │
   ./scripts/creer-mon-depot.sh
                     ▼
  etudiant-a/tp-gestion-de-versions              ← leur terrain : PR, CI, revues
        (etudiant-b ajouté en collaborateur)
```

**Pourquoi pas un dépôt commun à la promo ?** Parce que 30 étudiants qui ouvrent
des PR sur le même `main` passent leur temps en conflits d'intégration et
attendent votre merge. Un dépôt par binôme leur donne l'autonomie complète :
ils configurent la protection, ils relisent, ils mergent. Vous, vous relisez le
résultat.

**Pourquoi pas un fork ?** Un fork marcherait, mais il place les PR *chez vous*,
donc c'est vous qui mergez tout, et la CI d'un fork de première contribution
demande une validation manuelle à chaque push. Trop de friction pour un TP.

### Ce que l'étudiant lance

```bash
git clone https://github.com/antocreadev/COURS-ex-2-gestion-de-versions.git tp-gestion-de-versions
cd tp-gestion-de-versions
gh auth login
./scripts/creer-mon-depot.sh tp-gestion-de-versions LOGIN_DU_BINOME
```

[`scripts/creer-mon-depot.sh`](../scripts/creer-mon-depot.sh) enchaîne : renommage
de `origin` en `depart`, création du dépôt public, push, ajout du binôme en
collaborateur, réglage des PR en *squash only*, protection de `main`, puis
création des étiquettes et des 13 issues.

> Le script est volontairement lisible et commenté : c'est aussi un support de
> cours sur l'API GitHub. Faites-le lire avant de le lancer.

---

## 2. Votre travail de préparation

Le dépôt est déjà configuré pour `antocreadev/COURS-ex-2-gestion-de-versions`.
Il reste :

```bash
# publier le dépôt de cours
gh repo create antocreadev/COURS-ex-2-gestion-de-versions --public --source=. --push
```

| Optionnel | Quoi |
|---|---|
| `LICENSE` | le nom de l'établissement (ligne « Copyright ») |
| `.github/ISSUE_TEMPLATE/config.yml` | l'URL des Discussions, si vous les activez (`gh repo edit --enable-discussions`) |
| `.github/CODEOWNERS` | contient `@antocreadev` ; sur le dépôt d'un étudiant, cette ligne est simplement ignorée (vous n'y êtes pas collaborateur). Les faire l'adapter à leur binôme est un bon échauffement de PR. |

Pensez à vous faire ajouter en collaborateur (lecture) sur les dépôts des
binômes pour pouvoir suivre et noter :

```bash
gh api -X PUT repos/ETUDIANT/tp-gestion-de-versions/collaborators/antocreadev \
  -f permission=pull
```

Sur **votre** dépôt de cours, protégez aussi `main` — pour l'exemple, et pour
éviter une bêtise en direct :

```bash
gh api -X PUT repos/antocreadev/COURS-ex-2-gestion-de-versions/branches/main/protection \
  -F 'required_status_checks[strict]=true' \
  -f 'required_status_checks[contexts][]=CI OK' \
  -F 'required_pull_request_reviews[required_approving_review_count]=0' \
  -F 'enforce_admins=false' -F 'allow_force_pushes=false' -F 'restrictions=null'
```

> `required_approving_review_count=0` chez vous : GitHub interdit d'approuver
> ses propres PR, vous seriez sinon bloqué sur vos propres corrections. La CI
> reste obligatoire, c'est l'essentiel.

---

## 3. La protection de `main` chez les étudiants

Le script l'applique automatiquement. Voici ce qu'il règle, à savoir expliquer
au tableau — et à vérifier si un binôme a fait la manipulation à la main
(Settings → Branches → *Add branch ruleset*) :

- ☑️ Require a pull request before merging
  - Required approvals : **1** *(0 si le binôme n'a pas été ajouté — on ne peut
    pas approuver sa propre PR)*
  - ☑️ Dismiss stale approvals when new commits are pushed
  - ☐ Require review from Code Owners — inutile ici
- ☑️ Require status checks to pass
  - checks requis : **`CI OK`** et **`Conventions de PR`**
  - ☑️ Require branches to be up to date before merging
- ☑️ Require conversation resolution before merging
- ☑️ Block force pushes
- ☐ Allow bypass — décoché

Dans Settings → General → Pull Requests :

- ☑️ Allow squash merging — *Default message : Pull request title*
- ☐ Allow merge commits · ☐ Allow rebase merging
- ☑️ Automatically delete head branches

### Deux pièges des dépôts personnels

1. **On ne peut pas approuver sa propre PR.** D'où l'intérêt du binôme : sans
   lui, « 1 approbation requise » bloque tout. C'est aussi ce qui force une
   vraie revue croisée plutôt qu'un auto-merge.
2. **La protection de branche n'est gratuite que sur un dépôt public.** Sur un
   dépôt personnel privé il faut GitHub Pro (gratuit avec
   [GitHub Education](https://education.github.com)). Le plus simple : dépôts
   **publics**.

### Vérifier qu'un binôme a bien tout configuré

```bash
gh api repos/ETUDIANT/tp-gestion-de-versions/branches/main/protection \
  --jq '{checks: .required_status_checks.contexts,
         approbations: .required_pull_request_reviews.required_approving_review_count,
         force_push: .allow_force_pushes.enabled}'
```

---

## 4. Les issues de départ

[`scripts/creer_issues.sh`](../scripts/creer_issues.sh) crée 10 étiquettes et
**13 issues** calibrées *facile / moyenne / difficile*, chacune avec ses critères
d'acceptation. Il est appelé automatiquement par `creer-mon-depot.sh`, donc
**chaque binôme démarre avec ses propres issues** — vous n'avez rien à faire.

Pour le relancer seul sur un dépôt (ajout d'issues en cours de TP, ou binôme
ayant fait la configuration à la main) :

```bash
./scripts/creer_issues.sh ETUDIANT/tp-gestion-de-versions
```

13 issues pour un binôme, c'est volontairement large : ils doivent **choisir**,
et il doit rester du travail pour les plus rapides. Pour ajouter les vôtres,
éditez la fonction `issue` en fin de script — le modèle de critères
d'acceptation est partagé.

---

## 5. Déroulé conseillé

| Séance | Contenu | Livrable |
|---|---|---|
| **1** (2 h 15) | Démo du cycle au tableau, puis [TP 1](tp-01-premiere-contribution.md) | dépôt créé + 2 PR mergées + 1 revue par étudiant |
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

Chaque binôme a son dépôt : demandez-leur de rendre simplement **l'URL**. Tout
est ensuite vérifiable en ligne de commande, sans cloner.

```bash
DEPOT=ETUDIANT/tp-gestion-de-versions

# Les PR mergées, leur auteur et leur taille
gh pr list --repo "$DEPOT" --state merged \
  --json number,title,author,additions,deletions,mergedAt \
  --jq '.[] | "\(.number)\t\(.author.login)\t+\(.additions)/-\(.deletions)\t\(.title)"'

# Les titres suivent-ils Conventional Commits ?
gh pr list --repo "$DEPOT" --state merged --json title --jq '.[].title' \
  | grep -vE '^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?!?: ' \
  || echo "tous conformes"

# Qui a relu quoi ? (le cœur de la note)
gh api "search/issues?q=repo:$DEPOT+reviewed-by:LOGIN+type:pr" --jq .total_count

# Les PR ont-elles vraiment reçu des commentaires de fond ?
gh pr view NUMERO --repo "$DEPOT" --json reviews,comments \
  --jq '{revues: [.reviews[] | {qui: .author.login, etat: .state}], commentaires: (.comments | length)}'

# Rapport CI : combien d'échecs, et ont-ils été corrigés ?
gh run list --repo "$DEPOT" --limit 100 --json conclusion \
  --jq '[.[].conclusion] | group_by(.) | map({(.[0]): length}) | add'

# main a-t-il bien été protégé ? (ou ont-ils poussé dessus en direct ?)
gh api "repos/$DEPOT/commits?sha=main" --jq 'length'
gh api "repos/$DEPOT/branches/main/protection" --jq '.required_pull_request_reviews != null'

# L'historique de main : une ligne par PR, ou du grand n'importe quoi ?
gh api "repos/$DEPOT/commits?sha=main&per_page=30" --jq '.[].commit.message | split("\n")[0]'
```

> Le dernier point est le plus parlant : un `main` dont chaque commit est un
> titre de PR lisible signifie que tout le dispositif a été respecté. Un `main`
> avec « modif », « test2 », « ça marche » signifie qu'ils ont contourné.

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
