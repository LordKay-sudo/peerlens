import { AnalyzeSection } from "@/components/analyze-section";
import { BackgroundMesh } from "@/components/background-mesh";
import { Features } from "@/components/features";
import { Footer } from "@/components/footer";
import { Header } from "@/components/header";
import { Hero } from "@/components/hero";

export default function Home() {
  return (
    <main className="relative min-h-screen overflow-x-hidden">
      <BackgroundMesh />
      <Header />
      <Hero />
      <AnalyzeSection />
      <Features />
      <Footer />
    </main>
  );
}
