"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { motion } from "framer-motion";
import { Save, Loader2, FileText, Upload } from "lucide-react";

export default function AdminSettings() {
  const [content, setContent] = useState<any>({
    hero_title: "Hi, I\'m Jenith.",
    hero_headline: "I build software, automate workflows, and explore new technologies.",
    hero_description: "Based in Nepal, studying engineering at Cosmos College of Management and Technology.",
    available_for_work: true,
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [resume, setResume] = useState<File | null>(null);

  useEffect(() => {
    async function fetchSettings() {
      const { data } = await supabase.from(\'settings\').select(\'*\').eq(\'id\', \'homepage\').single();
      if (data) setContent(data.value);
      setLoading(false);
    }
    fetchSettings();
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);

    const { error } = await supabase.from(\'settings\').upsert({
      id: \'homepage\',
      value: content,
      updated_at: new Date().toISOString(),
    });

    if (error) alert(error.message);
    else alert("Homepage content updated successfully!");
    setSaving(false);
  };

  const handleResumeUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const { error } = await supabase.storage
      .from(\'documents\')
      .upload(\'resume.pdf\', file, { upsert: true });

    if (error) alert(error.message);
    else alert("Resume updated successfully!");
  };

  if (loading) return (
    <div className="h-64 flex items-center justify-center">
      <Loader2 className="animate-spin text-white/20" size={48} />
    </div>
  );

  return (
    <div className="space-y-12 max-w-4xl">
      <header>
        <h1 className="text-4xl font-bold tracking-tight mb-2">Settings</h1>
        <p className="text-white/40 font-medium">Customize your portfolio\'s core information.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <section className="p-8 rounded-[40px] border border-white/5 bg-white/[0.02]">
          <div className="flex items-center gap-3 mb-8">
            <div className="w-10 h-10 rounded-xl bg-blue-500/10 flex items-center justify-center text-blue-500">
              <FileText size={20} />
            </div>
            <h2 className="text-xl font-bold tracking-tight">Resume / CV</h2>
          </div>
          <p className="text-sm text-white/40 mb-6 font-medium">Upload your latest resume as a PDF file.</p>

          <div className="relative group">
            <input
              type="file"
              accept=".pdf"
              onChange={handleResumeUpload}
              className="absolute inset-0 opacity-0 cursor-pointer z-10"
            />
            <div className="w-full px-8 py-5 rounded-3xl bg-white/5 border border-dashed border-white/10 group-hover:border-white/20 transition-all flex flex-col items-center justify-center gap-3">
              <Upload size={24} className="text-white/20" />
              <span className="text-white/40 font-bold uppercase tracking-widest text-[10px]">Upload PDF</span>
            </div>
          </div>
        </section>

        <section className="p-8 rounded-[40px] border border-white/5 bg-white/[0.02]">
          <div className="flex items-center gap-3 mb-8">
            <div className="w-10 h-10 rounded-xl bg-green-500/10 flex items-center justify-center text-green-500">
              <Save size={20} />
            </div>
            <h2 className="text-xl font-bold tracking-tight">Homepage Content</h2>
          </div>
          <form onSubmit={handleSave} className="space-y-6">
            <div className="space-y-2">
              <label className="text-xs font-black text-white/20 uppercase tracking-[0.2em]">Hero Title</label>
              <input
                type="text"
                value={content.hero_title}
                onChange={(e) => setContent({ ...content, hero_title: e.target.value })}
                className="w-full px-6 py-4 rounded-2xl bg-white/5 border border-white/5 focus:border-white/20 transition-all outline-none font-bold"
              />
            </div>
            <div className="space-y-2">
              <label className="text-xs font-black text-white/20 uppercase tracking-[0.2em]">Hero Headline</label>
              <input
                type="text"
                value={content.hero_headline}
                onChange={(e) => setContent({ ...content, hero_headline: e.target.value })}
                className="w-full px-6 py-4 rounded-2xl bg-white/5 border border-white/5 focus:border-white/20 transition-all outline-none font-medium"
              />
            </div>
            <button
              type="submit"
              disabled={saving}
              className="w-full py-5 rounded-3xl bg-white text-black font-black hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-2"
            >
              {saving ? <Loader2 className="animate-spin" size={20} /> : "Update Content"}
            </button>
          </form>
        </section>
      </div>
    </div>
  );
}
