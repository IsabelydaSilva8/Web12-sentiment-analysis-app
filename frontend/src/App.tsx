import { useState } from "react";

export interface ResultadoAnalise{
  sentimento: 'Positivo' | 'Neutro' | 'Negativo';
  confianca: number;
  emocoes_detectadas: string[];
  resumo_motivo: string;
}

export default function App(){
  const [texto, setTexto] = useState('');
  const [resultado, setResultado] = useState<ResultadoAnalise | null>(null);
  const [carregando, setCarregando] = useState(false);

  const handlAnalisar = async () => {
    if(!texto.trim()) return;
    setCarregando(true);
    setResultado(null);

    try{
        const response = await fetch('http://localhost:8000/analisar', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ texto }),
        });

        if (!response.ok){
          throw new Error(`Erro do servidor: ${response.status}`);
        }

        const data: ResultadoAnalise = await response.json();
        setResultado(data);
    }catch (error){
      console.error(error);
      alert('Falha ao analisar o sentimento. Verifique se o backend está rodando . ')
    }finally{
      setCarregando(false);
    }
  };

  return(
    <div>
      <textarea
        value={texto}
        onChange={(e) => setTexto(e.target.value)}
        placeholder="Digite a frase ou feedback do cliente para análise aqui..."
      />

      <button
        onClick={handlAnalisar}
        disabled={carregando || !texto.trim()}
      >
        {carregando ? 'Processando dados com AI...' : 'Analisar Sentimento'}
      </button>

      {resultado &&(
        <div>
          <h1>Resultado da Análise:</h1>
          <h3>Sentimento da Frase:</h3>
          <span>
            {resultado.sentimento}
          </span>
        </div>
      )}
    </div>
  )

}