"use client";

import API from "@/utils/api";
import Link from "next/link";
import { useEffect, useState } from "react";

export default function Home() {
  const [companies, setCompanies] = useState([]);

  useEffect(() => {
    API.get("/companies")
      .then((response) => {
        console.log("Fetched companies:", response.data);
        setCompanies(response.data);
      })
      .catch((error) => {
        console.error("Error fetching companies:", error);
      });
  }, []);
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">NIFTY 50 Companies</h1>
      <ul className="space-y-4">
        {companies.map((c: any) => (
          <li key={c.companyId} className="bg-white rounded shadow p-4">
            <Link
              href={`/company/${c.companyId}`}
              className="text-blue-600 hover:underline"
            >
              {c.companyName} ({c.companyCode})
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
