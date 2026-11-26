"use client";

import { useEffect, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

type Resumo = {
  processos: number;
  tribunais: number;
  acordaos: number;
  ultima_coleta: string | null;
};

export default function KpiCards() {
  const [resumo, setResumo] = useState<Resumo | null>(null);

  useEffect(() => {
    fetch(`${API}/resumo`)
      .then((r) => r.json())
      .then(setResumo)
      .catch(() => setResumo(null));
  }, []);

  const cartoes = [
    { rotulo: "Processos coletados", valor: resumo?.processos },
    { rotulo: "Tribunais estaduais", valor: resumo?.tribunais },
    { rotulo: "Acórdãos do STJ citando a LGPD", valor: resumo?.acordaos },
    { rotulo: "Última coleta", valor: resumo?.ultima_coleta ?? "-" },
  ];

  return (
    <div className="mt-8 grid grid-cols-2 gap-4 md:grid-cols-4">
      {cartoes.map((cartao) => (
        <div
          key={cartao.rotulo}
          className="rounded-xl border border-gray-800 bg-gray-900/40 p-4"
        >
          <p className="text-3xl font-bold text-blue-500">
            {cartao.valor ?? "..."}
          </p>
          <p className="mt-1 text-xs text-gray-400">{cartao.rotulo}</p>
        </div>
      ))}
    </div>
  );
}