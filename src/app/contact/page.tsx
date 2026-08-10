"use client";

import { useState } from "react";
import { supabase } from "@/lib/supabase";
import { motion, AnimatePresence } from "framer-motion";
import { GridBackground } from "@/components/ui/grid-background";
import { ArrowLeft, Loader2, Send, CheckCircle2 } from "lucide-react";
import Link from "next/link";

export default function Contact() {
  const [formData, setFormData] = useState({ name: "", email: "", subject: "", message: "" });
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    const { error } = await supabase.from(\'messages\').insert([formData]);

    if (error) {
      alert(error.message);
    } else {
      setSubmitted(true);
    }
    setLoading(false);
  };

  return (
    <main className="relative min-h-screen px-6 py-24 md:px-12 lg:px-24 max-w-7xl mx-auto flex flex-col items-center">
      <GridBackground />

      <div className="w-full">
        <Link href="/" className="inline-flex items-center gap-2 text-white/40 hover:text-white transition-colors mb-12 group font-medium">
          <ArrowLeft size={20} className="group-hover:-translate-x-1 transition-transform" /> Back Home
        </Link>
      </div>

      <div className="w-full max-w-2xl text-center mb-16">
        <h1 className="text-5xl md:text-7xl font-bold tracking-tighter mb-6 leading-none">Let\'s connect.</h1>
        <p className="text-lg text-white/40 font-medium leading-relaxed">
          Have a question or want to work together? Feel free to reach out and I\'ll get back to you as soon as I can.
        </p>
      </div>

      <AnimatePresence mode="wait">
        {!submitted ? (
          <motion.form
            key="form"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95 }}
            onSubmit={handleSubmit}
            className="w-full max-w-xl space-y-6"
          >
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="text-sm font-bold text-white/40 ml-1 uppercase tracking-widest">Full Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                  className="w-full px-8 py-5 rounded-3xl bg-white/5 border border-white/5 focus:border-white/20 transition-all outline-none font-medium"
                  placeholder="John Doe"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-bold text-white/40 ml-1 uppercase tracking-widest">Email Address</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  required
                  className="w-full px-8 py-5 rounded-3xl bg-white/5 border border-white/5 focus:border-white/20 transition-all outline-none font-medium"
                  placeholder="john@example.com"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-bold text-white/40 ml-1 uppercase tracking-widest">Subject</label>
              <input
                type="text"
                value={formData.subject}
                onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                required
                className="w-full px-8 py-5 rounded-3xl bg-white/5 border border-white/5 focus:border-white/20 transition-all outline-none font-medium"
                placeholder="Collaborating on a project"
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-bold text-white/40 ml-1 uppercase tracking-widest">Message</label>
              <textarea
                value={formData.message}
                onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                required
                rows={6}
                className="w-full px-8 py-5 rounded-[40px] bg-white/5 border border-white/5 focus:border-white/20 transition-all outline-none resize-none font-medium"
                placeholder="Tell me more about what you have in mind..."
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-6 rounded-[40px] bg-white text-black font-black text-xl hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 flex items-center justify-center gap-3 shadow-2xl shadow-white/10"
            >
              {loading ? <Loader2 className="animate-spin" size={24} /> : (
                <>Send Message <Send size={20} /></>
              )}
            </button>
          </motion.form>
        ) : (
          <motion.div
            key="success"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="w-full max-w-xl p-12 rounded-[50px] bg-white/[0.02] border border-white/10 text-center flex flex-col items-center gap-6"
          >
            <div className="w-24 h-24 rounded-[40px] bg-green-500/10 flex items-center justify-center text-green-500 mb-4">
              <CheckCircle2 size={48} />
            </div>
            <h2 className="text-3xl font-black tracking-tight">Message Sent!</h2>
            <p className="text-lg text-white/40 font-medium">
              Thank you for reaching out. I\'ll get back to you shortly.
            </p>
            <button
              onClick={() => setSubmitted(false)}
              className="mt-6 text-white font-bold hover:underline"
            >
              Send another message
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  );
}
