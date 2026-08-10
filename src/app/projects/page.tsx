"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { motion } from "framer-motion";
import { GridBackground } from "@/components/ui/grid-background";
import { Github, ExternalLink, Loader2, ArrowLeft } from "lucide-react";
import Link from "next/link";

export default function Projects() {
  const [projects, setProjects] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchProjects() {
      const { data } = await supabase
        .from(\'projects\')
        .select(\'*\')
        .order(\'order\', { ascending: true });
      setProjects(data || []);
      setLoading(false);
    }
    fetchProjects();
  }, []);

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.1 },
    },
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0, transition: { duration: 0.8, ease: [0.16, 1, 0.3, 1] } },
  };

  return (
    <main className="relative min-h-screen px-6 py-24 md:px-12 lg:px-24 max-w-7xl mx-auto">
      <GridBackground />

      <Link href="/" className="inline-flex items-center gap-2 text-white/40 hover:text-white transition-colors mb-12 group font-medium">
        <ArrowLeft size={20} className="group-hover:-translate-x-1 transition-transform" /> Back Home
      </Link>

      <header className="mb-24">
        <h1 className="text-5xl md:text-7xl font-bold tracking-tighter mb-6 leading-none">Projects.</h1>
        <p className="max-w-2xl text-lg text-white/40 font-medium leading-relaxed">
          A collection of tools, applications, and experiments I\'ve built to solve problems or explore new ideas.
        </p>
      </header>

      {loading ? (
        <div className="h-64 flex items-center justify-center">
          <Loader2 className="animate-spin text-white/20" size={48} />
        </div>
      ) : (
        <motion.div
          variants={container}
          initial="hidden"
          animate="show"
          className="grid grid-cols-1 md:grid-cols-2 gap-8"
        >
          {projects.map((project) => (
            <motion.div
              key={project.id}
              variants={item}
              className="group p-8 rounded-[40px] border border-white/5 bg-white/[0.02] hover:bg-white/[0.04] hover:border-white/10 transition-all flex flex-col h-full"
            >
              <div className="aspect-[16/10] rounded-[32px] overflow-hidden bg-white/5 mb-8 border border-white/5 relative">
                {project.thumbnail_url ? (
                  <img src={project.thumbnail_url} alt="" className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" />
                ) : (
                  <div className="absolute inset-0 flex items-center justify-center text-white/5 font-black text-4xl">AR</div>
                )}
              </div>

              <div className="flex-1">
                <h3 className="text-2xl font-bold tracking-tight mb-3">{project.title}</h3>
                <p className="text-white/40 leading-relaxed font-medium mb-8 line-clamp-3">{project.description}</p>
              </div>

              <div className="flex items-center justify-between mt-auto pt-6 border-t border-white/5">
                <div className="flex gap-4">
                  {project.github_url && (
                    <a href={project.github_url} target="_blank" className="p-3 rounded-2xl bg-white/5 text-white/40 hover:text-white transition-all">
                      <Github size={20} />
                    </a>
                  )}
                  {project.live_url && (
                    <a href={project.live_url} target="_blank" className="p-3 rounded-2xl bg-white/5 text-white/40 hover:text-white transition-all">
                      <ExternalLink size={20} />
                    </a>
                  )}
                </div>
                <div className="flex flex-wrap gap-2 justify-end">
                  {project.technologies?.slice(0, 3).map((tech: string) => (
                    <span key={tech} className="px-3 py-1 rounded-full bg-white/5 text-[10px] font-black uppercase tracking-widest text-white/20">
                      {tech}
                    </span>
                  ))}
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>
      )}
    </main>
  );
}
