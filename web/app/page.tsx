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


const API = "http://127.0.0.1:8000";

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
      <h2 className="text-xl font-semibold">{titulo}</h2>
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
      <h1 className="text-3xl font-bold">Observatório Jurídico</h1>
      <p className="mt-2 text-gray-500">
        Processos sobre proteção de dados pessoais, coletados na API pública do
        DataJud (CNJ).
      </p>
      <p className="mt-2 text-sm text-amber-500">
        Atenção: os dados são uma amostra, não o total de processos de cada
        tribunal.
      </p>

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