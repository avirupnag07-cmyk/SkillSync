"use client";

import { useState, useEffect } from "react";
import { Header } from "@/components/layout/Header";
import {
  UploadCloud,
  FileText,
  Plus,
  Trash2,
  CheckCircle2,
  AlertCircle,
  ExternalLink,
  Save,
  Sparkles,
  BadgeCheck,
  Briefcase,
  FolderGit2,
  GraduationCap,
} from "lucide-react";
import { api } from "@/lib/api";
import { CandidateProfile, SkillItem, ExperienceItem, ProjectItem, EducationItem } from "@/lib/types";
import { getCategoryBadgeColor } from "@/lib/utils";

const EMPTY_PROFILE: CandidateProfile = {
  id: "",
  name: "No resume uploaded",
  experience_years: 0,
  skills: [],
  experiences: [],
  projects: [],
  education: [],
};

export default function ProfilePage() {
  const [profile, setProfile] = useState<CandidateProfile>(EMPTY_PROFILE);
  const [uploading, setUploading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [notification, setNotification] = useState<string | null>(null);
  const [newSkillInput, setNewSkillInput] = useState("");

  useEffect(() => {
    if (typeof window !== "undefined") {
      const stored = localStorage.getItem("skillsync_active_profile");
      if (stored) {
        try {
          setProfile(JSON.parse(stored));
        } catch {}
      }
    }
  }, []);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setNotification(null);
    try {
      const res = await api.uploadResume(file);
      const updatedProfile: CandidateProfile = {
        ...EMPTY_PROFILE,
        id: res.profile_id,
        name: res.name || "Unnamed Candidate",
        email: res.email,
        phone: res.phone,
        linkedin: res.linkedin,
        github: res.github,
        experience_years: res.experience_years || 0,
        skills: res.extracted_skills || [],
      };
      setProfile(updatedProfile);
      localStorage.setItem("skillsync_active_profile", JSON.stringify(updatedProfile));
      localStorage.removeItem("skillsync_last_gap_id");
      localStorage.removeItem("skillsync_last_gap_result");
      setNotification(`Resume parsed successfully! Extracted ${res.skills_count} skills.`);
    } catch (err: any) {
      setNotification(`Error uploading resume: ${err.response?.data?.detail || err.message}`);
    } finally {
      setUploading(false);
    }
  };

  const handleAddSkill = () => {
    if (!newSkillInput.trim()) return;
    const clean = newSkillInput.trim();
    if (profile.skills.some((s) => s.name.toLowerCase() === clean.toLowerCase())) {
      setNewSkillInput("");
      return;
    }

    const newSkill: SkillItem = {
      id: clean.toLowerCase().replace(/[^a-z0-9]/g, "_"),
      name: clean,
      category: "languages",
      weight: 1.5,
      verified: true,
    };

    const updated = {
      ...profile,
      skills: [...profile.skills, newSkill],
    };
    setProfile(updated);
    setNewSkillInput("");
  };

  const handleRemoveSkill = (skillId: string) => {
    setProfile({
      ...profile,
      skills: profile.skills.filter((s) => s.id !== skillId),
    });
  };

  const handleSaveProfile = async () => {
    setSaving(true);
    try {
      await api.saveProfile(profile, profile.id);
      localStorage.setItem("skillsync_active_profile", JSON.stringify(profile));
      setNotification("Profile changes saved to database.");
    } catch (err: any) {
      setNotification("Saved locally to session.");
      localStorage.setItem("skillsync_active_profile", JSON.stringify(profile));
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <Header
        title="Career Profile & Competency Matrix"
        subtitle="Upload your resume or manually customize technical qualifications and projects"
      />

      <div className="p-8 max-w-7xl mx-auto space-y-6">
        {notification && (
          <div className="p-3.5 rounded-lg bg-blue-500/10 border border-blue-500/20 text-xs text-blue-600 dark:text-blue-400 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 shrink-0" />
              <span>{notification}</span>
            </div>
            <button onClick={() => setNotification(null)} className="hover:opacity-75">
              &times;
            </button>
          </div>
        )}

        {/* Top Controls: Resume Dropzone & Sample Profiles */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* File Upload Dropzone */}
          <div className="lg:col-span-2 p-6 rounded-lg border border-dashed border-[var(--surface-border)] bg-[var(--surface)] flex flex-col items-center justify-center text-center hover:border-blue-500 transition-colors">
            <div className="w-12 h-12 rounded-full bg-blue-500/10 flex items-center justify-center text-blue-600 dark:text-blue-400 mb-3">
              <UploadCloud className="w-6 h-6" />
            </div>
            <h3 className="text-sm font-semibold text-[var(--foreground)]">
              Upload Resume (PDF, DOCX, or TXT)
            </h3>
            <p className="text-xs text-[var(--muted-text)] mt-1 max-w-md">
              Our automated Resume Intelligence Agent extracts your contact details, work milestones, education, and normalized skills.
            </p>
            <label className="mt-4 px-4 py-2 rounded-md bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold cursor-pointer shadow-electric transition-colors inline-flex items-center gap-2">
              <FileText className="w-4 h-4" />
              <span>{uploading ? "Analyzing Document..." : "Select File"}</span>
              <input
                type="file"
                accept=".pdf,.docx,.txt"
                className="hidden"
                onChange={handleFileUpload}
                disabled={uploading}
              />
            </label>
          </div>

          {/* Save Controls */}
          <div className="p-5 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] flex flex-col justify-end">
            <button
              onClick={handleSaveProfile}
              disabled={saving}
              className="w-full flex items-center justify-center gap-2 py-2 rounded-md bg-[var(--surface-muted)] hover:bg-[var(--surface-border)] text-xs font-semibold text-[var(--foreground)] border border-[var(--surface-border)] transition-colors"
            >
              <Save className="w-4 h-4" />
              <span>{saving ? "Saving..." : "Save Profile Changes"}</span>
            </button>
          </div>
        </div>

        {/* Profile Core Details Editor */}
        <div className="p-6 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-4">
          <h3 className="text-sm font-semibold text-[var(--foreground)] border-b border-[var(--surface-border)] pb-2">
            Personal & Career Information
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="text-xs text-[var(--muted-text)]">Full Name</label>
              <input
                type="text"
                value={profile.name}
                onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                className="w-full mt-1 px-3 py-1.5 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] text-xs text-[var(--foreground)]"
              />
            </div>
            <div>
              <label className="text-xs text-[var(--muted-text)]">Email Address</label>
              <input
                type="email"
                value={profile.email || ""}
                onChange={(e) => setProfile({ ...profile, email: e.target.value })}
                className="w-full mt-1 px-3 py-1.5 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] text-xs text-[var(--foreground)]"
              />
            </div>
            <div>
              <label className="text-xs text-[var(--muted-text)]">Total Experience (Years)</label>
              <input
                type="number"
                step="0.5"
                value={profile.experience_years}
                onChange={(e) => setProfile({ ...profile, experience_years: parseFloat(e.target.value) || 0 })}
                className="w-full mt-1 px-3 py-1.5 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] text-xs text-[var(--foreground)] font-mono"
              />
            </div>
            <div>
              <label className="text-xs text-[var(--muted-text)]">LinkedIn Profile</label>
              <input
                type="text"
                value={profile.linkedin || ""}
                onChange={(e) => setProfile({ ...profile, linkedin: e.target.value })}
                placeholder="linkedin.com/in/username"
                className="w-full mt-1 px-3 py-1.5 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] text-xs text-[var(--foreground)]"
              />
            </div>
            <div>
              <label className="text-xs text-[var(--muted-text)]">GitHub Profile</label>
              <input
                type="text"
                value={profile.github || ""}
                onChange={(e) => setProfile({ ...profile, github: e.target.value })}
                placeholder="github.com/username"
                className="w-full mt-1 px-3 py-1.5 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] text-xs text-[var(--foreground)]"
              />
            </div>
            <div>
              <label className="text-xs text-[var(--muted-text)]">Executive Bio</label>
              <input
                type="text"
                value={profile.bio || ""}
                onChange={(e) => setProfile({ ...profile, bio: e.target.value })}
                placeholder="Brief professional summary"
                className="w-full mt-1 px-3 py-1.5 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] text-xs text-[var(--foreground)]"
              />
            </div>
          </div>
        </div>

        {/* Technical Skills Competency Matrix */}
        <div className="p-6 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-4">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-[var(--surface-border)] pb-3">
            <div>
              <h3 className="text-sm font-semibold text-[var(--foreground)]">
                Recognized Competencies ({profile.skills.length})
              </h3>
              <p className="text-xs text-[var(--muted-text)]">
                Normalized skills mapped to industry taxonomy. Skills can be verified with project deliverables.
              </p>
            </div>
            <div className="flex items-center gap-2">
              <input
                type="text"
                value={newSkillInput}
                onChange={(e) => setNewSkillInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleAddSkill()}
                placeholder="Add skill (e.g. FastAPI, K8s)..."
                className="px-3 py-1.5 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] text-xs text-[var(--foreground)] w-48"
              />
              <button
                onClick={handleAddSkill}
                className="px-3 py-1.5 rounded-md bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold flex items-center gap-1 transition-colors"
              >
                <Plus className="w-3.5 h-3.5" />
                Add
              </button>
            </div>
          </div>

          <div className="flex flex-wrap gap-2 pt-2">
            {profile.skills.map((skill) => (
              <span
                key={skill.id}
                className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium border ${getCategoryBadgeColor(
                  skill.category
                )}`}
              >
                <span>{skill.name}</span>
                {skill.verified !== false && (
                  <span title="Verified in resume">
                    <BadgeCheck className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400" />
                  </span>
                )}
                <button
                  onClick={() => handleRemoveSkill(skill.id)}
                  className="hover:text-red-500 ml-0.5 text-xs font-bold leading-none"
                  title="Remove skill"
                >
                  &times;
                </button>
              </span>
            ))}
          </div>
        </div>

        {/* Experience Timeline */}
        <div className="p-6 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-4">
          <div className="flex items-center justify-between border-b border-[var(--surface-border)] pb-2">
            <div className="flex items-center gap-2">
              <Briefcase className="w-4 h-4 text-blue-600 dark:text-blue-400" />
              <h3 className="text-sm font-semibold text-[var(--foreground)]">
                Work Experience Timeline
              </h3>
            </div>
            <button
              onClick={() =>
                setProfile({
                  ...profile,
                  experiences: [
                    ...profile.experiences,
                    {
                      company: "",
                      role: "",
                      duration: "",
                      description: "",
                      skills_used: [],
                    },
                  ],
                })
              }
              className="text-xs text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1 font-medium"
            >
              <Plus className="w-3.5 h-3.5" /> Add Experience
            </button>
          </div>

          <div className="space-y-3">
            {profile.experiences.length === 0 && (
              <p className="text-xs text-[var(--muted-text)]">
                No work experience yet. Click "Add Experience" to enter company, role, duration and responsibilities.
              </p>
            )}
            {profile.experiences.map((exp, idx) => {
              const updateExp = (patch: Partial<ExperienceItem>) =>
                setProfile({
                  ...profile,
                  experiences: profile.experiences.map((e, i) => (i === idx ? { ...e, ...patch } : e)),
                });
              const inputCls =
                "w-full mt-1 px-3 py-1.5 rounded-md border border-[var(--surface-border)] bg-[var(--surface)] text-xs text-[var(--foreground)]";
              return (
                <div
                  key={idx}
                  className="p-4 rounded-lg border border-[var(--surface-border)] bg-[var(--surface-muted)] relative space-y-3"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold text-[var(--foreground)]">
                      {exp.role || "Role"} &bull; {exp.company || "Company"}
                    </span>
                    <button
                      onClick={() =>
                        setProfile({
                          ...profile,
                          experiences: profile.experiences.filter((_, i) => i !== idx),
                        })
                      }
                      className="text-red-500 hover:text-red-600"
                      title="Remove experience"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    <div>
                      <label className="text-xs text-[var(--muted-text)]">Company Name</label>
                      <input
                        type="text"
                        value={exp.company}
                        onChange={(e) => updateExp({ company: e.target.value })}
                        placeholder="e.g. Acme Technologies"
                        className={inputCls}
                      />
                    </div>
                    <div>
                      <label className="text-xs text-[var(--muted-text)]">Role / Job Title</label>
                      <input
                        type="text"
                        value={exp.role}
                        onChange={(e) => updateExp({ role: e.target.value })}
                        placeholder="e.g. Software Engineer"
                        className={inputCls}
                      />
                    </div>
                    <div>
                      <label className="text-xs text-[var(--muted-text)]">Duration</label>
                      <input
                        type="text"
                        value={exp.duration}
                        onChange={(e) => updateExp({ duration: e.target.value })}
                        placeholder="e.g. Jan 2022 - Present"
                        className={`${inputCls} font-mono`}
                      />
                    </div>
                  </div>

                  <div>
                    <label className="text-xs text-[var(--muted-text)]">Work Description / Responsibilities</label>
                    <textarea
                      value={exp.description || ""}
                      onChange={(e) => updateExp({ description: e.target.value })}
                      rows={3}
                      placeholder="Describe what you built, owned or achieved in this role"
                      className={inputCls}
                    />
                  </div>

                  <div>
                    <label className="text-xs text-[var(--muted-text)]">Skills / Technologies Used (comma separated)</label>
                    <input
                      type="text"
                      value={exp.skills_used.join(",")}
                      onChange={(e) => updateExp({ skills_used: e.target.value.split(",") })}
                      onBlur={() =>
                        updateExp({ skills_used: exp.skills_used.map((t) => t.trim()).filter(Boolean) })
                      }
                      placeholder="e.g. Python, FastAPI, Docker"
                      className={inputCls}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
