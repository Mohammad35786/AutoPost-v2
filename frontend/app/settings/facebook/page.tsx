"use client";

import { useEffect, useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import api from "@/lib/api";

interface FbStatus {
  is_connected: boolean;
  page_name?: string;
  connected_at?: string;
}

function FacebookSettingsContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  
  const [status, setStatus] = useState<FbStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [pagesToSelect, setPagesToSelect] = useState<any[]>([]);

  const fetchStatus = async () => {
    try {
      setLoading(true);
      const res = await api.get("/facebook/status");
      setStatus(res.data);
    } catch (err) {
      console.error("Failed to fetch status", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const connected = searchParams.get("connected");
    const pagesParam = searchParams.get("pages");

    if (connected === "true") {
      // Remove query param
      router.replace("/settings/facebook");
    }

    if (pagesParam) {
      try {
        const parsed = JSON.parse(decodeURIComponent(pagesParam));
        setPagesToSelect(parsed);
      } catch (err) {
        console.error("Failed to parse pages", err);
      }
    }

    fetchStatus();
  }, [searchParams, router]);

  const handleConnect = async () => {
    try {
      const res = await api.get("/facebook/connect-url");
      if (res.data.url) {
        window.location.href = res.data.url;
      }
    } catch (err) {
      console.error("Failed to get connect url", err);
      alert("Failed to initiate connection");
    }
  };

  const handleDisconnect = async () => {
    if (!confirm("Are you sure you want to disconnect your Facebook Page?")) return;
    try {
      await api.delete("/facebook/disconnect");
      setStatus({ is_connected: false });
    } catch (err) {
      console.error("Failed to disconnect", err);
      alert("Failed to disconnect");
    }
  };

  const handleSelectPage = async (page: any) => {
    try {
      await api.post("/facebook/select-page", {
        page_id: page.id,
        page_name: page.name,
        encrypted_token: page.token,
      });
      setPagesToSelect([]);
      router.replace("/settings/facebook");
      fetchStatus();
    } catch (err) {
      console.error("Failed to select page", err);
      alert("Failed to select page");
    }
  };

  if (loading) {
    return <div className="p-8"><div className="animate-pulse flex space-x-4"><div className="flex-1 space-y-6 py-1"><div className="h-2 bg-slate-200 rounded"></div></div></div></div>;
  }

  return (
    <div className="max-w-4xl mx-auto p-6 md:p-12">
      <h1 className="text-3xl font-bold mb-8 text-gray-900">Facebook Integration</h1>
      
      {pagesToSelect.length > 0 ? (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h2 className="text-xl font-semibold mb-4 text-gray-800">Select a Page</h2>
          <p className="text-gray-600 mb-6">You manage multiple pages. Which one would you like to connect?</p>
          <div className="space-y-4">
            {pagesToSelect.map((page) => (
              <div key={page.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition">
                <span className="font-medium text-gray-800">{page.name}</span>
                <button
                  onClick={() => handleSelectPage(page)}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition shadow-sm"
                >
                  Select
                </button>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 flex flex-col items-center text-center">
          <div className={`w-20 h-20 rounded-full flex items-center justify-center mb-6 ${status?.is_connected ? "bg-green-100 text-green-600" : "bg-gray-100 text-gray-400"}`}>
            <svg className="w-10 h-10" fill="currentColor" viewBox="0 0 24 24">
              <path d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" />
            </svg>
          </div>
          
          <h2 className="text-2xl font-semibold mb-2 text-gray-900">
            {status?.is_connected ? "Connected to Facebook" : "Not Connected"}
          </h2>
          
          {status?.is_connected ? (
            <>
              <p className="text-gray-600 mb-8">
                Currently posting to <span className="font-semibold text-gray-900">{status.page_name}</span>
              </p>
              <button
                onClick={handleDisconnect}
                className="px-6 py-2.5 bg-red-50 text-red-600 rounded-lg font-medium hover:bg-red-100 transition"
              >
                Disconnect
              </button>
            </>
          ) : (
            <>
              <p className="text-gray-600 mb-8 max-w-md">
                Connect your Facebook Page to allow AutoPoster to publish content automatically.
              </p>
              <button
                onClick={handleConnect}
                className="px-8 py-3 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 hover:shadow-lg hover:-translate-y-0.5 transition duration-200"
              >
                Connect Facebook
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default function FacebookSettings() {
  return (
    <Suspense fallback={<div className="p-8">Loading...</div>}>
      <FacebookSettingsContent />
    </Suspense>
  );
}

