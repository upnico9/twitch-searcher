# Twitch Video Searcher

Application web permettant de rechercher des vidéos Twitch par jeu et de les filtrer selon différents critères (langue, période, popularité).

## 🚀 Technologies utilisées

### Frontend
- Vue.js 3
- TypeScript
- Naive UI

### Backend
- FastAPI
- MongoDB
- Python 3.8+
- Twitch API

## 📋 Prérequis

1. Python 3.8 ou supérieur
2. Node.js 18 ou supérieur
3. MongoDB
4. Un compte développeur Twitch avec Client ID et Secret
5. pnpm (pour le frontend)

## ⚙️ Installation

### 1. Cloner le projet
```bash
git clone https://github.com/upnico9/twitch-searcher.git
cd twitch-searcher
```

### 2. Configuration du Backend

1. Créer un environnement virtuel Python et l'activer :
```bash
cd backend
python -m venv venv
# Sur macOS/Linux
source venv/bin/activate
# Sur Windows
.\venv\Scripts\activate
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurer les variables d'environnement :
```bash
cp .env.example .env
```
Puis modifier le fichier `.env` avec vos identifiants Twitch :
```
TWITCH_CLIENT_ID=votre_client_id
TWITCH_CLIENT_SECRET=votre_client_secret
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=twitch_search
```

### 3. Configuration du Frontend

1. Installer les dépendances :
```bash
cd frontend
pnpm install
```

## 🚀 Lancement de l'application

1. Démarrer MongoDB :
```bash
# Si MongoDB n'est pas démarré en service
mongod
```

2. Démarrer le backend (depuis le dossier backend) :
```bash
# Avec l'environnement virtuel activé
uvicorn app.main:app --reload
```
Le backend sera accessible sur http://localhost:8000
Documentation API disponible sur http://localhost:8000/docs

3. Démarrer le frontend (depuis le dossier frontend) :
```bash
pnpm dev
```
L'application sera accessible sur http://localhost:5173

## 🎮 Utilisation

1. Accédez à http://localhost:5173
2. Utilisez la barre de recherche pour chercher un jeu
3. Sélectionnez un jeu dans les suggestions
4. Appliquez des filtres si nécessaire (langue, période, tri)
5. Les vidéos s'afficheront en grille avec les informations principales
6. Cliquez sur une vidéo pour la lire dans le lecteur intégré
7. Cliquez sur le bouton pour activer/desactiver la sauvegarde des nouvelles videos toutes les deux minutes

## 🔍 Fonctionnalités

- Recherche autocomplétée des jeux
- Filtrage par langue
- Tri par temps, tendance ou vues
- Filtrage par période (jour, semaine, mois, tout)
- Actualisation et sauvegarde automatique des résultats
- Sauvegarde des vidéos en base de données
- Lecteur vidéo intégré

## 🔧 Structure du projet

```
twitch-searcher/
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── api/         # Routes API
│   │   ├── core/        # Configuration et gestion des erreurs
│   │   ├── db/          # Configuration MongoDB
│   │   ├── models/      # Modèles de données
│   │   └── services/    # Services (Twitch, MongoDB)
│   └── requirements.txt
└── frontend/            # Application Vue.js
    ├── src/
    │   ├── api/        # Client API
    │   ├── components/ # Composants Vue
    │   └── types.ts    # Types TypeScript
    └── package.json
```
