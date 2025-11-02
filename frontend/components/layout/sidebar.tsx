"use client";

import { useState } from "react";
import {
  LayoutDashboard,
  Trophy,
  Bell,
  Star,
  ChevronLeft,
  ChevronRight,
  Users,
  Calendar,
  Settings as SettingsIcon,
  FileText
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { Separator } from "@/components/ui/separator";

interface SidebarProps {
  currentPage: string;
  onNavigate: (page: string) => void;
  isAdmin?: boolean;
}

interface NavItem {
  id: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  adminOnly?: boolean;
}

const navItems: NavItem[] = [
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "rankings", label: "Classements", icon: Trophy },
  { id: "alerts", label: "Alertes", icon: Bell },
  { id: "favorites", label: "Favoris", icon: Star },
];

const adminNavItems: NavItem[] = [
  { id: "admin-epreuves", label: "Épreuves", icon: Calendar, adminOnly: true },
  { id: "admin-users", label: "Utilisateurs", icon: Users, adminOnly: true },
  { id: "admin-scraping", label: "Scraping", icon: SettingsIcon, adminOnly: true },
];

/**
 * Collapsible sidebar with navigation menu.
 * Displays user OR admin sections based on current page.
 * When on admin page, shows only admin items.
 * When on dashboard/user pages, shows only user items.
 */
export function Sidebar({ currentPage, onNavigate, isAdmin }: SidebarProps) {
  const [isCollapsed, setIsCollapsed] = useState(false);

  // Determine if we're on an admin page
  const isOnAdminPage = currentPage === "admin" || currentPage.startsWith("admin-");

  return (
    <aside
      className={cn(
        "relative flex h-full flex-col border-r bg-card transition-all duration-300",
        isCollapsed ? "w-16" : "w-64"
      )}
    >
      {/* Collapse/Expand button */}
      <Button
        variant="ghost"
        size="icon"
        className="absolute -right-3 top-6 z-10 h-6 w-6 rounded-full border bg-background shadow-md"
        onClick={() => setIsCollapsed(!isCollapsed)}
      >
        {isCollapsed ? (
          <ChevronRight className="h-4 w-4" />
        ) : (
          <ChevronLeft className="h-4 w-4" />
        )}
      </Button>

      {/* Navigation items */}
      <nav className="flex-1 space-y-1 p-3">
        {isOnAdminPage && isAdmin ? (
          // Admin navigation - show ONLY admin items
          <div className="space-y-1">
            {!isCollapsed && (
              <p className="mb-2 px-3 text-xs font-semibold text-muted-foreground">
                ADMINISTRATION
              </p>
            )}
            {adminNavItems.map((item) => (
              <SidebarItem
                key={item.id}
                item={item}
                isActive={currentPage === item.id}
                isCollapsed={isCollapsed}
                onClick={() => onNavigate(item.id)}
              />
            ))}
          </div>
        ) : (
          // User navigation - show ONLY user items
          <div className="space-y-1">
            {!isCollapsed && (
              <p className="mb-2 px-3 text-xs font-semibold text-muted-foreground">
                NAVIGATION
              </p>
            )}
            {navItems.map((item) => (
              <SidebarItem
                key={item.id}
                item={item}
                isActive={currentPage === item.id}
                isCollapsed={isCollapsed}
                onClick={() => onNavigate(item.id)}
              />
            ))}
          </div>
        )}
      </nav>

      {/* Footer info */}
      {!isCollapsed && (
        <div className="border-t p-4">
          <p className="text-xs text-muted-foreground">
            Athle Tracker v1.0
          </p>
        </div>
      )}
    </aside>
  );
}

/**
 * Individual sidebar navigation item.
 */
function SidebarItem({
  item,
  isActive,
  isCollapsed,
  onClick,
}: {
  item: NavItem;
  isActive: boolean;
  isCollapsed: boolean;
  onClick: () => void;
}) {
  const Icon = item.icon;

  return (
    <Button
      variant={isActive ? "secondary" : "ghost"}
      className={cn(
        "w-full justify-start",
        isActive && "bg-primary/10 text-primary hover:bg-primary/20",
        isCollapsed && "justify-center"
      )}
      onClick={onClick}
      title={isCollapsed ? item.label : undefined}
    >
      <Icon className={cn("h-5 w-5", !isCollapsed && "mr-3")} />
      {!isCollapsed && <span>{item.label}</span>}
    </Button>
  );
}
