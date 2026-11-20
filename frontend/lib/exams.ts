const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Examination {
  id: number;
  name: string;
  abbreviation?: string | null;
  conducting_body: string;
  exam_type: string;
  level: string;
  subject?: string | null;
  frequency?: string | null;
  eligibility_criteria?: string | null;
  exam_pattern?: Record<string, any> | null;
  syllabus?: string | null;
  official_website?: string | null;
  is_active: boolean;
  created_at?: string | null;
  updated_at?: string | null;
}

export interface PaginatedExaminations {
  items: Examination[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface ExamBodySummary {
  conducting_body: string;
  exam_type: string;
  exam_count: number;
}

export interface ExamQueryParams {
  q?: string;
  conducting_body?: string;
  exam_type?: string;
  level?: string;
  is_active?: boolean;
  page?: number;
  page_size?: number;
}

export async function getExaminations(params: ExamQueryParams = {}): Promise<PaginatedExaminations> {
  const query = new URLSearchParams();
  if (params.q) query.set("q", params.q);
  if (params.conducting_body) query.set("conducting_body", params.conducting_body);
  if (params.exam_type) query.set("exam_type", params.exam_type);
  if (params.level) query.set("level", params.level);
  if (params.is_active !== undefined) query.set("is_active", String(params.is_active));
  if (params.page) query.set("page", String(params.page));
  if (params.page_size) query.set("page_size", String(params.page_size));

  const res = await fetch(`${API_BASE}/api/v1/exams?${query.toString()}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    throw new Error("Failed to load examinations");
  }
  return await res.json();
}

export async function getExaminationById(id: number): Promise<Examination> {
  const res = await fetch(`${API_BASE}/api/v1/exams/${id}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    throw new Error("Examination not found");
  }
  return await res.json();
}

export async function getConductingBodies(): Promise<ExamBodySummary[]> {
  const res = await fetch(`${API_BASE}/api/v1/exams/bodies`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    return [];
  }
  return await res.json();
}
