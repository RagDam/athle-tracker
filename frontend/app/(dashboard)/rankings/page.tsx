"use client";

import { useEffect, useState, useMemo } from "react";
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
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { X, Search } from "lucide-react";

/**
 * Rankings page - displays current rankings for all active competitions.
 */
export default function RankingsPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [currentPage, setCurrentPage] = useState("rankings");
  const [rankings, setRankings] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Filter states for each column (no filter for rank)
  const [filterAthlete, setFilterAthlete] = useState("");
  const [filterClub, setFilterClub] = useState("");
  const [filterPerformance, setFilterPerformance] = useState("");
  const [filterDate, setFilterDate] = useState("");

  // Debounced filter states (used for actual filtering)
  const [debouncedFilterAthlete, setDebouncedFilterAthlete] = useState("");
  const [debouncedFilterClub, setDebouncedFilterClub] = useState("");
  const [debouncedFilterPerformance, setDebouncedFilterPerformance] = useState("");
  const [debouncedFilterDate, setDebouncedFilterDate] = useState("");

  // Debounce effect for filters (500ms delay)
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedFilterAthlete(filterAthlete);
      setDebouncedFilterClub(filterClub);
      setDebouncedFilterPerformance(filterPerformance);
      setDebouncedFilterDate(filterDate);
    }, 500);

    return () => clearTimeout(timer);
  }, [filterAthlete, filterClub, filterPerformance, filterDate]);

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

  // Clear all filters
  const clearFilters = () => {
    setFilterAthlete("");
    setFilterClub("");
    setFilterPerformance("");
    setFilterDate("");
  };

  // Check if any filter is active
  const hasActiveFilters =
    debouncedFilterAthlete || debouncedFilterClub || debouncedFilterPerformance || debouncedFilterDate;

  // Filter rankings based on all column filters (using debounced values)
  const filteredRankings = useMemo(() => {
    return rankings.filter((ranking) => {
      const matchAthlete = debouncedFilterAthlete === "" ||
        ranking.athlete_nom.toLowerCase().includes(debouncedFilterAthlete.toLowerCase());

      const matchClub = debouncedFilterClub === "" ||
        (ranking.club && ranking.club.toLowerCase().includes(debouncedFilterClub.toLowerCase()));

      const matchPerformance = debouncedFilterPerformance === "" ||
        ranking.performance.toLowerCase().includes(debouncedFilterPerformance.toLowerCase());

      const matchDate = debouncedFilterDate === "" ||
        new Date(ranking.date_performance)
          .toLocaleDateString("fr-FR")
          .includes(debouncedFilterDate);

      return matchAthlete && matchClub && matchPerformance && matchDate;
    });
  }, [rankings, debouncedFilterAthlete, debouncedFilterClub, debouncedFilterPerformance, debouncedFilterDate]);

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
              <div className="space-y-4">
                {/* Clear filters button and results count */}
                {hasActiveFilters && (
                  <div className="flex items-center justify-between">
                    <p className="text-sm text-muted-foreground">
                      {filteredRankings.length} résultat(s) sur {rankings.length}
                    </p>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={clearFilters}
                      className="h-8 text-xs"
                    >
                      <X className="mr-1 h-3 w-3" />
                      Effacer les filtres
                    </Button>
                  </div>
                )}

                <Table>
                  <TableHeader>
                    {/* Column labels */}
                    <TableRow>
                      <TableHead className="w-20">Rang</TableHead>
                      <TableHead>Athlète</TableHead>
                      <TableHead>Club</TableHead>
                      <TableHead className="text-right">Performance</TableHead>
                      <TableHead className="text-right">Date</TableHead>
                      <TableHead className="w-24">Statut</TableHead>
                    </TableRow>
                    {/* Search inputs */}
                    <TableRow className="hover:bg-transparent">
                      <TableHead className="h-12 py-2">
                        {/* No filter for rank */}
                      </TableHead>
                      <TableHead className="py-2">
                        <div className="relative">
                          <Search className="absolute left-2 top-1/2 h-3 w-3 -translate-y-1/2 text-muted-foreground" />
                          <Input
                            placeholder="Rechercher..."
                            value={filterAthlete}
                            onChange={(e) => setFilterAthlete(e.target.value)}
                            className="h-8 text-xs pl-7 pr-7"
                          />
                          {filterAthlete && (
                            <button
                              onClick={() => setFilterAthlete("")}
                              className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                            >
                              <X className="h-3 w-3" />
                            </button>
                          )}
                        </div>
                      </TableHead>
                      <TableHead className="py-2">
                        <div className="relative">
                          <Search className="absolute left-2 top-1/2 h-3 w-3 -translate-y-1/2 text-muted-foreground" />
                          <Input
                            placeholder="Rechercher..."
                            value={filterClub}
                            onChange={(e) => setFilterClub(e.target.value)}
                            className="h-8 text-xs pl-7 pr-7"
                          />
                          {filterClub && (
                            <button
                              onClick={() => setFilterClub("")}
                              className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                            >
                              <X className="h-3 w-3" />
                            </button>
                          )}
                        </div>
                      </TableHead>
                      <TableHead className="py-2">
                        <div className="relative">
                          <Search className="absolute left-2 top-1/2 h-3 w-3 -translate-y-1/2 text-muted-foreground" />
                          <Input
                            placeholder="Rechercher..."
                            value={filterPerformance}
                            onChange={(e) => setFilterPerformance(e.target.value)}
                            className="h-8 text-xs pl-7 pr-7"
                          />
                          {filterPerformance && (
                            <button
                              onClick={() => setFilterPerformance("")}
                              className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                            >
                              <X className="h-3 w-3" />
                            </button>
                          )}
                        </div>
                      </TableHead>
                      <TableHead className="py-2">
                        <div className="relative">
                          <Search className="absolute left-2 top-1/2 h-3 w-3 -translate-y-1/2 text-muted-foreground" />
                          <Input
                            placeholder="JJ/MM/AAAA"
                            value={filterDate}
                            onChange={(e) => setFilterDate(e.target.value)}
                            className="h-8 text-xs pl-7 pr-7"
                          />
                          {filterDate && (
                            <button
                              onClick={() => setFilterDate("")}
                              className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                            >
                              <X className="h-3 w-3" />
                            </button>
                          )}
                        </div>
                      </TableHead>
                      <TableHead className="py-2">
                        {/* No filter for status */}
                      </TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredRankings.map((ranking) => (
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
              </div>
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
              <div className="text-2xl font-bold">{filteredRankings.length}</div>
              <p className="text-xs text-muted-foreground">
                {filteredRankings.length !== rankings.length
                  ? `Filtré sur ${rankings.length}`
                  : "Classement complet"}
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
                {filteredRankings[0]?.performance || "-"}
              </div>
              <p className="text-xs text-muted-foreground">
                {filteredRankings[0]?.athlete_nom || "Aucune donnée"}
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
