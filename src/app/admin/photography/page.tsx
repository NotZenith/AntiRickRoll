"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { motion, AnimatePresence } from "framer-motion";
import {
  Plus,
  Trash2,
  Loader2,
  X,
  Upload,
  Image as ImageIcon
} from "lucide-react";

export default function AdminPhotography() {
  const [photos, setPhotos] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    fetchPhotos();
  }, []);

  async function fetchPhotos() {
    setLoading(true);
    const { data, error } = await supabase
      .from(\'photos\')
      .select(\'*\')
      .order(\'created_at\', { ascending: false });

    if (error) console.error(error);
    else setPhotos(data || []);
    setLoading(false);
  }

  const handleDelete = async (id: string) => {
    if (!confirm("Delete this photo?")) return;

    const { error } = await supabase.from(\'photos\').delete().eq(\'id\', id);
    if (error) alert(error.message);
    else fetchPhotos();
  };

  return (
    <div className="space-y-8">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold tracking-tight mb-2">Photography</h1>
          <p className="text-white/40 font-medium">Capture and share your visual stories.</p>
        </div>
        <button
          onClick={() => setIsModalOpen(true)}
          className="flex items-center gap-2 px-6 py-3 rounded-2xl bg-white text-black font-bold hover:scale-[1.02] active:scale-[0.98] transition-all"
        >
          <Plus size={20} /> Upload Photo
        </button>
      </header>

      {loading ? (
        <div className="h-64 flex items-center justify-center">
          <Loader2 className="animate-spin text-white/20" size={48} />
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {photos.map((photo) => (
            <motion.div
              key={photo.id}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="group aspect-square rounded-3xl overflow-hidden relative border border-white/5"
            >
              <img src={photo.image_url} alt="" className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" />
              <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-4">
                <button
                  onClick={() => handleDelete(photo.id)}
                  className="p-3 rounded-2xl bg-red-500 text-white hover:scale-110 transition-transform"
                >
                  <Trash2 size={20} />
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* Upload Modal */}
      <AnimatePresence>
        {isModalOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center px-6">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsModalOpen(false)}
              className="absolute inset-0 bg-black/80 backdrop-blur-sm"
            />
            <motion.div
              initial={{ opacity: 0, scale: 0.9, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9, y: 20 }}
              className="relative w-full max-w-md p-10 rounded-[40px] border border-white/10 bg-[#0A0A0A] shadow-2xl"
            >
              <button
                onClick={() => setIsModalOpen(false)}
                className="absolute right-8 top-8 text-white/20 hover:text-white transition-colors"
              >
                <X size={24} />
              </button>

              <h2 className="text-3xl font-bold tracking-tight mb-8">Upload Photo</h2>

              <PhotoForm
                onSuccess={() => {
                  setIsModalOpen(false);
                  fetchPhotos();
                }}
              />
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}

function PhotoForm({ onSuccess }: { onSuccess: () => void }) {
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [image, setImage] = useState<File | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!image) return;
    setLoading(true);

    const fileExt = image.name.split(\'.\').pop();
    const fileName = `${Math.random()}.${fileExt}`;
    const { data: uploadData, error: uploadError } = await supabase.storage
      .from(\'photography\')
      .upload(fileName, image);

    if (uploadError) {
      alert(uploadError.message);
      setLoading(false);
      return;
    }

    const { data: { publicUrl } } = supabase.storage
      .from(\'photography\')
      .getPublicUrl(fileName);

    const { error } = await supabase.from(\'photos\').insert([{
      title,
      image_url: publicUrl,
    }]);

    if (error) alert(error.message);
    else onSuccess();
    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-2">
        <label className="text-sm font-bold text-white/40 ml-1 uppercase tracking-widest">Image File</label>
        <div className="relative group h-32">
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setImage(e.target.files?.[0] || null)}
            className="absolute inset-0 opacity-0 cursor-pointer z-10"
          />
          <div className="w-full h-full rounded-2xl bg-white/5 border border-dashed border-white/10 group-hover:border-white/20 transition-all flex flex-col items-center justify-center gap-2">
            <Upload size={24} className="text-white/20" />
            <span className="text-white/40 font-medium truncate px-4 w-full text-center">
              {image?.name || "Click to browse"}
            </span>
          </div>
        </div>
      </div>

      <div className="space-y-2">
        <label className="text-sm font-bold text-white/40 ml-1 uppercase tracking-widest">Title (Optional)</label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full px-6 py-4 rounded-2xl bg-white/5 border border-white/5 focus:border-white/20 transition-all outline-none"
          placeholder="Sunset at..."
        />
      </div>

      <button
        type="submit"
        disabled={loading || !image}
        className="w-full py-5 rounded-3xl bg-white text-black font-black text-lg hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 flex items-center justify-center gap-2"
      >
        {loading ? <Loader2 className="animate-spin" size={24} /> : "Upload to Gallery"}
      </button>
    </form>
  );
}
