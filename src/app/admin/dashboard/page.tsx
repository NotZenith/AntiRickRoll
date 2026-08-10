"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { motion } from "framer-motion";
import {
  FolderGit2,
  Camera,
  MessageSquare,
  Eye,
  ArrowUpRight,
  TrendingUp,
  Clock
} from "lucide-react";

export default function AdminDashboard() {
  const [stats, setStats] = useState({
    projects: 0,
    photos: 0,
    messages: 0,
    visitors: 1240, // Mock for now, integrate with Plausible/Vercel Analytics later
  });

  useEffect(() => {
    async function fetchStats() {
      const { count: projectsCount } = await supabase.from(\'projects\').select(\'*\', { count: \'exact\', head: true });
      const { count: photosCount } = await supabase.from(\'photos\').select(\'*\', { count: \'exact\', head: true });
      const { count: messagesCount } = await supabase.from(\'messages\').select(\'*\', { count: \'exact\', head: true });

      setStats({
        projects: projectsCount || 0,
        photos: photosCount || 0,
        messages: messagesCount || 0,
        visitors: 1240,
      });
    }

    fetchStats();
  }, []);

  const cards = [
    { label: "Total Projects", value: stats.projects, icon: FolderGit2, color: "text-blue-500", bg: "bg-blue-500/10" },
    { label: "Gallery Items", value: stats.photos, icon: Camera, color: "text-purple-500", bg: "bg-purple-500/10" },
    { label: "New Messages", value: stats.messages, icon: MessageSquare, color: "text-orange-500", bg: "bg-orange-500/10" },
    { label: "Unique Visitors", value: stats.visitors, icon: Eye, color: "text-green-500", bg: "bg-green-500/10" },
  ];

  return (
    <div className="space-y-12">
      <header>
        <h1 className="text-4xl font-bold tracking-tight mb-2">Welcome back, Jenith</h1>
        <p className="text-white/40 font-medium">Here\'s what\'s happening with your portfolio.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {cards.map((card, i) => (
          <motion.div
            key={card.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="p-8 rounded-3xl border border-white/5 bg-white/[0.02] relative overflow-hidden group hover:border-white/10 transition-all"
          >
            <div className={`w-12 h-12 rounded-2xl ${card.bg} flex items-center justify-center ${card.color} mb-6`}>
              <card.icon size={24} />
            </div>
            <p className="text-white/40 text-sm font-medium mb-1">{card.label}</p>
            <p className="text-3xl font-bold tracking-tight">{card.value}</p>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 p-8 rounded-3xl border border-white/5 bg-white/[0.02]">
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-blue-500/10 flex items-center justify-center text-blue-500">
                <TrendingUp size={20} />
              </div>
              <h2 className="text-xl font-bold tracking-tight">Analytics Overview</h2>
            </div>
            <button className="text-sm text-white/40 hover:text-white transition-colors flex items-center gap-1 font-medium">
              View Detailed Report <ArrowUpRight size={16} />
            </button>
          </div>
          <div className="h-64 flex items-center justify-center border border-dashed border-white/10 rounded-2xl">
            <p className="text-white/20 font-medium italic">Vercel Analytics Integration Coming Soon</p>
          </div>
        </div>

        <div className="p-8 rounded-3xl border border-white/5 bg-white/[0.02]">
          <div className="flex items-center gap-3 mb-8">
            <div className="w-10 h-10 rounded-xl bg-orange-500/10 flex items-center justify-center text-orange-500">
              <Clock size={20} />
            </div>
            <h2 className="text-xl font-bold tracking-tight">Recent Activity</h2>
          </div>
          <div className="space-y-6">
            <div className="flex gap-4">
              <div className="w-2 h-2 rounded-full bg-blue-500 mt-2 shrink-0" />
              <div>
                <p className="text-sm font-medium">Project "Portfolio v2" updated</p>
                <p className="text-xs text-white/40">2 hours ago</p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="w-2 h-2 rounded-full bg-green-500 mt-2 shrink-0" />
              <div>
                <p className="text-sm font-medium">New photo "Himalayas" uploaded</p>
                <p className="text-xs text-white/40">5 hours ago</p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="w-2 h-2 rounded-full bg-orange-500 mt-2 shrink-0" />
              <div>
                <p className="text-sm font-medium">Message received from Alice</p>
                <p className="text-xs text-white/40">Yesterday</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
