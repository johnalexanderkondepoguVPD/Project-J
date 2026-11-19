"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { getExaminations, Examination } from "@/lib/exams";
import { 
  Search, 
  Filter, 
  ExternalLink, 
  ArrowLeft, 
  Building2, 
  Calendar, 
  BookOpen, 
  GraduationCap,
  ChevronRight,
  ShieldAlert,
  Loader2
} from "lucide-react";

const EXAM_TYPES = ["All", "UPSC", "SSC", "Banking", "Railways", "NTA", "State PSC"];

// Fallback catalog for preview if backend is not actively running
const FALLBACK_EXAMS: Examination[] = [
  {
    id: 1,
    name: "Civil Services Examination",
    abbreviation: "UPSC CSE",
    conducting_body: "Union Public Service Commission",
    exam_type: "UPSC",
    level: "National",
    subject: "General Studies & Optional",
    frequency: "Annual",
    eligibility_criteria: "Bachelor's degree from a recognized university. Age 21-32.",
    syllabus: "Indian History, Polity, Geography, Economy, Environment, CSAT.",
    official_website: "https://upsc.gov.in",
    is_active: true,
  },
  {
    id: 2,
    name: "Combined Graduate Level Examination",
    abbreviation: "SSC CGL",
    conducting_body: "Staff Selection Commission",
    exam_type: "SSC",
    level: "National",
    subject: "Reasoning, Quantitative Aptitude, English, GA",
    frequency: "Annual",
    eligibility_criteria: "Graduation in any discipline. Age 18-32.",
    syllabus: "General Intelligence & Reasoning, Quantitative Aptitude, General Awareness.",
    official_website: "https://ssc.gov.in",
    is_active: true,
  },
  {
    id: 3,
    name: "Probationary Officers / Management Trainees",
    abbreviation: "IBPS PO",
    conducting_body: "Institute of Banking Personnel Selection",
    exam_type: "Banking",
    level: "National",
    subject: "Quant, Reasoning, Banking Awareness, English",
    frequency: "Annual",
    eligibility_criteria: "Graduate in any stream. Age 20-30.",
    syllabus: "Data Analysis, Reasoning, English, Banking & Economic Awareness.",
    official_website: "https://ibps.in",
    is_active: true,
  },
  {
    id: 4,
    name: "Non-Technical Popular Categories",
    abbreviation: "RRB NTPC",
    conducting_body: "Railway Recruitment Boards",
    exam_type: "Railways",
    level: "National",
    subject: "Mathematics, General Intelligence, Awareness",
    frequency: "Biennial",
    eligibility_criteria: "12th or Graduate. Age 18-33.",
    syllabus: "Arithmetic, Reasoning, Current Affairs, Indian Railways general info.",
    official_website: "https://indianrailways.gov.in",
    is_active: true,
  },
];

