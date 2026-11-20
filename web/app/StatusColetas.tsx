"use client";

import { useEffect, useState } from "react";

const API = "http://127.0.0.1:8000";

type Coleta = {
  sigla: string;
  status: string;
  qtd_processos: number;
  no_banco: number;
  iniciada_em: string;
};

export default function StatusColetas() {
  const [coletas, setColetas] = useState<Coleta[]>([]);

  useEffect(() => {
    fetch(`${API}/coletas`)
      .then((resposta) => resposta.json())
      .then(setColetas)
      .catch(() => setColetas([]));
  }, []);

  return (
    <section className="mt-12">
      <h2 className="text-xl font-semibold">Status das coletas</h2>
      <p className="mt-1 text-sm text-gray-500">
        Resultado da última coleta de cada tribunal. &quot;Parcial&quot; quer dizer
        que a API do CNJ falhou no meio, então aquele tribunal pode estar
        incompleto.
      </p>
      <table className="mt-4 w-full text-left text-sm">
        <thead className="border-b border-gray-700 text-gray-400">
          <tr>
            <th className="py-2 pr-6 pr-6 pr-6">Tribunal</th>
            <th className="py-2 pr-6 pr-6 pr-6">Última coleta</th>
            <th className="py-2 pr-6 pr-6 pr-6">Status</th>
            <th className="py-2 pr-6 pr-6 pr-6">Pegos na coleta</th>
            <th className="py-2 pr-6 pr-6 pr-6">Total no banco</th>
          </tr>
        </thead>
        <tbody>
          {coletas.map((coleta) => (
            <tr key={coleta.sigla} className="border-b border-gray-800">
              <td className="py-2 pr-6 pr-6 pr-6 font-medium">{coleta.sigla}</td>
              <td className="py-2 pr-6 pr-6 pr-6">{coleta.iniciada_em}</td>
              <td
                className={
                  coleta.status === "concluida"
                    ? "py-2 pr-6 pr-6 pr-6 text-green-500"
                    : "py-2 pr-6 pr-6 pr-6 text-amber-500"
                }
              >
                {coleta.status === "concluida" ? "concluída" : "parcial"}
              </td>
              <td className="py-2 pr-6 pr-6 pr-6">{coleta.qtd_processos}</td>
              <td className="py-2 pr-6 pr-6 pr-6">{coleta.no_banco}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}