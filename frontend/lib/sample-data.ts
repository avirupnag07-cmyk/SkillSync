import { CandidateProfile } from "./types";

export const SAMPLE_CANDIDATE_PROFILES: CandidateProfile[] = [
  {
    id: "sample-ai-01",
    name: "Maya Chen (Sample AI Engineer)",
    email: "maya.chen@sample.skillsync.io",
    experience_years: 4.0,
    bio: "Senior AI Systems Engineer specializing in autonomous multi-agent systems, RAG architectures, and local inference optimization.",
    skills: [
      { id: "python", name: "Python", category: "languages", category_name: "Languages", weight: 2.0, verified: true },
      { id: "pytorch", name: "PyTorch", category: "ai_ml", category_name: "AI & ML", weight: 2.2, verified: true },
      { id: "huggingface", name: "Hugging Face", category: "ai_ml", category_name: "AI & ML", weight: 2.2, verified: true },
      { id: "llms", name: "LLMs", category: "ai_ml", category_name: "AI & ML", weight: 2.2, verified: true },
      { id: "rag", name: "RAG", category: "ai_ml", category_name: "AI & ML", weight: 2.2, verified: true },
      { id: "vector_databases", name: "Vector Databases", category: "ai_ml", category_name: "AI & ML", weight: 2.0, verified: true },
      { id: "fastapi", name: "FastAPI", category: "frameworks_libraries", category_name: "Frameworks", weight: 2.0, verified: true },
      { id: "docker", name: "Docker", category: "cloud_devops", category_name: "Cloud & DevOps", weight: 2.0, verified: true },
      { id: "postgresql", name: "PostgreSQL", category: "databases_data", category_name: "Databases", weight: 2.0, verified: true },
      { id: "git", name: "Git", category: "developer_tools", category_name: "Tools", weight: 1.8, verified: true },
    ],
    experiences: [
      {
        company: "Cognitive Matrix Labs",
        role: "Lead AI Systems Engineer",
        duration: "2022 - Present",
        description: "Architected cyclical LangGraph agent workflows processing 500k+ monthly interactions.",
        skills_used: ["Python", "PyTorch", "RAG", "Vector Databases", "FastAPI"]
      }
    ],
    projects: [
      {
        title: "MultiAgent-Orchestrator",
        description: "Open-source hierarchical supervisor agent with state checkpointing and SQLite memory persistence.",
        technologies: ["Python", "LangGraph", "ChromaDB", "FastAPI"]
      }
    ],
    education: [
      {
        institution: "University of California, Berkeley",
        degree: "B.S. in Computer Science",
        graduation_year: "2020"
      }
    ]
  },
  {
    id: "sample-fs-02",
    name: "Marcus Vance (Sample Full Stack)",
    email: "marcus.vance@sample.skillsync.io",
    experience_years: 5.0,
    bio: "Full Stack Engineer specialized in Next.js 14 App Router, TypeScript, and high-concurrency Python backends.",
    skills: [
      { id: "typescript", name: "TypeScript", category: "languages", category_name: "Languages", weight: 2.0, verified: true },
      { id: "javascript", name: "JavaScript", category: "languages", category_name: "Languages", weight: 2.0, verified: true },
      { id: "react", name: "React", category: "frameworks_libraries", category_name: "Frameworks", weight: 2.0, verified: true },
      { id: "nextjs", name: "Next.js", category: "frameworks_libraries", category_name: "Frameworks", weight: 2.0, verified: true },
      { id: "tailwind", name: "Tailwind CSS", category: "frameworks_libraries", category_name: "Frameworks", weight: 1.6, verified: true },
      { id: "python", name: "Python", category: "languages", category_name: "Languages", weight: 2.0, verified: true },
      { id: "fastapi", name: "FastAPI", category: "frameworks_libraries", category_name: "Frameworks", weight: 2.0, verified: true },
      { id: "postgresql", name: "PostgreSQL", category: "databases_data", category_name: "Databases", weight: 2.0, verified: true },
      { id: "docker", name: "Docker", category: "cloud_devops", category_name: "Cloud & DevOps", weight: 2.0, verified: true },
    ],
    experiences: [
      {
        company: "HyperScale Web",
        role: "Senior Full Stack Engineer",
        duration: "2022 - Present",
        description: "Led core Next.js 14 App Router migration and background FastAPI worker services.",
        skills_used: ["TypeScript", "Next.js", "Tailwind CSS", "FastAPI", "PostgreSQL"]
      }
    ],
    projects: [
      {
        title: "SyncTable Data Grid",
        description: "Virtual table component rendering 100k rows with optimistic server action mutations.",
        technologies: ["React", "TypeScript", "Tailwind CSS"]
      }
    ],
    education: [
      {
        institution: "University of Washington",
        degree: "B.S. in Software Engineering",
        graduation_year: "2019"
      }
    ]
  },
  {
    id: "sample-devops-03",
    name: "Elena Rostova (Sample DevOps)",
    email: "elena.rostova@sample.skillsync.io",
    experience_years: 4.5,
    bio: "DevOps Infrastructure Engineer managing multi-cloud Kubernetes clusters, Terraform IaC, and CI/CD automation.",
    skills: [
      { id: "aws", name: "AWS", category: "cloud_devops", category_name: "Cloud & DevOps", weight: 2.0, verified: true },
      { id: "gcp", name: "Google Cloud (GCP)", category: "cloud_devops", category_name: "Cloud & DevOps", weight: 2.0, verified: true },
      { id: "docker", name: "Docker", category: "cloud_devops", category_name: "Cloud & DevOps", weight: 2.0, verified: true },
      { id: "kubernetes", name: "Kubernetes", category: "cloud_devops", category_name: "Cloud & DevOps", weight: 2.2, verified: true },
      { id: "terraform", name: "Terraform", category: "cloud_devops", category_name: "Cloud & DevOps", weight: 2.0, verified: true },
      { id: "ci_cd", name: "CI/CD (GitHub Actions)", category: "cloud_devops", category_name: "Cloud & DevOps", weight: 2.0, verified: true },
      { id: "linux", name: "Linux Administration", category: "cloud_devops", category_name: "Cloud & DevOps", weight: 1.8, verified: true },
      { id: "bash", name: "Bash Scripting", category: "languages", category_name: "Languages", weight: 1.4, verified: true },
    ],
    experiences: [
      {
        company: "Nexus Cloud Systems",
        role: "Lead DevOps Engineer",
        duration: "2022 - Present",
        description: "Provisioned multi-region EKS and GKE clusters using Terraform with zero downtime deployments.",
        skills_used: ["AWS", "Kubernetes", "Terraform", "GitHub Actions", "Linux"]
      }
    ],
    projects: [
      {
        title: "KubeScale Autoscaler",
        description: "Event-driven Kubernetes pod autoscaler based on custom Kafka queue metrics.",
        technologies: ["Go", "Kubernetes", "Docker", "Prometheus"]
      }
    ],
    education: [
      {
        institution: "University of Illinois Urbana-Champaign",
        degree: "B.S. in Computer Systems Engineering",
        graduation_year: "2020"
      }
    ]
  }
];
