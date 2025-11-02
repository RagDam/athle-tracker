"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { MainLayout } from "@/components/layout/main-layout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { authApi, setAuthToken, rankingsApi } from "@/lib/api/client";
import type { User } from "@/types";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

/**
 * Rankings page - displays current rankings for all active competitions.
 */
export default function RankingsPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [currentPage, setCurrentPage] = useState("rankings");
  const [rankings, setRankings] = useState<any[]>([]);
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

    // Load rankings data
    loadRankings();
  }, [router]);

  const loadRankings = async () => {
    try {
      setIsLoading(true);
      const data = await rankingsApi.getAll();
      setRankings(data);
    } catch (error) {
      console.error("Error loading rankings:", error);
    } finally {
      setIsLoading(false);
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

  return (
    <MainLayout
      user={user}
      currentPage={currentPage}
      onNavigate={handleNavigate}
      onLogout={handleLogout}
    >
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Classements</h1>
          <p className="text-muted-foreground">
            Consultez les classements en temps réel
          </p>
        </div>

        {/* Rankings table */}
        <Card>
          <CardHeader>
            <CardTitle>Javelot Cadets 2026</CardTitle>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <p className="text-center py-8 text-muted-foreground">
                Chargement des classements...
              </p>
            ) : rankings.length === 0 ? (
              <p className="text-center py-8 text-muted-foreground">
                Aucun classement disponible pour le moment.
              </p>
            ) : (
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-20">Rang</TableHead>
                    <TableHead>Athlète</TableHead>
                    <TableHead>Club</TableHead>
                    <TableHead className="text-right">Performance</TableHead>
                    <TableHead className="text-right">Date</TableHead>
                    <TableHead className="w-24">Statut</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {rankings.map((ranking) => (
                    <TableRow key={ranking.id}>
                      <TableCell className="font-medium">
                        {ranking.rang}
                      </TableCell>
                      <TableCell>{ranking.athlete_nom}</TableCell>
                      <TableCell className="text-muted-foreground">
                        {ranking.club}
                      </TableCell>
                      <TableCell className="text-right font-semibold">
                        {ranking.performance}
                      </TableCell>
                      <TableCell className="text-right text-muted-foreground">
                        {new Date(ranking.date_performance).toLocaleDateString(
                          "fr-FR"
                        )}
                      </TableCell>
                      <TableCell>
                        {ranking.changement_rang !== 0 && (
                          <Badge
                            variant={
                              ranking.changement_rang > 0
                                ? "default"
                                : "destructive"
                            }
                          >
                            {ranking.changement_rang > 0 ? "↑" : "↓"}{" "}
                            {Math.abs(ranking.changement_rang)}
                          </Badge>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </CardContent>
        </Card>

        {/* Stats summary */}
        <div className="grid gap-4 md:grid-cols-3">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total athlètes
              </CardTitle>
              <span className="text-2xl">👥</span>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{rankings.length}</div>
              <p className="text-xs text-muted-foreground">
                Classement complet
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Meilleure performance
              </CardTitle>
              <span className="text-2xl">🏆</span>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {rankings[0]?.performance || "-"}
              </div>
              <p className="text-xs text-muted-foreground">
                {rankings[0]?.athlete_nom || "Aucune donnée"}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Dernière mise à jour
              </CardTitle>
              <span className="text-2xl">📅</span>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {rankings[0]
                  ? new Date(rankings[0].date_scraping).toLocaleDateString(
                      "fr-FR"
                    )
                  : "-"}
              </div>
              <p className="text-xs text-muted-foreground">Dernier scraping</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </MainLayout>
  );
}