export default function ExaminationsPage() {
  const [exams, setExams] = useState<Examination[]>(FALLBACK_EXAMS);
  const [search, setSearch] = useState("");
  const [selectedType, setSelectedType] = useState("All");
  const [loading, setLoading] = useState(false);
  const [selectedExam, setSelectedExam] = useState<Examination | null>(null);

  useEffect(() => {
    let isMounted = true;
    async function load() {
      setLoading(true);
      try {
        const queryParams: any = {};
        if (search) queryParams.q = search;
        if (selectedType !== "All") queryParams.exam_type = selectedType;

        const data = await getExaminations(queryParams);
        if (isMounted && data.items.length > 0) {
          setExams(data.items);
        }
      } catch {
        // Fallback filtering if backend is unreachable
        if (isMounted) {
          let filtered = FALLBACK_EXAMS;
          if (selectedType !== "All") {
            filtered = filtered.filter((e) => e.exam_type === selectedType);
          }
          if (search) {
            const s = search.toLowerCase();
            filtered = filtered.filter(
              (e) =>
                e.name.toLowerCase().includes(s) ||
                (e.abbreviation && e.abbreviation.toLowerCase().includes(s)) ||
                e.conducting_body.toLowerCase().includes(s)
            );
          }
          setExams(filtered);
        }
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    const timer = setTimeout(load, 200);
    return () => {
      isMounted = false;
      clearTimeout(timer);
    };
  }, [search, selectedType]);

  return (
    <main className="min-h-screen bg-background text-foreground">
      <div className="max-w-7xl mx-auto p-4 sm:p-6 lg:p-8">
        {/* Navigation Bar */}
        <div className="flex items-center justify-between mb-8 pb-4 border-b border-border">
          <Link
            href="/"
            className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Overview</span>
          </Link>
          <div className="flex items-center gap-3">
            <Link
              href="/login"
              className="text-sm font-medium hover:text-primary transition"
            >
              Sign In
            </Link>
            <Link
              href="/register"
              className="px-3.5 py-1.5 text-xs font-medium bg-primary text-primary-foreground rounded-lg hover:opacity-90 transition"
            >
              Register
            </Link>
          </div>
        </div>

        {/* Header */}
        <header className="mb-8">
          <h1 className="text-3xl sm:text-4xl font-bold tracking-tight mb-2">
            Government Examination Catalog
          </h1>
          <p className="text-muted-foreground max-w-3xl">
            Explore and track official examination bodies, recruitment notices, syllabus guidelines, and verified patterns across India.
          </p>
        </header>

        {/* Filters and Search Bar */}
        <div className="flex flex-col md:flex-row gap-4 mb-8">
          <div className="relative flex-1">
            <Search className="w-4 h-4 absolute left-3 top-3 text-muted-foreground" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by exam name, acronym (e.g. UPSC, SSC CGL), or conducting body..."
              className="w-full pl-9 pr-4 py-2 rounded-lg border border-input bg-card text-sm focus:outline-none focus:ring-2 focus:ring-primary shadow-sm"
            />
          </div>

          <div className="flex items-center gap-2 overflow-x-auto pb-2 md:pb-0">
            {EXAM_TYPES.map((type) => (
              <button
                key={type}
                onClick={() => setSelectedType(type)}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition ${
                  selectedType === type
                    ? "bg-primary text-primary-foreground shadow-sm"
                    : "border border-border bg-card hover:bg-muted text-muted-foreground"
                }`}
              >
                {type}
              </button>
            ))}
          </div>
        </div>

        {/* Loading Spinner */}
        {loading && (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="w-6 h-6 animate-spin text-primary" />
          </div>
        )}

        {/* Examination Cards Grid */}
        {!loading && exams.length === 0 ? (
          <div className="text-center py-16 border border-dashed border-border rounded-xl">
            <p className="text-muted-foreground">No examinations match your current filters.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {exams.map((exam) => (
              <div
                key={exam.id}
                onClick={() => setSelectedExam(exam)}
                className="bg-card border border-border rounded-xl p-6 shadow-sm hover:border-primary hover:shadow-md transition cursor-pointer flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-start justify-between gap-2 mb-3">
                    <span className="inline-block px-2.5 py-0.5 rounded-md text-xs font-semibold bg-primary/10 text-primary">
                      {exam.abbreviation || exam.exam_type}
                    </span>
                    <span className="text-xs text-muted-foreground font-medium">
                      {exam.level}
                    </span>
                  </div>

                  <h3 className="font-semibold text-lg mb-1 leading-snug">
                    {exam.name}
                  </h3>

                  <p className="text-xs text-muted-foreground flex items-center gap-1.5 mb-4">
                    <Building2 className="w-3.5 h-3.5 shrink-0" />
                    <span className="truncate">{exam.conducting_body}</span>
                  </p>

                  {exam.syllabus && (
                    <p className="text-xs text-muted-foreground line-clamp-2 mb-4 bg-muted/40 p-2.5 rounded-lg">
                      {exam.syllabus}
                    </p>
                  )}
                </div>

                <div className="pt-4 border-t border-border flex items-center justify-between text-xs text-primary font-medium">
                  <span>View Syllabus & Pattern</span>
                  <ChevronRight className="w-4 h-4" />
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Detailed Modal Drawer */}
        {selectedExam && (
          <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
            <div className="bg-card border border-border rounded-2xl max-w-2xl w-full max-h-[85vh] overflow-y-auto p-6 sm:p-8 shadow-xl">
              <div className="flex items-start justify-between gap-4 mb-4">
                <div>
                  <span className="px-2.5 py-0.5 rounded text-xs font-semibold bg-primary/10 text-primary mb-2 inline-block">
                    {selectedExam.abbreviation || selectedExam.exam_type}
                  </span>
                  <h2 className="text-2xl font-bold">{selectedExam.name}</h2>
                  <p className="text-sm text-muted-foreground mt-1">
                    Conducting Body: {selectedExam.conducting_body}
                  </p>
                </div>
                <button
                  onClick={() => setSelectedExam(null)}
                  className="text-muted-foreground hover:text-foreground text-sm p-1"
                >
                  ✕
                </button>
              </div>

              <div className="space-y-4 my-6 text-sm">
                {selectedExam.eligibility_criteria && (
                  <div>
                    <h4 className="font-semibold flex items-center gap-2 mb-1">
                      <GraduationCap className="w-4 h-4 text-primary" />
                      Eligibility Criteria
                    </h4>
                    <p className="text-muted-foreground bg-muted/40 p-3 rounded-lg text-xs">
                      {selectedExam.eligibility_criteria}
                    </p>
                  </div>
                )}

                {selectedExam.syllabus && (
                  <div>
                    <h4 className="font-semibold flex items-center gap-2 mb-1">
                      <BookOpen className="w-4 h-4 text-primary" />
                      Syllabus Overview
                    </h4>
                    <p className="text-muted-foreground bg-muted/40 p-3 rounded-lg text-xs leading-relaxed">
                      {selectedExam.syllabus}
                    </p>
                  </div>
                )}

                {selectedExam.frequency && (
                  <div>
                    <h4 className="font-semibold flex items-center gap-2 mb-1">
                      <Calendar className="w-4 h-4 text-primary" />
                      Examination Frequency
                    </h4>
                    <p className="text-muted-foreground text-xs">{selectedExam.frequency}</p>
                  </div>
                )}
              </div>

              <div className="flex items-center justify-between pt-4 border-t border-border">
                {selectedExam.official_website ? (
                  <a
                    href={selectedExam.official_website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1.5 text-xs text-primary hover:underline font-medium"
                  >
                    <span>Official Portal</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                ) : (
                  <div />
                )}
                <button
                  onClick={() => setSelectedExam(null)}
                  className="px-4 py-2 bg-primary text-primary-foreground text-xs font-medium rounded-lg hover:opacity-90 transition"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
