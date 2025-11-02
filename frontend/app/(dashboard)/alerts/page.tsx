"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { MainLayout } from "@/components/layout/main-layout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { authApi, setAuthToken, alertsApi } from "@/lib/api/client";
import type { User } from "@/types";
import { Badge } from "@/components/ui/badge";
import { Bell, BellOff, TrendingUp, TrendingDown } from "lucide-react";
import { Button } from "@/components/ui/button";

/**
 * Alerts page - displays notification center for ranking changes.
 */
export default function AlertsPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [currentPage, setCurrentPage] = useState("alerts");
  const [alerts, setAlerts] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

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

    // Load alerts data
    loadAlerts();
  }, [router]);

  const loadAlerts = async () => {
    try {
      setIsLoading(true);
      const data = await alertsApi.getAll();
      setAlerts(data);
    } catch (error) {
      console.error("Error loading alerts:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleMarkAsRead = async (alertId: number) => {
    try {
      await alertsApi.markAsRead(alertId);
      await loadAlerts(); // Reload alerts
    } catch (error) {
      console.error("Error marking alert as read:", error);
    }
  };

  const handleLogout = () => {
    authApi.logout();
    localStorage.removeItem("auth_token");
    localStorage.removeItem("user");
    router.push("/login");
  };

  const handleNavigate = (page: string) => {
    setCurrentPage(page);

    if (page === "dashboard") {
      router.push("/dashboard");
    } else if (page === "admin") {
      router.push("/admin");
    } else if (page.startsWith("admin-")) {
      router.push("/admin");
    } else {
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

  const unreadCount = alerts.filter((a) => !a.lu).length;

  return (
    <MainLayout
      user={user}
      currentPage={currentPage}
      onNavigate={handleNavigate}
      onLogout={handleLogout}
    >
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Alertes</h1>
            <p className="text-muted-foreground">
              Centre de notifications pour les changements de classement
            </p>
          </div>
          {unreadCount > 0 && (
            <Badge variant="default" className="text-lg px-4 py-2">
              {unreadCount} non lue{unreadCount > 1 ? "s" : ""}
            </Badge>
          )}
        </div>

        {/* Stats cards */}
        <div className="grid gap-4 md:grid-cols-3">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Alertes non lues
              </CardTitle>
              <Bell className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{unreadCount}</div>
              <p className="text-xs text-muted-foreground">À consulter</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total alertes
              </CardTitle>
              <BellOff className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{alerts.length}</div>
              <p className="text-xs text-muted-foreground">Toutes périodes</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Dernière alerte
              </CardTitle>
              <Bell className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {alerts[0]
                  ? new Date(alerts[0].created_at).toLocaleDateString("fr-FR")
                  : "-"}
              </div>
              <p className="text-xs text-muted-foreground">
                {alerts[0]
                  ? new Date(alerts[0].created_at).toLocaleTimeString("fr-FR", {
                      hour: "2-digit",
                      minute: "2-digit",
                    })
                  : "Aucune alerte"}
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Alerts list */}
        <div className="space-y-4">
          {isLoading ? (
            <Card>
              <CardContent className="py-8">
                <p className="text-center text-muted-foreground">
                  Chargement des alertes...
                </p>
              </CardContent>
            </Card>
          ) : alerts.length === 0 ? (
            <Card>
              <CardContent className="py-8">
                <div className="flex flex-col items-center gap-2">
                  <BellOff className="h-12 w-12 text-muted-foreground" />
                  <p className="text-center text-muted-foreground">
                    Aucune alerte pour le moment.
                  </p>
                  <p className="text-center text-sm text-muted-foreground">
                    Les alertes apparaîtront ici lorsque des changements de
                    classement seront détectés.
                  </p>
                </div>
              </CardContent>
            </Card>
          ) : (
            alerts.map((alert) => (
              <Card
                key={alert.id}
                className={alert.lu ? "opacity-60" : "border-primary"}
              >
                <CardContent className="py-4">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex items-start gap-4 flex-1">
                      {/* Icon based on change type */}
                      <div
                        className={`p-2 rounded-full ${
                          alert.nouveau_rang < alert.ancien_rang
                            ? "bg-green-100 text-green-600"
                            : "bg-red-100 text-red-600"
                        }`}
                      >
                        {alert.nouveau_rang < alert.ancien_rang ? (
                          <TrendingUp className="h-5 w-5" />
                        ) : (
                          <TrendingDown className="h-5 w-5" />
                        )}
                      </div>

                      {/* Alert content */}
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <h3 className="font-semibold">{alert.athlete_nom}</h3>
                          {!alert.lu && (
                            <Badge variant="default" className="text-xs">
                              Nouveau
                            </Badge>
                          )}
                        </div>
                        <p className="text-sm text-muted-foreground mb-2">
                          {alert.message}
                        </p>
                        <div className="flex items-center gap-4 text-xs text-muted-foreground">
                          <span>
                            {new Date(alert.created_at).toLocaleDateString(
                              "fr-FR",
                              {
                                day: "numeric",
                                month: "long",
                                year: "numeric",
                                hour: "2-digit",
                                minute: "2-digit",
                              }
                            )}
                          </span>
                          <span>
                            Rang {alert.ancien_rang} → {alert.nouveau_rang}
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* Mark as read button */}
                    {!alert.lu && (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleMarkAsRead(alert.id)}
                      >
                        Marquer comme lu
                      </Button>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      </div>
    </MainLayout>
  );
}
