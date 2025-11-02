"use client";

import { ReactNode } from "react";
import { Header } from "./header";
import { Sidebar } from "./sidebar";

interface MainLayoutProps {
  children: ReactNode;
  user?: {
    email: string;
    role: "admin" | "user";
  };
  currentPage: string;
  onNavigate: (page: string) => void;
  onLogout: () => void;
}

/**
 * Main application layout with full-width header and collapsible sidebar.
 *
 * Layout structure:
 * - Header: Full-width, fixed at top, gradient background
 * - Content area: Flexbox with sidebar (left) and main content (right)
 * - Sidebar: Collapsible navigation menu
 */
export function MainLayout({
  children,
  user,
  currentPage,
  onNavigate,
  onLogout,
}: MainLayoutProps) {
  const headerPage = currentPage.startsWith("admin-") ? "admin" : "dashboard";

  return (
    <div className="flex h-screen flex-col">
      {/* Full-width header */}
      <Header
        user={user}
        currentPage={headerPage}
        onNavigate={onNavigate}
        onLogout={onLogout}
      />

      {/* Content area with sidebar + main content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <Sidebar
          currentPage={currentPage}
          onNavigate={onNavigate}
          isAdmin={user?.role === "admin"}
        />

        {/* Main content */}
        <main className="flex-1 overflow-y-auto bg-background p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
