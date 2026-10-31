export interface SkillItem {
  id: string;
  name: string;
  category: string;
  category_name?: string;
  weight?: number;
  verified?: boolean;
  years_experience?: number;
  is_mandatory?: boolean;
  mention_count?: number;
  docs_url?: string;
  free_courses?: string[];
  project_idea?: string;
  matched_with?: string;
  transferable_skill?: string;
  similarity?: number;
}

export interface ExperienceItem {
  company: string;
  role: string;
  duration: string;
  description?: string;
  skills_used: string[];
}

export interface ProjectItem {
  title: string;
  description: string;
  url?: string;
  technologies: string[];
}

export interface EducationItem {
  institution: string;
  degree: string;
  graduation_year?: string;
}

export interface CandidateProfile {
  id: string;
  name: string;
  email?: string;
  phone?: string;
  linkedin?: string;
  github?: string;
  experience_years: number;
  bio?: string;
  skills: SkillItem[];
  experiences: ExperienceItem[];
  projects: ProjectItem[];
  education: EducationItem[];
  created_at?: string;
}

export interface JobPosting {
  id: string;
  title: string;
  company?: string;
  location?: string;
  source: string;
  salary_range?: string;
  required_experience_years: number;
  description: string;
  url?: string;
  extracted_skills: SkillItem[];
  skills_count: number;
}

export interface CategoryBreakdown {
  category: string;
  category_name: string;
  score: number;
  required_count: number;
  matched_count: number;
}

export interface GapAnalysisResult {
  id?: string;
  overall_score: number;
  mandatory_score: number;
  preferred_score: number;
  experience_score: number;
  alignment_tier: string;
  executive_summary: string;
  disclaimer: string;
  counts: {
    total_job_skills: number;
    matched_count: number;
    partially_matched_count: number;
    missing_mandatory_count: number;
    missing_preferred_count: number;
    unverified_count: number;
  };
  matched_skills: SkillItem[];
  partially_matched_skills: SkillItem[];
  missing_mandatory_skills: SkillItem[];
  missing_preferred_skills: SkillItem[];
  unverified_skills: SkillItem[];
  category_breakdown: CategoryBreakdown[];
  audit_trail?: Array<{
    agent: string;
    action: string;
    timestamp: string;
    [key: string]: any;
  }>;
  provider_info?: ProviderInfo;
}

export interface RoadmapTask {
  id: string;
  description: string;
  completed: boolean;
}

export interface WeekPlan {
  week_number: number;
  title: string;
  goal: string;
  skills: SkillItem[];
  documentation_links: string[];
  free_resources: string[];
  project_milestone: string;
  tasks: RoadmapTask[];
}

export interface LearningRoadmap {
  id?: string;
  title: string;
  target_role: string;
  duration_weeks: number;
  total_skills: number;
  weeks: WeekPlan[];
  created_at?: string;
}

export interface RankedSkill {
  id: string;
  name: string;
  category: string;
  category_name: string;
  frequency: number;
  demand_percentage: number;
  mandatory_ratio: number;
  weight: number;
}

export interface MarketOverview {
  total_jobs_analyzed: number;
  unique_skills_tracked: number;
  top_skills: RankedSkill[];
  category_distribution: Array<{
    category_id: string;
    name: string;
    count: number;
    percentage: number;
  }>;
  emerging_technologies: Array<{
    name: string;
    category: string;
    growth: string;
  }>;
}

export interface RoleDetail {
  key: string;
  title: string;
  description: string;
  average_salary: string;
  demand_trend: string;
  total_core_skills: number;
  unique_skills: SkillItem[];
}

export interface RoleComparison {
  role_a: RoleDetail;
  role_b: RoleDetail;
  shared_skills: SkillItem[];
  overlap_percentage: number;
  transition_difficulty_score: number;
  recommendation: string;
}

export interface ProviderInfo {
  provider: string;
  model_name: string;
  is_local: boolean;
  requires_api_key: boolean;
  status: string;
  badge_label: string;
  description: string;
}
