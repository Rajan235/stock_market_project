"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import API from "@/utils/api";

export default function CompanyPage() {
  const { id } = useParams();
  const [company, setCompany] = useState<any>(null);
  const [events, setEvents] = useState<any[]>([]);

  useEffect(() => {
    if (!id) return;
    API.get(`/companies/${id}`).then((res) => setCompany(res.data));
    API.get(`/companies/${id}/events`).then((res) => setEvents(res.data));
  }, [id]);

  if (!company) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-3xl font-bold">{company.company_name}</h1>
      <p className="text-gray-500">{company.sector}</p>

      <h2 className="text-xl font-semibold mt-6">Recent Events</h2>
      <ul className="space-y-3">
        {events.map((e, idx) => (
          <li key={idx} className="bg-gray-100 rounded p-4">
            <div>
              <strong>{e.main_metric}</strong> | {e.event_timestamp}
            </div>
            <div>
              Previous: {e.previous_value} → Current: {e.current_value} (Δ{" "}
              {e.variance})
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
