"use client";

import { User, Settings, LogOut, LayoutDashboard, Shield } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

interface HeaderProps {
  user?: {
    email: string;
    role: "admin" | "user";
  };
  currentPage: "dashboard" | "admin";
  onNavigate: (page: "dashboard" | "admin") => void;
  onLogout: () => void;
}

/**
 * Full-width header component with gradient background.
 * Contains app name, navigation tabs (Dashboard/Admin), user info, settings icon, and logout.
 */
export function Header({ user, currentPage, onNavigate, onLogout }: HeaderProps) {
  const isAdmin = user?.role === "admin";

  return (
    <header className="w-full bg-gradient-to-r from-purple-600 to-purple-800 shadow-lg">
      <div className="flex items-center justify-between px-6 py-4">
        {/* Left side: App name + Navigation tabs */}
        <div className="flex items-center gap-6">
          {/* App name */}
          <div className="flex items-center gap-2">
            <span className="text-2xl">🏃</span>
            <h1 className="text-xl font-bold text-white">Athle Tracker</h1>
          </div>

          {/* Navigation tabs */}
          <nav className="flex items-center gap-2">
            <Button
              variant={currentPage === "dashboard" ? "secondary" : "ghost"}
              className={
                currentPage === "dashboard"
                  ? "bg-white/20 text-white hover:bg-white/30"
                  : "text-white/80 hover:bg-white/10 hover:text-white"
              }
              onClick={() => onNavigate("dashboard")}
            >
              <LayoutDashboard className="mr-2 h-4 w-4" />
              Dashboard
            </Button>

            {isAdmin && (
              <Button
                variant={currentPage === "admin" ? "secondary" : "ghost"}
                className={
                  currentPage === "admin"
                    ? "bg-white/20 text-white hover:bg-white/30"
                    : "text-white/80 hover:bg-white/10 hover:text-white"
                }
                onClick={() => onNavigate("admin")}
              >
                <Shield className="mr-2 h-4 w-4" />
                Admin
              </Button>
            )}
          </nav>
        </div>

        {/* Right side: User info + Settings + Logout */}
        <div className="flex items-center gap-4">
          {/* User info */}
          {user && (
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium text-white">{user.email}</span>
              <Badge
                variant={isAdmin ? "default" : "secondary"}
                className={
                  isAdmin
                    ? "bg-yellow-400 text-yellow-900 hover:bg-yellow-500"
                    : "bg-white/20 text-white"
                }
              >
                {user.role.toUpperCase()}
              </Badge>
            </div>
          )}

          {/* Settings icon (for admin) */}
          {isAdmin && (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button
                  variant="ghost"
                  size="icon"
                  className="text-white hover:bg-white/10"
                  title="Paramètres"
                >
                  <Settings className="h-5 w-5" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56">
                <DropdownMenuItem onClick={() => onNavigate("admin")}>
                  <Shield className="mr-2 h-4 w-4" />
                  Administration
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          )}

          {/* Logout button */}
          <Button
            variant="ghost"
            size="icon"
            className="text-white hover:bg-white/10"
            onClick={onLogout}
            title="Déconnexion"
          >
            <LogOut className="h-5 w-5" />
          </Button>
        </div>
      </div>
    </header>
  );
}
