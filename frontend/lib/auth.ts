const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface User {
  id: string;
  email: string;
  username: string;
  full_name?: string | null;
  is_active: boolean;
  is_verified: boolean;
  created_at?: string | null;
}

export interface RegisterInput {
  email: string;
  username: string;
  full_name?: string;
  password: string;
}

export interface LoginInput {
  identifier: string; // username or email
  password: string;
}

export async function registerUser(input: RegisterInput): Promise<User> {
  const res = await fetch(`${API_BASE}/api/v1/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(input),
  });

  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || "Registration failed");
  }
  return data;
}

export async function loginUser(input: LoginInput): Promise<User> {
  const res = await fetch(`${API_BASE}/api/v1/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(input),
  });

  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || "Login failed");
  }
  return data;
}

export async function logoutUser(): Promise<void> {
  const res = await fetch(`${API_BASE}/api/v1/auth/logout`, {
    method: "POST",
    credentials: "include",
  });
  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.detail || "Logout failed");
  }
}

export async function getCurrentUser(): Promise<User | null> {
  try {
    const res = await fetch(`${API_BASE}/api/v1/auth/me`, {
      method: "GET",
      credentials: "include",
    });

    if (!res.ok) {
      return null;
    }
    return await res.json();
  } catch {
    return null;
  }
}
