import axios from "axios";
import {
  CandidateProfile,
  GapAnalysisResult,
  JobPosting,
  LearningRoadmap,
  MarketOverview,
  RoleComparison,
  ProviderInfo,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json",
  },
});

// Attach JWT token if available
apiClient.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("skillsync_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

export const api = {
  // Health & Diagnostics
  getHealth: async (): Promise<{ status: string; active_provider: ProviderInfo }> => {
    const res = await apiClient.get("/health");
    return res.data;
  },

  // Auth
  loginGuest: async () => {
    const res = await apiClient.post("/auth/guest");
    if (typeof window !== "undefined" && res.data.access_token) {
      localStorage.setItem("skillsync_token", res.data.access_token);
    }
    return res.data;
  },

  // Profile
  uploadResume: async (file: File): Promise<{
    profile_id: string;
    name: string;
    email?: string;
    phone?: string;
    linkedin?: string;
    github?: string;
    experience_years: number;
    extracted_skills: any[];
    skills_count: number;
  }> => {
    const formData = new FormData();
    formData.append("file", file);
    const res = await apiClient.post("/profile/upload-resume", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return res.data;
  },

  saveProfile: async (profileData: any, profileId?: string) => {
    const res = await apiClient.post("/profile/save", profileData, {
      params: profileId ? { profile_id: profileId } : {},
    });
    return res.data;
  },

  getProfile: async (profileId: string): Promise<CandidateProfile> => {
    const res = await apiClient.get(`/profile/${profileId}`);
    return res.data;
  },

  addSkillToProfile: async (profileId: string, skillName: string) => {
    const res = await apiClient.post(`/profile/${profileId}/add-skill`, null, {
      params: { skill_name: skillName },
    });
    return res.data;
  },

  removeSkillFromProfile: async (profileId: string, skillId: string) => {
    const res = await apiClient.delete(`/profile/${profileId}/remove-skill/${skillId}`);
    return res.data;
  },

  // Job Intelligence
  searchJobs: async (query = "", location = "", source = "all"): Promise<JobPosting[]> => {
    const res = await apiClient.get("/jobs/search", {
      params: { query, location, source },
    });
    return res.data;
  },

  getBenchmarkJobs: async (): Promise<JobPosting[]> => {
    const res = await apiClient.get("/jobs/benchmark");
    return res.data;
  },

  getJobById: async (jobId: string): Promise<JobPosting> => {
    const res = await apiClient.get(`/jobs/${jobId}`);
    return res.data;
  },

  pasteJob: async (jobData: {
    title: string;
    company?: string;
    location?: string;
    description: string;
    salary_range?: string;
  }): Promise<JobPosting> => {
    const res = await apiClient.post("/jobs/paste", jobData);
    return res.data;
  },

  // Skill Gap Analysis
  analyzeGap: async (payload: {
    profile_id?: string;
    job_id?: string;
    raw_resume_text?: string;
    raw_job_description?: string;
    candidate_skills?: any[];
    candidate_experience_years?: number;
    required_experience_years?: number;
    job_title?: string;
    candidate_name?: string;
  }): Promise<GapAnalysisResult> => {
    const res = await apiClient.post("/gap/analyze", payload);
    return res.data;
  },

  getGapHistory: async () => {
    const res = await apiClient.get("/gap/history");
    return res.data;
  },

  getGapById: async (analysisId: string): Promise<GapAnalysisResult> => {
    const res = await apiClient.get(`/gap/${analysisId}`);
    return res.data;
  },

  // Market Intelligence & Role Comparison
  getMarketOverview: async (): Promise<MarketOverview> => {
    const res = await apiClient.get("/market/overview");
    return res.data;
  },

  getAvailableRoles: async () => {
    const res = await apiClient.get("/market/roles");
    return res.data;
  },

  compareRoles: async (roleA = "ai_engineer", roleB = "data_scientist"): Promise<RoleComparison> => {
    const res = await apiClient.get("/comparison/compare", {
      params: { role_a: roleA, role_b: roleB },
    });
    return res.data;
  },

  // Learning Roadmap
  generateRoadmap: async (payload: {
    gap_analysis_id?: string;
    target_role?: string;
    duration_weeks?: number;
    missing_skills?: any[];
  }): Promise<LearningRoadmap> => {
    const res = await apiClient.post("/roadmap/generate", payload);
    return res.data;
  },

  getRoadmapById: async (roadmapId: string): Promise<LearningRoadmap> => {
    const res = await apiClient.get(`/roadmap/${roadmapId}`);
    return res.data;
  },

  toggleRoadmapTask: async (
    roadmapId: string,
    weekNumber: number,
    taskId: string,
    completed: boolean
  ) => {
    const res = await apiClient.post(`/roadmap/${roadmapId}/toggle-task`, {
      week_number: weekNumber,
      task_id: taskId,
      completed,
    });
    return res.data;
  },

  // Export URLs
  getGapPdfUrl: (analysisId: string) => `${API_BASE}/reports/gap-pdf?analysis_id=${analysisId}`,
  getGapCsvUrl: (analysisId: string) => `${API_BASE}/reports/gap-csv?analysis_id=${analysisId}`,
  getRoadmapPdfUrl: (roadmapId: string) => `${API_BASE}/reports/roadmap-pdf?roadmap_id=${roadmapId}`,
  getRoadmapCsvUrl: (roadmapId: string) => `${API_BASE}/reports/roadmap-csv?roadmap_id=${roadmapId}`,
};
