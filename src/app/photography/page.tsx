"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { motion, AnimatePresence } from "framer-motion";
import { GridBackground } from "@/components/ui/grid-background";
import { Loader2, ArrowLeft, X } from "lucide-react";
import Link from "next/link";

export default function Photography() {
  const [photos, setPhotos] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedPhoto, setSelectedPhoto] = useState<string | null>(null);

  useEffect(() => {
    async function fetchPhotos() {
      const { data } = await supabase
        .from(\'photos\')
        .select(\'*\')
        .order(\'created_at\', { ascending: false });
      setPhotos(data || []);
      setLoading(false);
    }
    fetchPhotos();
  }, []);

  return (
    <main className="relative min-h-screen px-6 py-24 md:px-12 lg:px-24 max-w-7xl mx-auto">
      <GridBackground />

      <Link href="/" className="inline-flex items-center gap-2 text-white/40 hover:text-white transition-colors mb-12 group font-medium">
        <ArrowLeft size={20} className="group-hover:-translate-x-1 transition-transform" /> Back Home
      </Link>

      <header className="mb-24 text-center">
        <h1 className="text-5xl md:text-7xl font-bold tracking-tighter mb-6 leading-none italic">Photography.</h1>
        <p className="max-w-xl mx-auto text-lg text-white/40 font-medium leading-relaxed">
          Through my lens: exploring the world and capturing moments of stillness in a fast-paced environment.
        </p>
      </header>

      {loading ? (
        <div className="h-64 flex items-center justify-center">
          <Loader2 className="animate-spin text-white/20" size={48} />
        </div>
      ) : (
        <div className="columns-1 sm:columns-2 lg:columns-3 gap-6 space-y-6">
          {photos.map((photo, i) => (
            <motion.div
              key={photo.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="break-inside-avoid relative group rounded-3xl overflow-hidden bg-white/5 border border-white/5 cursor-pointer"
              onClick={() => setSelectedPhoto(photo.image_url)}
            >
              <img
                src={photo.image_url}
                alt={photo.title || ""}
                className="w-full h-auto object-cover group-hover:scale-105 transition-transform duration-700"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity p-8 flex flex-col justify-end">
                <h3 className="text-xl font-bold tracking-tight">{photo.title}</h3>
                <p className="text-sm text-white/60 font-medium uppercase tracking-widest mt-1">Nepal</p>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* Lightbox */}
      <AnimatePresence>
        {selectedPhoto && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[100] bg-black/95 backdrop-blur-xl flex items-center justify-center p-6 sm:p-12 md:p-24"
            onClick={() => setSelectedPhoto(null)}
          >
            <button className="absolute top-12 right-12 text-white/40 hover:text-white transition-colors">
              <X size={32} />
            </button>
            <motion.img
              initial={{ scale: 0.9, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.9, y: 20 }}
              src={selectedPhoto}
              alt=""
              className="max-w-full max-h-full rounded-2xl shadow-2xl object-contain"
            />
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  );
}
