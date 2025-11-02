/**
 * Type definitions for Athle Tracker application.
 */

export interface User {
  id: number;
  email: string;
  role: "admin" | "user";
  created_at: string;
}

export interface Athlete {
  id: number;
  name: string;
  created_at: string;
}

export interface Epreuve {
  id: number;
  code: number;
  nom: string;
  is_active: boolean;
  created_at: string;
}

export interface Ranking {
  id: number;
  epreuve_code: number;
  athlete_id: number;
  sexe: "M" | "F";
  rank: number;
  performance: string;
  performance_numeric: number;
  club?: string;
  ligue?: string;
  departement?: string;
  scrape_date: string;
  athlete: Athlete;
}

export interface Alert {
  id: number;
  user_id: number;
  alert_type: "critique" | "important" | "info";
  title: string;
  message: string;
  is_read: boolean;
  created_at: string;
}

export interface ScrapeLog {
  id: number;
  epreuve_code: number;
  sexe: "M" | "F";
  scrape_date: string;
  status: "success" | "error";
  results_count: number;
  duration_seconds: number;
  error_message?: string;
}

export interface ScrapeResult {
  success: boolean;
  rankings_count: number;
  alerts_count: number;
  duration_seconds: number;
  error?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}
