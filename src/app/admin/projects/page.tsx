"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { motion, AnimatePresence } from "framer-motion";
import {
  Plus,
  Search,
  Trash2,
  Edit3,
  ExternalLink,
  Github,
  Loader2,
  X,
  Upload
} from "lucide-react";

export default function AdminProjects() {
  const [projects, setProjects] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentProject, setCurrentProject] = useState<any>(null);
  const [isSubmitting, setIsModalSubmitting] = useState(false);

  useEffect(() => {
    fetchProjects();
  }, []);

  async function fetchProjects() {
    setLoading(true);
    const { data, error } = await supabase
      .from(\'projects\')
      .select(\'*\')
      .order(\'order\', { ascending: true });

    if (error) console.error(error);
    else setProjects(data || []);
    setLoading(false);
  }

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to delete this project?")) return;

    const { error } = await supabase.from(\'projects\').delete().eq(\'id\', id);
    if (error) alert(error.message);
    else fetchProjects();
  };

  const handleEdit = (project: any) => {
    setCurrentProject(project);
    setIsModalOpen(true);
  };

  const handleAdd = () => {
    setCurrentProject(null);
    setIsModalOpen(true);
  };

  const filteredProjects = projects.filter(p =>
    p.title.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-8">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold tracking-tight mb-2">Projects</h1>
          <p className="text-white/40 font-medium">Manage your portfolio showcase.</p>
        </div>
        <button
          onClick={handleAdd}
          className="flex items-center gap-2 px-6 py-3 rounded-2xl bg-white text-black font-bold hover:scale-[1.02] active:scale-[0.98] transition-all"
        >
          <Plus size={20} /> Add New Project
        </button>
      </header>

      <div className="relative">
        <Search className="absolute left-6 top-1/2 -translate-y-1/2 text-white/20" size={20} />
        <input
          type="text"
          placeholder="Search projects..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full pl-16 pr-6 py-4 rounded-3xl bg-white/5 border border-white/5 focus:border-white/20 focus:ring-4 focus:ring-white/5 transition-all outline-none"
        />
      </div>

      {loading ? (
        <div className="h-64 flex items-center justify-center">
          <Loader2 className="animate-spin text-white/20" size={48} />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filteredProjects.map((project) => (
            <motion.div
              key={project.id}
              layout
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="p-6 rounded-3xl border border-white/5 bg-white/[0.02] flex gap-6"
            >
              <div className="w-32 h-32 rounded-2xl bg-white/5 shrink-0 overflow-hidden relative">
                {project.thumbnail_url ? (
                  <img src={project.thumbnail_url} alt="" className="w-full h-full object-cover" />
                ) : (
                  <div className="w-full h-full flex items-center justify-center text-white/10">
                    <FolderGit2 size={32} />
                  </div>
                )}
              </div>

              <div className="flex-1">
                <div className="flex items-start justify-between mb-2">
                  <h3 className="text-xl font-bold tracking-tight">{project.title}</h3>
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleEdit(project)}
                      className="p-2 rounded-lg hover:bg-white/5 text-white/40 hover:text-white transition-all"
                    >
                      <Edit3 size={18} />
                    </button>
                    <button
                      onClick={() => handleDelete(project.id)}
                      className="p-2 rounded-lg hover:bg-red-400/10 text-white/40 hover:text-red-400 transition-all"
                    >
                      <Trash2 size={18} />
                    </button>
                  </div>
                </div>
                <p className="text-white/40 text-sm line-clamp-2 mb-4 font-medium">{project.description}</p>
                <div className="flex gap-4">
                  {project.github_url && <a href={project.github_url} target="_blank" className="text-white/20 hover:text-white transition-colors"><Github size={18} /></a>}
                  {project.live_url && <a href={project.live_url} target="_blank" className="text-white/20 hover:text-white transition-colors"><ExternalLink size={18} /></a>}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* Project Modal */}
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
              className="relative w-full max-w-2xl p-10 rounded-[40px] border border-white/10 bg-[#0A0A0A] shadow-2xl"
            >
              <button
                onClick={() => setIsModalOpen(false)}
                className="absolute right-8 top-8 text-white/20 hover:text-white transition-colors"
              >
                <X size={24} />
              </button>

              <h2 className="text-3xl font-bold tracking-tight mb-8">
                {currentProject ? "Edit Project" : "New Project"}
              </h2>

              <ProjectForm
                project={currentProject}
                onSuccess={() => {
                  setIsModalOpen(false);
                  fetchProjects();
                }}
              />
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}

function ProjectForm({ project, onSuccess }: { project?: any, onSuccess: () => void }) {
  const [title, setTitle] = useState(project?.title || "");
  const [description, setDescription] = useState(project?.description || "");
  const [github, setGithub] = useState(project?.github_url || "");
  const [live, setLive] = useState(project?.live_url || "");
  const [loading, setLoading] = useState(false);
  const [image, setImage] = useState<File | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    let thumbnail_url = project?.thumbnail_url;

    if (image) {
      const fileExt = image.name.split(\'.\').pop();
      const fileName = `${Math.random()}.${fileExt}`;
      const { data: uploadData, error: uploadError } = await supabase.storage
        .from(\'thumbnails\')
        .upload(fileName, image);

      if (uploadError) {
        alert(uploadError.message);
        setLoading(false);
        return;
      }

      const { data: { publicUrl } } = supabase.storage
        .from(\'thumbnails\')
        .getPublicUrl(fileName);

      thumbnail_url = publicUrl;
    }

    const payload = {
      title,
      description,
      github_url: github,
      live_url: live,
      thumbnail_url,
    };

    const { error } = project
      ? await supabase.from(\'projects\').update(payload).eq(\'id\', project.id)
      : await supabase.from(\'projects\').insert([payload]);

    if (error) alert(error.message);
    else onSuccess();
    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-2 gap-6">
        <div className="space-y-2">
          <label className="text-sm font-bold text-white/40 ml-1 uppercase tracking-widest">Title</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            className="w-full px-6 py-4 rounded-2xl bg-white/5 border border-white/5 focus:border-white/20 transition-all outline-none"
            placeholder="Cool App Name"
          />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-bold text-white/40 ml-1 uppercase tracking-widest">Thumbnail</label>
          <div className="relative group">
            <input
              type="file"
              onChange={(e) => setImage(e.target.files?.[0] || null)}
              className="absolute inset-0 opacity-0 cursor-pointer z-10"
            />
            <div className="w-full px-6 py-4 rounded-2xl bg-white/5 border border-white/5 group-hover:border-white/20 transition-all flex items-center gap-3">
              <Upload size={18} className="text-white/20" />
              <span className="text-white/40 font-medium truncate">{image?.name || "Choose file..."}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="space-y-2">
        <label className="text-sm font-bold text-white/40 ml-1 uppercase tracking-widest">Description</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
          rows={3}
          className="w-full px-6 py-4 rounded-2xl bg-white/5 border border-white/5 focus:border-white/20 transition-all outline-none resize-none"
          placeholder="What did you build?"
        />
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="space-y-2">
          <label className="text-sm font-bold text-white/40 ml-1 uppercase tracking-widest">GitHub URL</label>
          <input
            type="url"
            value={github}
            onChange={(e) => setGithub(e.target.value)}
            className="w-full px-6 py-4 rounded-2xl bg-white/5 border border-white/5 focus:border-white/20 transition-all outline-none"
            placeholder="https://github.com/..."
          />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-bold text-white/40 ml-1 uppercase tracking-widest">Live Demo URL</label>
          <input
            type="url"
            value={live}
            onChange={(e) => setLive(e.target.value)}
            className="w-full px-6 py-4 rounded-2xl bg-white/5 border border-white/5 focus:border-white/20 transition-all outline-none"
            placeholder="https://..."
          />
        </div>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full py-5 rounded-3xl bg-white text-black font-black text-lg hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 flex items-center justify-center gap-2 mt-4"
      >
        {loading ? <Loader2 className="animate-spin" size={24} /> : (project ? "Update Project" : "Publish Project")}
      </button>
    </form>
  );
}
