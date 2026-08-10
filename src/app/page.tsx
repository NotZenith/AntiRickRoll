"use client";

import { motion } from "framer-motion";
import { GridBackground } from "@/components/ui/grid-background";
import { Github, Instagram, Linkedin, Mail, ExternalLink, Camera, Code, Cpu } from "lucide-react";
import Link from "next/link";

export default function Home() {
  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.3,
      },
    },
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0, transition: { duration: 0.8, ease: [0.16, 1, 0.3, 1] } },
  };

  return (
    <main className="relative min-h-screen px-6 py-24 md:px-12 lg:px-24 max-w-7xl mx-auto overflow-hidden">
      <GridBackground />

      <motion.div
        variants={container}
        initial="hidden"
        animate="show"
        className="space-y-24"
      >
        {/* Hero Section */}
        <section className="relative pt-12 md:pt-24">
          <motion.div variants={item} className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-white/10 bg-white/5 backdrop-blur-sm mb-6">
            <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
            <span className="text-xs font-medium text-white/60 tracking-wider uppercase">Available for work</span>
          </motion.div>

          <motion.h1 variants={item} className="text-5xl md:text-8xl font-bold tracking-tighter mb-8 leading-[0.9]">
            Hi, I\'m Jenith.<br />
            <span className="text-white/40">I build tools for the future.</span>
          </motion.h1>

          <motion.p variants={item} className="max-w-2xl text-lg md:text-xl text-white/60 leading-relaxed mb-12">
            Engineering student from Nepal. I build software, automate workflows, and explore new technologies. Currently studying at Cosmos College.
          </motion.p>

          <motion.div variants={item} className="flex flex-wrap gap-4">
            <Link href="/projects" className="group relative px-8 py-4 rounded-full bg-white text-black font-semibold overflow-hidden transition-all hover:scale-[1.02] active:scale-[0.98]">
              <span className="relative z-10 flex items-center gap-2">
                Explore Projects <ExternalLink size={18} />
              </span>
            </Link>
            <Link href="/contact" className="px-8 py-4 rounded-full border border-white/10 bg-white/5 backdrop-blur-sm text-white font-semibold transition-all hover:bg-white/10 hover:scale-[1.02] active:scale-[0.98]">
              Get in Touch
            </Link>
          </motion.div>

          <motion.div variants={item} className="flex gap-6 mt-16 text-white/40">
            <a href="https://github.com/NotZenith" target="_blank" className="hover:text-white transition-colors"><Github size={24} /></a>
            <a href="https://linkedin.com/in/notzenith" target="_blank" className="hover:text-white transition-colors"><Linkedin size={24} /></a>
            <a href="https://instagram.com/not.zenith" target="_blank" className="hover:text-white transition-colors"><Instagram size={24} /></a>
            <a href="mailto:notzenith69@gmail.com" className="hover:text-white transition-colors"><Mail size={24} /></a>
          </motion.div>
        </section>

        {/* Areas of Interest */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <motion.div variants={item} className="group p-8 rounded-3xl border border-white/5 bg-white/[0.02] transition-all hover:bg-white/[0.04] hover:border-white/10">
            <div className="w-12 h-12 rounded-2xl bg-blue-500/10 flex items-center justify-center text-blue-500 mb-6 group-hover:scale-110 transition-transform">
              <Code size={24} />
            </div>
            <h3 className="text-xl font-bold mb-3 tracking-tight">Software Engineering</h3>
            <p className="text-white/40 leading-relaxed">Designing clean, scalable architectures with modern frameworks.</p>
          </motion.div>

          <motion.div variants={item} className="group p-8 rounded-3xl border border-white/5 bg-white/[0.02] transition-all hover:bg-white/[0.04] hover:border-white/10">
            <div className="w-12 h-12 rounded-2xl bg-purple-500/10 flex items-center justify-center text-purple-500 mb-6 group-hover:scale-110 transition-transform">
              <Cpu size={24} />
            </div>
            <h3 className="text-xl font-bold mb-3 tracking-tight">System Automation</h3>
            <p className="text-white/40 leading-relaxed">Automating workflows and optimizing development pipelines.</p>
          </motion.div>

          <motion.div variants={item} className="group p-8 rounded-3xl border border-white/5 bg-white/[0.02] transition-all hover:bg-white/[0.04] hover:border-white/10">
            <div className="w-12 h-12 rounded-2xl bg-orange-500/10 flex items-center justify-center text-orange-500 mb-6 group-hover:scale-110 transition-transform">
              <Camera size={24} />
            </div>
            <h3 className="text-xl font-bold mb-3 tracking-tight">Photography</h3>
            <p className="text-white/40 leading-relaxed">Capturing moments and exploring visual storytelling through my lens.</p>
          </motion.div>
        </section>

        {/* Featured Projects Link */}
        <motion.section variants={item} className="border-t border-white/10 pt-24 pb-12 text-center">
          <h2 className="text-3xl font-bold tracking-tight mb-8">Ready to see what I\'ve been working on?</h2>
          <Link href="/projects" className="inline-flex items-center gap-2 text-white group">
            Browse all projects <motion.span className="group-hover:translate-x-1 transition-transform">→</motion.span>
          </Link>
        </motion.section>
      </motion.div>
    </main>
  );
}
