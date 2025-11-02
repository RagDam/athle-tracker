"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

/**
 * Root page - redirects to login or dashboard based on auth status.
 */
export default function Home() {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("auth_token");

    if (token) {
      router.push("/dashboard");
    } else {
      router.push("/login");
    }
  }, [router]);

  return (
    <div className="flex min-h-screen items-center justify-center">
      <p>Redirection...</p>
    </div>
  );
}
