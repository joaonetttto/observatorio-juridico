"use client";

import { useEffect, useState } from "react";
import StatusColetas from "./StatusColetas";
import AcordaosStj from "./AcordaosStj";
import BuscaAcordaos from "./BuscaAcordaos";
import KpiCards from "./KpiCards";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

type Linha = Record<string, string | number>;

type GraficoProps = {
  titulo: string;
  descricao: string;
  dados: Linha[];
  categoria: string;
  valor: string;
  horizontal?: boolean;
};

function Grafico({
  titulo,
  descricao,
  dados,
  categoria,
  valor,
  horizontal = false,
}: GraficoProps) {
  return (
    <section className="mt-8 rounded-xl border border-gray-800 bg-gray-900/40 p-6">
      <h2 className="border-l-4 border-blue-500 pl-3 text-xl font-semibold">
        {titulo}
      </h2>
      <p className="mt-1 text-sm text-gray-500">{descricao}</p>
      <div className={horizontal ? "mt-4 h-96" : "mt-4 h-72"}>
        <ResponsiveContainer width="100%" height="100%">
          {horizontal ? (
            <BarChart data={dados} layout="vertical" margin={{ left: 20 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" allowDecimals={false} />
              <YAxis
                type="category"
                dataKey={categoria}
                width={220}
                tick={{ fontSize: 12 }}
              />
              <Tooltip />
              <Bar dataKey={valor} fill="#2563eb" />
            </BarChart>
          ) : (
            <BarChart data={dados}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={categoria} />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey={valor} fill="#2563eb" />
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>
    </section>
  );
}

export default function Home() {
  const [porAno, setPorAno] = useState<Linha[]>([]);
  const [porTribunal, setPorTribunal] = useState<Linha[]>([]);
  const [assuntos, setAssuntos] = useState<Linha[]>([]);
  const [classes, setClasses] = useState<Linha[]>([]);
  const [erro, setErro] = useState(false);

  useEffect(() => {
    Promise.all([
      fetch(`${API}/processos-por-ano`).then((r) => r.json()),
      fetch(`${API}/tribunais`).then((r) => r.json()),
      fetch(`${API}/assuntos-relacionados`).then((r) => r.json()),
      fetch(`${API}/classes`).then((r) => r.json()),
    ])
      .then(([ano, tribunal, assunto, classe]) => {
        setPorAno(ano);
        setPorTribunal(tribunal);
        setAssuntos(assunto);
        setClasses(classe);
      })
      .catch(() => setErro(true));
  }, []);

  return (
    <main className="mx-auto max-w-4xl p-8">
      <header>
        <span className="rounded-full border border-blue-500/40 bg-blue-500/10 px-3 py-1 text-xs font-medium text-blue-400">
          Projeto de portfólio · LGPD
        </span>
        <h1 className="mt-4 text-4xl font-bold tracking-tight md:text-5xl">
          Observatório <span className="text-blue-500">Jurídico</span>
        </h1>
        <p className="mt-3 max-w-2xl text-base text-gray-400">
          Decisões judiciais sobre proteção de dados pessoais (LGPD), coletadas
          no DataJud (CNJ) e nos Dados Abertos do STJ.
        </p>
        <p className="mt-4 rounded-lg border border-amber-500/30 bg-amber-500/10 px-4 py-2 text-sm text-amber-400">
          Atenção: os dados são uma amostra, não o total de processos de cada
          tribunal.
        </p>
      </header>

      {erro && (
        <p className="mt-6 text-red-600">
          Não consegui falar com a API. Ela está ligada?
        </p>
      )}

      <KpiCards />
      <StatusColetas />

      <Grafico
        titulo="Processos por ano de ajuizamento"
        descricao="Quantidade de processos da amostra, por ano em que foram abertos."
        dados={porAno}
        categoria="ano"
        valor="quantidade"
      />

      <Grafico
        titulo="Processos por tribunal"
        descricao="Quantos processos de cada tribunal estão na amostra."
        dados={porTribunal}
        categoria="sigla"
        valor="processos"
      />

      <Grafico
        titulo="Assuntos que aparecem junto"
        descricao="Outros assuntos registrados nos mesmos processos."
        dados={assuntos}
        categoria="assunto"
        valor="quantidade"
        horizontal
      />

      <Grafico
        titulo="Classes de processo mais comuns"
        descricao="Tipo de ação em que os processos foram abertos."
        dados={classes}
        categoria="classe"
        valor="quantidade"
        horizontal
      />

      <AcordaosStj />
      <BuscaAcordaos />
    </main>
  );
}