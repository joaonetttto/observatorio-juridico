"use client";

import { useState } from "react";

const API = "http://127.0.0.1:8000";

type Resultado = {
  id_stj: string;
  orgao_julgador: string;
  classe: string;
  data: string;
  trecho: string;
};

function Destaque({ texto }: { texto: string }) {
  const partes = texto.split(/(<<.*?>>)/g);
  return (
    <>
      {partes.map((parte, indice) =>
        parte.startsWith("<<") ? (
          <mark key={indice} className="bg-yellow-300 px-0.5 text-black">
            {parte.slice(2, -2)}
          </mark>
        ) : (
          <span key={indice}>{parte}</span>
        ),
      )}
    </>
  );
}

export default function BuscaAcordaos() {
  const [termo, setTermo] = useState("");
  const [resultados, setResultados] = useState<Resultado[] | null>(null);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState(false);

  async function buscar() {
    if (termo.trim().length < 2) return;
    setCarregando(true);
    setErro(false);
    try {
      const resposta = await fetch(
        `${API}/acordaos-busca?q=${encodeURIComponent(termo.trim())}`,
      );
      if (!resposta.ok) throw new Error("falhou");
      setResultados(await resposta.json());
    } catch {
      setErro(true);
      setResultados(null);
    } finally {
      setCarregando(false);
    }
  }

  return (
    <section className="mt-8 rounded-xl border border-gray-800 bg-gray-900/40 p-6">
      <h2 className="text-2xl font-bold">Buscar nas ementas</h2>
      <p className="mt-2 text-sm text-gray-500">
        Pesquisa nas ementas dos acórdãos do STJ que citam a LGPD. Digite as
        palavras com acento (por exemplo: indenização). Use aspas para uma
        expressão exata e o sinal de menos para excluir uma palavra.
      </p>

      <div className="mt-4 flex gap-2">
        <input
          value={termo}
          onChange={(evento) => setTermo(evento.target.value)}
          onKeyDown={(evento) => {
            if (evento.key === "Enter") buscar();
          }}
          placeholder="ex.: vazamento, cadastro positivo, dano moral"
          className="flex-1 rounded border border-gray-700 bg-transparent px-3 py-2 text-sm"
        />
        <button
          onClick={buscar}
          disabled={carregando}
          className="rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
        >
          {carregando ? "Buscando..." : "Buscar"}
        </button>
      </div>

      {erro && (
        <p className="mt-4 text-sm text-red-600">
          Não consegui buscar. A API está ligada?
        </p>
      )}

      {resultados && resultados.length === 0 && (
        <p className="mt-4 text-sm text-gray-500">
          Nenhum acórdão encontrado para esse termo.
        </p>
      )}

      {resultados && resultados.length > 0 && (
        <ul className="mt-6 space-y-4">
          {resultados.map((acordao) => (
            <li
              key={acordao.id_stj}
              className="rounded border border-gray-800 p-4 text-sm"
            >
              <p className="font-medium">
                {acordao.classe}{" "}
                <span className="text-gray-500">
                  · {acordao.orgao_julgador} · {acordao.data}
                </span>
              </p>
              <p className="mt-2 text-gray-400">
                ...
                <Destaque texto={acordao.trecho} />
                ...
              </p>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}