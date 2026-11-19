import Link from "next/link";
import { 
  ChevronDown,
  Search,
  Clipboard, 
  Calendar,
  TrendingUp,
  Shield,
  ChartBar,
  Users,
  Folder,
  Brain,
  Microscope
} from "lucide-react";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-background text-foreground">
      <div className="max-w-7xl mx-auto p-4 sm:p-6 lg:p-8">
        <header className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-4xl sm:text-5xl font-bold tracking-tighter">
                Project-J
              </h1>
              <p className="text-sm text-muted-foreground">
                AI Government Exam Intelligence Platform
              </p>
            </div>
            <div className="flex items-center gap-3">
              <Link
                href="/login"
                className="px-4 py-2 text-sm font-medium border border-border rounded-lg hover:bg-muted transition"
              >
                Sign In
              </Link>
              <Link
                href="/register"
                className="px-4 py-2 text-sm font-medium bg-primary text-primary-foreground rounded-lg hover:opacity-90 transition"
              >
                Register
              </Link>
            </div>
          </div>
          <div className="flex items-center gap-4 mt-4">
            <p className="text-lg text-muted-foreground max-w-2xl">
              Discover, analyze, and prepare for government examinations with AI-powered
              pattern analysis, question paper collection, and mock test generation.
            </p>
            <Link
              href="/exams"
              className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-medium border border-primary text-primary hover:bg-primary/10 rounded-lg transition"
            >
              <Search className="w-4 h-4" />
              <span>Explore Exams</span>
            </Link>
          </div>
        </header>

        <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Examination Discovery Card */}
          <Link href="/exams" className="block">
            <div className="card hover:border-primary hover:shadow-md transition duration-300 h-full">
              <div className="p-6">
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                    <Shield className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <h3 className="font-medium mb-1">Examination Discovery</h3>
                    <p className="text-sm text-muted-foreground">
                      Automated discovery of government examinations across bodies and regions
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </Link>

          {/* Question Paper Collection Card */}
          <div className="card hover:card-lg hover:transition-transform duration-300">
            <div className="p-6">
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                  <Folder className="w-5 h-5 text-primary" />
                </div>
                <div>
                  <h3 className="font-medium mb-1">Question Paper Collection</h3>
                  <p className="text-sm text-muted-foreground">
                    Scraping and collection of previous-year question papers
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Pattern Analysis Card */}
          <div className="card hover:card-lg hover:transition-transform duration-300">
            <div className="p-6">
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                  <ChartBar className="w-5 h-5 text-primary" />
                </div>
                <div>
                  <h3 className="font-medium mb-1">Pattern Analysis</h3>
                  <p className="text-sm text-muted-foreground">
                    AI-powered analysis of examination patterns and trends
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Mock Test Generation Card */}
          <div className="card hover:card-lg hover:transition-transform duration-300">
            <div className="p-6">
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                  <Brain className="w-5 h-5 text-primary" />
                </div>
                <div>
                  <h3 className="font-medium mb-1">AI Mock Tests</h3>
                  <p className="text-sm text-muted-foreground">
                    Generate AI-powered mock tests with detailed explanations
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* OCR & Document Processing Card */}
          <div className="card hover:card-lg hover:transition-transform duration-300">
            <div className="p-6">
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                  <Microscope className="w-5 h-5 text-primary" />
                </div>
                <div>
                  <h3 className="font-medium mb-1">OCR & Document Processing</h3>
                  <p className="text-sm text-muted-foreground">
                    PaddleOCR and document digitization for scanned papers
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* AI Analysis Card */}
          <div className="card hover:card-lg hover:transition-transform duration-300">
            <div className="p-6">
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                  <Brain className="w-5 h-5 text-primary" />
                </div>
                <div>
                  <h3 className="font-medium mb-1">AI Analysis</h3>
                  <p className="text-sm text-muted-foreground">
                    Detailed explanations, answer verification, and pattern insights
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}