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
type Acordao = {
  id_stj: string;
  orgao_julgador: string;
  classe: string;
  data: string;
  ementa: string;
};

export default function AcordaosStj() {
  const [porAno, setPorAno] = useState<PorAno[]>([]);
  const [recentes, setRecentes] = useState<Acordao[]>([]);

  useEffect(() => {
    fetch(`${API}/acordaos-por-ano`)
      .then((r) => r.json())
      .then(setPorAno)
      .catch(() => setPorAno([]));
    fetch(`${API}/acordaos-recentes`)
      .then((r) => r.json())
      .then(setRecentes)
      .catch(() => setRecentes([]));
  }, []);

  return (
    <section className="mt-16">
      <h2 className="text-2xl font-bold">Acórdãos do STJ que citam a LGPD</h2>
      <p className="mt-2 text-sm text-gray-500">
        Fonte: Portal de Dados Abertos do STJ (espelhos de acórdãos). Aqui entram
        os acórdãos cuja ementa, referências legislativas ou termos de pesquisa
        citam a Lei 13.709/2018. Isso não significa que a LGPD seja o assunto
        central de cada decisão.
      </p>

      <div className="mt-6 h-72">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={porAno}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="ano" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar dataKey="quantidade" fill="#2563eb" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <h3 className="mt-10 text-lg font-semibold">Mais recentes</h3>
      <ul className="mt-4 space-y-4">
        {recentes.map((acordao) => (
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
            <p className="mt-2 text-gray-400">{acordao.ementa}...</p>
          </li>
        ))}
      </ul>
    </section>
  );
}
