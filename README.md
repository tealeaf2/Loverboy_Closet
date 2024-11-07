# Loverboy_Closet

LoverboyCloset is a personalized fashion assistant designed to help users manage and organize their wardrobe while offering recommendations for occasions. Users can input their clothes into digital closets, categorize them, and create outfits based on preferences, trends, and occasion.

## Getting Started

### Prerequisites

- Nodeenv
- Node (Npm)
- Python

### Sample folder structure

```sh
loverboy_closet
├── backend
├── deploy.sh
├── flask-env
├── frontend
├── README.md
├── requirements-local.txt
└── requirements-prod.txt
```

### Installation/Setup for development

1. Clone the repo

```sh
https://github.com/tealeaf2/loverboy_closet.git
```

#### Frontend

2. Create a node environment and activate it

```sh
nodeenv --node=18.18.0 vue-nenv
source vue-nenv/bin/activate
```

3. Install node packages if not installed
```sh
cd frontend
npm install
```

4. Run `frontend` on reload
```sh
npm run dev
```

#### Backend

5. Open another shell session and create a python environment and install all dependencies required in `requirements.txt`
```sh
python -m venv flask-env
source flask-env/bin/activate
pip install -r requirements-local.txt
```

6. Go into `backend` folder, initialize database, and start flask
```sh
cd backend
python init_db.py
python app.py
```