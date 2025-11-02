"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { MainLayout } from "@/components/layout/main-layout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { authApi, setAuthToken, rankingsApi } from "@/lib/api/client";
import type { User } from "@/types";
import { Badge } from "@/components/ui/badge";
import { Star, StarOff, Trophy, TrendingUp } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

/**
 * Favorites page - displays and manages favorite athletes.
 */
export default function FavoritesPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [currentPage, setCurrentPage] = useState("favorites");
  const [favorites, setFavorites] = useState<any[]>([]);
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

    // Load favorites data
    loadFavorites();
  }, [router]);

  const loadFavorites = async () => {
    try {
      setIsLoading(true);
      // For now, we'll get all rankings and filter favorites
      // TODO: Add favorites endpoint in API
      const data = await rankingsApi.getAll();
      // Simulate favorites (first 5 athletes for demo)
      setFavorites(data.slice(0, 5));
    } catch (error) {
      console.error("Error loading favorites:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleToggleFavorite = async (athleteId: number) => {
    // TODO: Implement favorite toggle API call
    console.log("Toggle favorite for athlete:", athleteId);
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
          <h1 className="text-3xl font-bold">Athlètes Favoris</h1>
          <p className="text-muted-foreground">
            Suivez les performances de vos athlètes préférés
          </p>
        </div>

        {/* Stats cards */}
        <div className="grid gap-4 md:grid-cols-3">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Athlètes suivis
              </CardTitle>
              <Star className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{favorites.length}</div>
              <p className="text-xs text-muted-foreground">Dans vos favoris</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Meilleur classé
              </CardTitle>
              <Trophy className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {favorites[0]?.rang || "-"}
              </div>
              <p className="text-xs text-muted-foreground">
                {favorites[0]?.athlete_nom || "Aucun favori"}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Progressions
              </CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {favorites.filter((f) => f.changement_rang > 0).length}
              </div>
              <p className="text-xs text-muted-foreground">
                Athlètes en progression
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Favorites table */}
        <Card>
          <CardHeader>
            <CardTitle>Vos Favoris</CardTitle>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <p className="text-center py-8 text-muted-foreground">
                Chargement des favoris...
              </p>
            ) : favorites.length === 0 ? (
              <div className="text-center py-8">
                <StarOff className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground mb-2">
                  Aucun athlète favori pour le moment.
                </p>
                <p className="text-sm text-muted-foreground">
                  Ajoutez des athlètes à vos favoris depuis la page Classements
                  pour suivre leurs performances.
                </p>
              </div>
            ) : (
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-20">Rang</TableHead>
                    <TableHead>Athlète</TableHead>
                    <TableHead>Club</TableHead>
                    <TableHead className="text-right">Performance</TableHead>
                    <TableHead className="text-right">Date</TableHead>
                    <TableHead className="w-24">Évolution</TableHead>
                    <TableHead className="w-24"></TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {favorites.map((favorite) => (
                    <TableRow key={favorite.id}>
                      <TableCell className="font-medium">
                        {favorite.rang}
                      </TableCell>
                      <TableCell className="font-semibold">
                        <div className="flex items-center gap-2">
                          <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                          {favorite.athlete_nom}
                        </div>
                      </TableCell>
                      <TableCell className="text-muted-foreground">
                        {favorite.club}
                      </TableCell>
                      <TableCell className="text-right font-semibold">
                        {favorite.performance}
                      </TableCell>
                      <TableCell className="text-right text-muted-foreground">
                        {new Date(favorite.date_performance).toLocaleDateString(
                          "fr-FR"
                        )}
                      </TableCell>
                      <TableCell>
                        {favorite.changement_rang !== 0 && (
                          <Badge
                            variant={
                              favorite.changement_rang > 0
                                ? "default"
                                : "destructive"
                            }
                          >
                            {favorite.changement_rang > 0 ? "↑" : "↓"}{" "}
                            {Math.abs(favorite.changement_rang)}
                          </Badge>
                        )}
                      </TableCell>
                      <TableCell>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleToggleFavorite(favorite.id)}
                        >
                          <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </CardContent>
        </Card>

        {/* Info card */}
        <Card className="border-primary/50 bg-primary/5">
          <CardContent className="pt-6">
            <div className="flex gap-4">
              <Star className="h-5 w-5 text-primary mt-1" />
              <div>
                <h3 className="font-semibold mb-1">
                  Comment ajouter des favoris ?
                </h3>
                <p className="text-sm text-muted-foreground">
                  Rendez-vous sur la page Classements et cliquez sur l&apos;icône
                  étoile à côté du nom d&apos;un athlète pour l&apos;ajouter à vos
                  favoris. Vous recevrez alors des alertes automatiques en cas
                  de changement de position.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  );
}
