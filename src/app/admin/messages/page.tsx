"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { motion, AnimatePresence } from "framer-motion";
import {
  Trash2,
  Loader2,
  Mail,
  User,
  Clock,
  CheckCircle2,
  Archive,
  MoreVertical
} from "lucide-react";

export default function AdminMessages() {
  const [messages, setMessages] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMessages();
  }, []);

  async function fetchMessages() {
    setLoading(true);
    const { data, error } = await supabase
      .from(\'messages\')
      .select(\'*\')
      .order(\'created_at\', { ascending: false });

    if (error) console.error(error);
    else setMessages(data || []);
    setLoading(false);
  }

  const handleDelete = async (id: string) => {
    if (!confirm("Delete this message?")) return;
    const { error } = await supabase.from(\'messages\').delete().eq(\'id\', id);
    if (error) alert(error.message);
    else fetchMessages();
  };

  const toggleRead = async (id: string, currentStatus: boolean) => {
    const { error } = await supabase
      .from(\'messages\')
      .update({ read: !currentStatus })
      .eq(\'id\', id);
    if (error) alert(error.message);
    else fetchMessages();
  };

  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-4xl font-bold tracking-tight mb-2">Inbox</h1>
        <p className="text-white/40 font-medium">Messages from your visitors.</p>
      </header>

      {loading ? (
        <div className="h-64 flex items-center justify-center">
          <Loader2 className="animate-spin text-white/20" size={48} />
        </div>
      ) : (
        <div className="space-y-4">
          {messages.map((msg) => (
            <motion.div
              key={msg.id}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              className={`p-6 rounded-3xl border transition-all ${
                msg.read
                  ? "border-white/5 bg-white/[0.01] opacity-60"
                  : "border-blue-500/30 bg-blue-500/[0.02] shadow-[0_0_20px_rgba(59,130,246,0.05)]"
              }`}
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-4">
                  <div className={`w-12 h-12 rounded-2xl flex items-center justify-center ${msg.read ? "bg-white/5 text-white/20" : "bg-blue-500/20 text-blue-500"}`}>
                    <User size={20} />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold tracking-tight">{msg.name}</h3>
                    <p className="text-white/40 text-sm font-medium">{msg.email}</p>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => toggleRead(msg.id, msg.read)}
                    className={`p-2 rounded-lg transition-all ${msg.read ? "text-white/20 hover:text-white" : "text-blue-500 hover:bg-blue-500/10"}`}
                    title={msg.read ? "Mark as unread" : "Mark as read"}
                  >
                    <CheckCircle2 size={20} />
                  </button>
                  <button
                    onClick={() => handleDelete(msg.id)}
                    className="p-2 rounded-lg text-white/20 hover:text-red-400 hover:bg-red-400/10 transition-all"
                  >
                    <Trash2 size={20} />
                  </button>
                </div>
              </div>

              <div className="pl-16 space-y-4">
                {msg.subject && <p className="font-bold text-white/80">{msg.subject}</p>}
                <p className="text-white/60 leading-relaxed font-medium whitespace-pre-wrap">{msg.message}</p>
                <div className="flex items-center gap-2 text-white/20 text-xs font-bold uppercase tracking-widest">
                  <Clock size={12} />
                  {new Date(msg.created_at).toLocaleString()}
                </div>
              </div>
            </motion.div>
          ))}

          {messages.length === 0 && (
            <div className="h-64 flex flex-col items-center justify-center border border-dashed border-white/10 rounded-[40px]">
              <Mail size={48} className="text-white/5 mb-4" />
              <p className="text-white/20 font-bold uppercase tracking-widest">No messages yet</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
