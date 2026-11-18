"use client";

import { useEffect, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const API = "http://127.0.0.1:8000";

type PorAno = { ano: number; quantidade: number };

export default function Home() {
  const [dados, setDados] = useState<PorAno[]>([]);
  const [erro, setErro] = useState(false);

  useEffect(() => {
    fetch(`${API}/processos-por-ano`)
      .then((resposta) => resposta.json())
      .then(setDados)
      .catch(() => setErro(true));
  }, []);

  return (
    <main className="mx-auto max-w-3xl p-8">
      <h1 className="text-3xl font-bold">Observatório Jurídico</h1>
      <p className="mt-2 text-gray-600">
        Processos sobre proteção de dados pessoais, por ano de ajuizamento.
      </p>

      {erro && (
        <p className="mt-6 text-red-600">
          Não consegui falar com a API. Ela está ligada?
        </p>
      )}

      <div className="mt-8 h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={dados}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="ano" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar dataKey="quantidade" fill="#2563eb" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </main>
  );
}