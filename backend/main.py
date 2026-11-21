
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

app = FastAPI(title="Analisador de Sentimento - Dataset Próprio HF")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextoRequest(BaseModel):
    texto: str

class AnaliseSentimento(BaseModel):
    sentimento: str
    confianca: float
    emocoes_detectadas: list[str]
    resumo_motivo: str

print("⏳ Baixando seu dataset do Hugging Face...")

NOME_DO_DATASET = "Zaza2isa/portfolio-reviews-dataset"
dataset = load_dataset(NOME_DO_DATASET)

dados_treino = dataset['train']

COLUNA_TEXTO = "review_text"       
COLUNA_CATEGORIA = "sentiment" 

textos = dados_treino[COLUNA_TEXTO]
categorias = dados_treino[COLUNA_CATEGORIA]

print("🧠 Treinando o modelo com os seus dados...")
modelo_ia = make_pipeline(TfidfVectorizer(), LogisticRegression(max_iter=1000))
modelo_ia.fit(textos, categorias)
print("✅ Modelo treinado e pronto para uso!")
# ----------------------------------------------------

@app.post("/analisar", response_model=AnaliseSentimento)
async def analisar_texto(request: TextoRequest):
    if not request.texto.strip():
        raise HTTPException(status_code=400, detail="O texto não pode estar vazio.")

    try:
        predicao = modelo_ia.predict([request.texto])[0]
        
        probabilidades = modelo_ia.predict_proba([request.texto])[0]
        maior_confianca = float(max(probabilidades))

        predicao_str = str(predicao)
        if "positiv" in predicao_str.lower():
            emocoes = ["satisfação", "alegria"]
        elif "negativ" in predicao_str.lower():
            emocoes = ["frustração", "insatisfação"]
        else:
            emocoes = ["imparcialidade", "neutralidade"]

        return AnaliseSentimento(
            sentimento=predicao_str,
            confianca=round(maior_confianca, 2),
            emocoes_detectadas=emocoes,
            resumo_motivo=f"Classificado como '{predicao_str}' utilizando modelo treinado no dataset {NOME_DO_DATASET}."
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar previsão: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
