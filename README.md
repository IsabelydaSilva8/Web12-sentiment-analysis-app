#  Análise de Sentimentos Full-Stack

Aplicação web full-stack para classificação de sentimentos em avaliações de portfólio/produtos. O modelo de Machine Learning foi treinado com um dataset autoral publicado no Hugging Face e integrado a uma API de alta performance com interface moderna.

# Tecnologias Utilizadas
*******Backend
* FastApi
* Python
* Uvicorn
* Scikit-learn
* Hugging Face Datasets (`portfolio-reviews-dataset`)

******Frontend
* React
* TypeScript
* Vite

# Configurando o Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Configurando o Frontend (React + Vite)
```bash
cd frontend
npm install
npm run dev
```
