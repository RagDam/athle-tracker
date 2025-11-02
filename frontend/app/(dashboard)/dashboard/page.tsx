"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { MainLayout } from "@/components/layout/main-layout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { authApi, setAuthToken } from "@/lib/api/client";
import type { User } from "@/types";

/**
 * Dashboard page - main landing page after login.
 */
export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [currentPage, setCurrentPage] = useState("dashboard");

  useEffect(() => {
    // Check authentication
    const token = localStorage.getItem("auth_token");
    const storedUser = localStorage.getItem("user");

    if (!token || !storedUser) {
      router.push("/login");
      return;
    }

    setAuthToken(token);
    setUser(JSON.parse(storedUser));
  }, [router]);

  const handleLogout = () => {
    authApi.logout();
    localStorage.removeItem("auth_token");
    localStorage.removeItem("user");
    router.push("/login");
  };

  const handleNavigate = (page: string) => {
    // Handle navigation based on page type
    if (page === "dashboard") {
      setCurrentPage("dashboard");
      router.push("/dashboard");
    } else if (page === "admin") {
      // Don't set currentPage here - will be handled by admin page
      router.push("/admin");
    } else if (page.startsWith("admin-")) {
      // Admin sub-pages: navigate to admin page
      router.push("/admin");
    } else {
      // User pages: rankings, alerts, favorites
      setCurrentPage(page);
      router.push(`/${page}`);
    }
  };

  if (!user) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p>Chargement...</p>
      </div>
    );
  }

  return (
    <MainLayout
      user={user}
      currentPage={currentPage}
      onNavigate={handleNavigate}
      onLogout={handleLogout}
    >
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-muted-foreground">
            Bienvenue sur Athle Tracker
          </p>
        </div>

        {/* Stats cards */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Épreuves actives</CardTitle>
              <span className="text-2xl">🏅</span>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">1</div>
              <p className="text-xs text-muted-foreground">
                Javelot Cadets 2026
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Alertes non lues</CardTitle>
              <span className="text-2xl">🔔</span>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">0</div>
              <p className="text-xs text-muted-foreground">
                Aucune nouvelle alerte
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Athlètes suivis</CardTitle>
              <span className="text-2xl">👥</span>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">170</div>
              <p className="text-xs text-muted-foreground">
                Classement complet
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Dernier scraping</CardTitle>
              <span className="text-2xl">📊</span>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">-</div>
              <p className="text-xs text-muted-foreground">
                À venir
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Welcome message */}
        <Card>
          <CardHeader>
            <CardTitle>Bienvenue ! 🎉</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-muted-foreground">
              Votre application de suivi des classements athlétiques est maintenant prête !
            </p>
            <div className="rounded-lg bg-primary/10 p-4">
              <h3 className="font-semibold text-primary mb-2">Fonctionnalités disponibles :</h3>
              <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground">
                <li>Consultation des classements en temps réel</li>
                <li>Alertes personnalisées pour les changements de position</li>
                <li>Suivi de vos athlètes favoris</li>
                <li>Administration des épreuves et utilisateurs (admin)</li>
                <li>Scraping automatique quotidien</li>
              </ul>
            </div>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  );
}
