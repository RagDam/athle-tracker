"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { MainLayout } from "@/components/layout/main-layout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { authApi, setAuthToken } from "@/lib/api/client";
import type { User } from "@/types";

/**
 * Admin page - administration panel with multiple tabs.
 * Contains Épreuves, Utilisateurs, and Scraping management.
 */
export default function AdminPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [currentPage, setCurrentPage] = useState("admin-epreuves");

  useEffect(() => {
    // Check authentication and admin role
    const token = localStorage.getItem("auth_token");
    const storedUser = localStorage.getItem("user");

    if (!token || !storedUser) {
      router.push("/login");
      return;
    }

    const parsedUser = JSON.parse(storedUser);
    if (parsedUser.role !== "admin") {
      router.push("/dashboard");
      return;
    }

    setAuthToken(token);
    setUser(parsedUser);
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
      router.push("/dashboard");
    } else if (page === "admin") {
      // When navigating to admin, set currentPage to admin-epreuves (default tab)
      setCurrentPage("admin-epreuves");
      router.push("/admin");
    } else if (page.startsWith("admin-")) {
      // Admin sub-pages: stay on admin page
      setCurrentPage(page);
    } else {
      // User pages: rankings, alerts, favorites
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
          <h1 className="text-3xl font-bold">Administration</h1>
          <p className="text-muted-foreground">
            Gérez les épreuves, utilisateurs et le scraping
          </p>
        </div>

        {/* Admin Tabs */}
        <Tabs defaultValue="epreuves" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="epreuves" onClick={() => setCurrentPage("admin-epreuves")}>
              Épreuves
            </TabsTrigger>
            <TabsTrigger value="users" onClick={() => setCurrentPage("admin-users")}>
              Utilisateurs
            </TabsTrigger>
            <TabsTrigger value="scraping" onClick={() => setCurrentPage("admin-scraping")}>
              Scraping
            </TabsTrigger>
          </TabsList>

          {/* Épreuves Tab */}
          <TabsContent value="epreuves" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Gestion des Épreuves</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Gestion des épreuves athlétiques suivies (à implémenter)
                </p>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Users Tab */}
          <TabsContent value="users" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Gestion des Utilisateurs</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Gestion des comptes utilisateurs (à implémenter)
                </p>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Scraping Tab */}
          <TabsContent value="scraping" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Gestion du Scraping</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Configuration et logs du scraping (à implémenter)
                </p>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </MainLayout>
  );
}
