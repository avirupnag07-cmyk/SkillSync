"""Comprehensive Skill Taxonomy, Normalization, and Ontology Engine.

Contains 450+ canonical technical and professional skills across 8 core domains,
including alias mappings, categories, similarity relationships, and curated learning resources.
"""

from typing import Dict, List, Optional, Set, Tuple
import re

# Domain Categories
CATEGORIES = {
    "languages": "Programming & Query Languages",
    "frameworks_libraries": "Frameworks & Libraries",
    "cloud_devops": "Cloud & DevOps Infrastructure",
    "databases_data": "Databases & Data Engineering",
    "ai_ml": "Artificial Intelligence & Machine Learning",
    "developer_tools": "Developer Tools & Platforms",
    "certifications": "Certifications & Credentials",
    "soft_skills": "Soft Skills & Engineering Practices",
}

# Canonical Skill Definitions
# Format: id: { name, category, weight, related: {id: similarity}, docs_url, free_courses: [], project_idea }
SKILL_TAXONOMY: Dict[str, dict] = {
    # ------------------- LANGUAGES -------------------
    "python": {
        "name": "Python",
        "category": "languages",
        "weight": 2.0,
        "related": {"r": 0.5, "julia": 0.5, "go": 0.4},
        "docs_url": "https://docs.python.org/3/",
        "free_courses": ["freeCodeCamp - Python for Everybody", "Harvard CS50P"],
        "project_idea": "Build an asynchronous data extraction and processing CLI tool with Pydantic and SQLite."
    },
    "javascript": {
        "name": "JavaScript",
        "category": "languages",
        "weight": 2.0,
        "related": {"typescript": 0.85},
        "docs_url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
        "free_courses": ["freeCodeCamp - JavaScript Algorithms and Data Structures", "The Odin Project"],
        "project_idea": "Create an interactive browser-based state management visualization utility."
    },
    "typescript": {
        "name": "TypeScript",
        "category": "languages",
        "weight": 2.0,
        "related": {"javascript": 0.9},
        "docs_url": "https://www.typescriptlang.org/docs/",
        "free_courses": ["Total TypeScript Beginner Tutorial", "freeCodeCamp - TypeScript Course"],
        "project_idea": "Build a strictly typed REST & WebSocket real-time analytics SDK with zero runtime dependencies."
    },
    "sql": {
        "name": "SQL",
        "category": "languages",
        "weight": 1.8,
        "related": {"postgresql": 0.8, "mysql": 0.8},
        "docs_url": "https://www.w3schools.com/sql/",
        "free_courses": ["Stanford Online - Databases: Relational Databases and SQL", "SQLBolt"],
        "project_idea": "Design an enterprise database schema with complex window functions and CTE performance benchmarks."
    },
    "go": {
        "name": "Go (Golang)",
        "category": "languages",
        "weight": 2.0,
        "related": {"rust": 0.6, "c++": 0.5},
        "docs_url": "https://go.dev/doc/",
        "free_courses": ["Go by Example", "Tour of Go"],
        "project_idea": "Construct a high-concurrency rate-limited reverse proxy with distributed health checks."
    },
    "rust": {
        "name": "Rust",
        "category": "languages",
        "weight": 2.0,
        "related": {"c++": 0.7, "go": 0.6},
        "docs_url": "https://doc.rust-lang.org/book/",
        "free_courses": ["Rustlings", "The Rust Programming Language Book"],
        "project_idea": "Develop a memory-efficient memory-mapped vector search index."
    },
    "c++": {
        "name": "C++",
        "category": "languages",
        "weight": 2.0,
        "related": {"c": 0.8, "rust": 0.7},
        "docs_url": "https://en.cppreference.com/w/",
        "free_courses": ["LearnCpp.com", "MIT 6.096 Introduction to C++"],
        "project_idea": "Implement a lock-free multi-producer multi-consumer queue with benchmarking."
    },
    "java": {
        "name": "Java",
        "category": "languages",
        "weight": 1.8,
        "related": {"kotlin": 0.8, "scala": 0.7, "c#": 0.75},
        "docs_url": "https://docs.oracle.com/en/java/",
        "free_courses": ["University of Helsinki - Java MOOC", "freeCodeCamp Java for Beginners"],
        "project_idea": "Build a modular multi-tenant event pipeline using virtual threads."
    },
    "c#": {
        "name": "C#",
        "category": "languages",
        "weight": 1.8,
        "related": {"java": 0.75, ".net": 0.9},
        "docs_url": "https://learn.microsoft.com/en-us/dotnet/csharp/",
        "free_courses": ["Microsoft Learn - C# Certification", "freeCodeCamp C# Tutorial"],
        "project_idea": "Build a high-performance ASP.NET Core microservice with Entity Framework Core."
    },
    "kotlin": {
        "name": "Kotlin",
        "category": "languages",
        "weight": 1.8,
        "related": {"java": 0.85},
        "docs_url": "https://kotlinlang.org/docs/home.html",
        "free_courses": ["Kotlin Bootcamp by Google", "Kotlin by Example"],
        "project_idea": "Develop a multiplatform shared business logic module with coroutines."
    },
    "scala": {
        "name": "Scala",
        "category": "languages",
        "weight": 1.8,
        "related": {"java": 0.7, "apache_spark": 0.8},
        "docs_url": "https://docs.scala-lang.org/",
        "free_courses": ["Coursera Functional Programming in Scala (EPFL)", "Tour of Scala"],
        "project_idea": "Create an immutable streaming processing engine with Akka / Pekko."
    },
    "r": {
        "name": "R",
        "category": "languages",
        "weight": 1.6,
        "related": {"python": 0.5},
        "docs_url": "https://cran.r-project.org/manuals.html",
        "free_courses": ["Johns Hopkins R Programming (Coursera)", "Hands-On Programming with R"],
        "project_idea": "Generate automated reproducible statistical survival and econometric analysis reports."
    },
    "bash": {
        "name": "Bash / Shell Scripting",
        "category": "languages",
        "weight": 1.4,
        "related": {"linux": 0.85},
        "docs_url": "https://www.gnu.org/software/bash/manual/",
        "free_courses": ["MIT The Missing Semester of Your CS Education", "Bash Guide for Beginners"],
        "project_idea": "Write an automated multi-environment deployment and diagnostic healthcheck CLI."
    },

    # ------------------- FRAMEWORKS & LIBRARIES -------------------
    "fastapi": {
        "name": "FastAPI",
        "category": "frameworks_libraries",
        "weight": 2.0,
        "related": {"flask": 0.75, "django": 0.7, "pydantic": 0.85},
        "docs_url": "https://fastapi.tiangolo.com/",
        "free_courses": ["FastAPI Official Tutorial", "TestDriven.io FastAPI Crash Course"],
        "project_idea": "Create a production-ready asynchronous API with OAuth2, rate limiting, and OpenAPI schemas."
    },
    "django": {
        "name": "Django",
        "category": "frameworks_libraries",
        "weight": 1.8,
        "related": {"fastapi": 0.7, "flask": 0.75},
        "docs_url": "https://docs.djangoproject.com/",
        "free_courses": ["MDN Django Web Framework", "Django Girls Tutorial"],
        "project_idea": "Build a full-featured content management portal with robust RBAC and Celery background workers."
    },
    "flask": {
        "name": "Flask",
        "category": "frameworks_libraries",
        "weight": 1.6,
        "related": {"fastapi": 0.75, "django": 0.7},
        "docs_url": "https://flask.palletsprojects.com/",
        "free_courses": ["The Flask Mega-Tutorial by Miguel Grinberg"],
        "project_idea": "Deploy a lightweight REST microservice with blueprint architecture and Pytest coverage."
    },
    "react": {
        "name": "React",
        "category": "frameworks_libraries",
        "weight": 2.0,
        "related": {"nextjs": 0.85, "vue": 0.65},
        "docs_url": "https://react.dev/",
        "free_courses": ["React.dev Interactive Documentation", "freeCodeCamp React Course"],
        "project_idea": "Develop a complex dashboard with optimistic updates, virtualization, and custom hooks."
    },
    "nextjs": {
        "name": "Next.js",
        "category": "frameworks_libraries",
        "weight": 2.0,
        "related": {"react": 0.9, "nodejs": 0.75},
        "docs_url": "https://nextjs.org/docs",
        "free_courses": ["Next.js Official Learn Course", "freeCodeCamp Full Stack Next.js"],
        "project_idea": "Build an enterprise portal with App Router, Server Actions, edge caching, and dynamic OG images."
    },
    "nodejs": {
        "name": "Node.js",
        "category": "frameworks_libraries",
        "weight": 2.0,
        "related": {"express": 0.85, "typescript": 0.8},
        "docs_url": "https://nodejs.org/docs/",
        "free_courses": ["Node.js Official Guides", "freeCodeCamp Node.js and Express"],
        "project_idea": "Implement a real-time event-driven streaming server handling millions of concurrent events."
    },
    "express": {
        "name": "Express.js",
        "category": "frameworks_libraries",
        "weight": 1.7,
        "related": {"nodejs": 0.9, "fastapi": 0.65},
        "docs_url": "https://expressjs.com/",
        "free_courses": ["Mozilla MDN Express Tutorial", "Full Stack Open (University of Helsinki)"],
        "project_idea": "Construct a secure REST API with helmet, CORS, JWT authentication, and structured logging."
    },
    "vue": {
        "name": "Vue.js",
        "category": "frameworks_libraries",
        "weight": 1.8,
        "related": {"react": 0.7, "nuxt": 0.85},
        "docs_url": "https://vuejs.org/guide/introduction.html",
        "free_courses": ["Vue.js Official Tutorial", "Vue Mastery Intro to Vue 3"],
        "project_idea": "Build an interactive Kanban workflow application with Pinia state management."
    },
    "angular": {
        "name": "Angular",
        "category": "frameworks_libraries",
        "weight": 1.8,
        "related": {"react": 0.65, "typescript": 0.85},
        "docs_url": "https://angular.dev/",
        "free_courses": ["Angular.dev Official Interactive Tutorials"],
        "project_idea": "Create an enterprise administrative suite with signals, standalone components, and RxJS pipelines."
    },
    "tailwind": {
        "name": "Tailwind CSS",
        "category": "frameworks_libraries",
        "weight": 1.6,
        "related": {"css": 0.9},
        "docs_url": "https://tailwindcss.com/docs",
        "free_courses": ["Tailwind Labs YouTube", "Scrimba Tailwind CSS Course"],
        "project_idea": "Design an accessible, responsive design system library with dark/light theme tokens."
    },
    "spring_boot": {
        "name": "Spring Boot",
        "category": "frameworks_libraries",
        "weight": 2.0,
        "related": {"java": 0.9, "kotlin": 0.7},
        "docs_url": "https://spring.io/projects/spring-boot",
        "free_courses": ["Spring Academy Guides", "Amigoscode Spring Boot Tutorial"],
        "project_idea": "Build a microservices architecture with Spring Cloud, Eureka service discovery, and Resilience4j."
    },
    "graphql": {
        "name": "GraphQL",
        "category": "frameworks_libraries",
        "weight": 1.7,
        "related": {"rest_api": 0.75},
        "docs_url": "https://graphql.org/learn/",
        "free_courses": ["Apollo Odyssey Tutorials", "How to GraphQL"],
        "project_idea": "Construct a unified GraphQL gateway with Apollo Federation or Strawberry Python."
    },
    "rest_api": {
        "name": "RESTful APIs",
        "category": "frameworks_libraries",
        "weight": 1.8,
        "related": {"graphql": 0.7, "fastapi": 0.8},
        "docs_url": "https://restfulapi.net/",
        "free_courses": ["Postman REST API Basics", "MDN HTTP Overview"],
        "project_idea": "Design an idempotent REST API following OpenAPI 3.1 specifications."
    },

    # ------------------- AI & MACHINE LEARNING -------------------
    "pytorch": {
        "name": "PyTorch",
        "category": "ai_ml",
        "weight": 2.2,
        "related": {"tensorflow": 0.75, "huggingface": 0.85},
        "docs_url": "https://pytorch.org/docs/stable/index.html",
        "free_courses": ["Deep Learning with PyTorch (Udacity/NYU)", "Fast.ai Practical Deep Learning for Coders"],
        "project_idea": "Train a custom vision transformer or text embedding model with distributed data parallel."
    },
    "tensorflow": {
        "name": "TensorFlow",
        "category": "ai_ml",
        "weight": 2.0,
        "related": {"pytorch": 0.75, "keras": 0.9},
        "docs_url": "https://www.tensorflow.org/api_docs",
        "free_courses": ["Coursera DeepLearning.AI TensorFlow Developer", "TensorFlow YouTube Channel"],
        "project_idea": "Train and convert a model for edge deployment using TensorFlow Lite and ONNX."
    },
    "scikit_learn": {
        "name": "Scikit-Learn",
        "category": "ai_ml",
        "weight": 1.9,
        "related": {"pandas": 0.8, "numpy": 0.8},
        "docs_url": "https://scikit-learn.org/stable/",
        "free_courses": ["INRIA - Machine Learning in Python with scikit-learn", "Kaggle Learn Micro-Courses"],
        "project_idea": "Build an end-to-end automated classification pipeline with cross-validation and SHAP explainability."
    },
    "huggingface": {
        "name": "Hugging Face (Transformers)",
        "category": "ai_ml",
        "weight": 2.2,
        "related": {"pytorch": 0.85, "llms": 0.9},
        "docs_url": "https://huggingface.co/docs",
        "free_courses": ["Hugging Face NLP Course", "DeepLearning.AI Open Source Models with Hugging Face"],
        "project_idea": "Fine-tune a quantized instruction model using LoRA and evaluate perplexity on custom benchmarks."
    },
    "langchain": {
        "name": "LangChain",
        "category": "ai_ml",
        "weight": 2.0,
        "related": {"langgraph": 0.85, "rag": 0.85, "llms": 0.9},
        "docs_url": "https://python.langchain.com/docs/",
        "free_courses": ["DeepLearning.AI LangChain for LLM Application Development"],
        "project_idea": "Build a multi-tool autonomous agent that extracts data, executes Python scripts, and summarizes results."
    },
    "langgraph": {
        "name": "LangGraph",
        "category": "ai_ml",
        "weight": 2.2,
        "related": {"langchain": 0.9, "llms": 0.9},
        "docs_url": "https://langchain-ai.github.io/langgraph/",
        "free_courses": ["LangChain Academy - Introduction to LangGraph"],
        "project_idea": "Design a resilient multi-agent cyclical workflow with human-in-the-loop validation and state persistence."
    },
    "llms": {
        "name": "Large Language Models (LLMs)",
        "category": "ai_ml",
        "weight": 2.2,
        "related": {"rag": 0.85, "prompt_engineering": 0.8},
        "docs_url": "https://platform.openai.com/docs/guides/text-generation",
        "free_courses": ["DeepLearning.AI Generative AI for Everyone", "Andrej Karpathy - Intro to Large Language Models"],
        "project_idea": "Build an LLM routing proxy that dynamically selects between local Ollama and cloud models by latency and cost."
    },
    "rag": {
        "name": "RAG (Retrieval-Augmented Generation)",
        "category": "ai_ml",
        "weight": 2.2,
        "related": {"vector_databases": 0.9, "llms": 0.9},
        "docs_url": "https://docs.llamaindex.ai/en/stable/",
        "free_courses": ["DeepLearning.AI Building Systems with ChatGPT", "LlamaIndex University"],
        "project_idea": "Develop a hybrid dense+sparse retrieval pipeline with cross-encoder re-ranking for complex PDF manuals."
    },
    "vector_databases": {
        "name": "Vector Databases (Chroma/Pinecone/Qdrant/Milvus)",
        "category": "ai_ml",
        "weight": 2.0,
        "related": {"rag": 0.85, "postgresql": 0.6},
        "docs_url": "https://docs.trychroma.com/",
        "free_courses": ["Pinecone Vector Database 101", "Qdrant Course"],
        "project_idea": "Implement a real-time semantic document search engine with cosine and dot-product vector indices."
    },
    "nlp": {
        "name": "Natural Language Processing (NLP)",
        "category": "ai_ml",
        "weight": 2.0,
        "related": {"llms": 0.85, "spacy": 0.8},
        "docs_url": "https://spacy.io/usage",
        "free_courses": ["Stanford CS224N: Natural Language Processing with Deep Learning"],
        "project_idea": "Build a custom Named Entity Recognition model for extracting technical competencies from job postings."
    },
    "computer_vision": {
        "name": "Computer Vision",
        "category": "ai_ml",
        "weight": 2.0,
        "related": {"pytorch": 0.75, "opencv": 0.85},
        "docs_url": "https://docs.opencv.org/",
        "free_courses": ["Stanford CS231N: Deep Learning for Computer Vision"],
        "project_idea": "Deploy a real-time object detection and segmentation service using YOLOv8 and TensorRT."
    },
    "mlops": {
        "name": "MLOps",
        "category": "ai_ml",
        "weight": 2.0,
        "related": {"docker": 0.8, "kubernetes": 0.75, "ci_cd": 0.75},
        "docs_url": "https://ml-ops.org/",
        "free_courses": ["Coursera Machine Learning Engineering for Production (MLOps)", "Made With ML MLOps Guide"],
        "project_idea": "Configure an automated ML pipeline with MLflow experiment tracking, DVC data versioning, and CI testing."
    },
    "prompt_engineering": {
        "name": "Prompt Engineering",
        "category": "ai_ml",
        "weight": 1.5,
        "related": {"llms": 0.85},
        "docs_url": "https://www.promptingguide.ai/",
        "free_courses": ["Learn Prompting Course", "DeepLearning.AI Prompt Engineering for Developers"],
        "project_idea": "Create an automated few-shot prompt optimizer that evaluates and self-corrects extraction accuracy."
    },

    # ------------------- DATABASES & DATA ENGINEERING -------------------
    "postgresql": {
        "name": "PostgreSQL",
        "category": "databases_data",
        "weight": 2.0,
        "related": {"sql": 0.85, "mysql": 0.75},
        "docs_url": "https://www.postgresql.org/docs/",
        "free_courses": ["PostgreSQL Tutorial (postgresqltutorial.com)", "CMU Database Systems (15-445)"],
        "project_idea": "Implement full-text search, JSONB indexing, and pgvector embeddings in a unified PostgreSQL database."
    },
    "mongodb": {
        "name": "MongoDB",
        "category": "databases_data",
        "weight": 1.8,
        "related": {"nosql": 0.85, "redis": 0.6},
        "docs_url": "https://www.mongodb.com/docs/",
        "free_courses": ["MongoDB University - Free Courses"],
        "project_idea": "Construct a high-throughput time-series analytics storage engine with aggregation pipelines."
    },
    "redis": {
        "name": "Redis",
        "category": "databases_data",
        "weight": 1.8,
        "related": {"postgresql": 0.5},
        "docs_url": "https://redis.io/docs/",
        "free_courses": ["Redis University RU101"],
        "project_idea": "Build a distributed cache with sliding-window rate limiting and Pub/Sub message broker."
    },
    "apache_kafka": {
        "name": "Apache Kafka",
        "category": "databases_data",
        "weight": 2.2,
        "related": {"event_driven": 0.8, "apache_spark": 0.75},
        "docs_url": "https://kafka.apache.org/documentation/",
        "free_courses": ["Confluent Kafka Developer Course", "freeCodeCamp Kafka Course"],
        "project_idea": "Build an event-driven streaming fraud detection engine processing thousands of messages/sec."
    },
    "apache_spark": {
        "name": "Apache Spark (PySpark)",
        "category": "databases_data",
        "weight": 2.2,
        "related": {"python": 0.7, "hadoop": 0.7},
        "docs_url": "https://spark.apache.org/docs/latest/",
        "free_courses": ["Databricks Community Edition Tutorials", "edX Big Data with Spark"],
        "project_idea": "Process terabyte-scale clickstream event logs into Parquet partitioned lakes with Spark SQL."
    },
    "snowflake": {
        "name": "Snowflake",
        "category": "databases_data",
        "weight": 2.0,
        "related": {"bigquery": 0.8, "sql": 0.75},
        "docs_url": "https://docs.snowflake.com/",
        "free_courses": ["Snowflake Hands-on Essentials Badge Series"],
        "project_idea": "Build an automated ELT pipeline transforming raw JSON staging tables into analytics dimensional marts."
    },
    "bigquery": {
        "name": "Google BigQuery",
        "category": "databases_data",
        "weight": 2.0,
        "related": {"snowflake": 0.8, "gcp": 0.85},
        "docs_url": "https://cloud.google.com/bigquery/docs",
        "free_courses": ["Google Cloud Skills Boost - BigQuery Basics"],
        "project_idea": "Query public datasets with partitioned tables, clustering, and BigQuery ML models."
    },
    "elasticsearch": {
        "name": "Elasticsearch",
        "category": "databases_data",
        "weight": 1.9,
        "related": {"opensearch": 0.9, "vector_databases": 0.65},
        "docs_url": "https://www.elastic.co/guide/index.html",
        "free_courses": ["Elasticsearch Complete Guide on YouTube"],
        "project_idea": "Build a typo-tolerant e-commerce product search with faceted navigation and BM25 scoring."
    },
    "data_warehousing": {
        "name": "Data Warehousing (Kimball / Star Schema)",
        "category": "databases_data",
        "weight": 1.9,
        "related": {"snowflake": 0.8, "sql": 0.8},
        "docs_url": "https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/",
        "free_courses": ["DataCamp Introduction to Data Warehousing"],
        "project_idea": "Model and populate a dimensional star schema with slowly changing dimensions (SCD Type 2)."
    },

    # ------------------- CLOUD & DEVOPS -------------------
    "aws": {
        "name": "Amazon Web Services (AWS)",
        "category": "cloud_devops",
        "weight": 2.0,
        "related": {"gcp": 0.8, "azure": 0.8},
        "docs_url": "https://docs.aws.amazon.com/",
        "free_courses": ["AWS Skill Builder - Cloud Practitioner Essentials", "freeCodeCamp AWS Course"],
        "project_idea": "Provision a serverless REST architecture using AWS Lambda, API Gateway, DynamoDB, and CloudFront."
    },
    "gcp": {
        "name": "Google Cloud Platform (GCP)",
        "category": "cloud_devops",
        "weight": 2.0,
        "related": {"aws": 0.8, "azure": 0.8},
        "docs_url": "https://cloud.google.com/docs",
        "free_courses": ["Google Cloud Skills Boost Free Tier", "Coursera GCP Fundamentals"],
        "project_idea": "Deploy a containerized microservice on Google Cloud Run with Cloud SQL and Secret Manager."
    },
    "azure": {
        "name": "Microsoft Azure",
        "category": "cloud_devops",
        "weight": 2.0,
        "related": {"aws": 0.8, "gcp": 0.8},
        "docs_url": "https://learn.microsoft.com/en-us/azure/",
        "free_courses": ["Microsoft Learn - Azure Fundamentals (AZ-900)"],
        "project_idea": "Deploy an enterprise solution using Azure App Service, Azure Key Vault, and Azure Cosmos DB."
    },
    "docker": {
        "name": "Docker",
        "category": "cloud_devops",
        "weight": 2.0,
        "related": {"kubernetes": 0.85, "linux": 0.7},
        "docs_url": "https://docs.docker.com/",
        "free_courses": ["Docker Curriculum (docker-curriculum.com)", "freeCodeCamp Docker Course"],
        "project_idea": "Build multi-stage production Docker images with non-root security profiles and minimal size."
    },
    "kubernetes": {
        "name": "Kubernetes (K8s)",
        "category": "cloud_devops",
        "weight": 2.2,
        "related": {"docker": 0.85, "helm": 0.8},
        "docs_url": "https://kubernetes.io/docs/home/",
        "free_courses": ["KubeAcademy by VMware", "Kubernetes Official Tutorials"],
        "project_idea": "Deploy an auto-scaling microservice cluster with Ingress, cert-manager SSL, and ConfigMaps."
    },
    "terraform": {
        "name": "Terraform (IaC)",
        "category": "cloud_devops",
        "weight": 2.0,
        "related": {"ansible": 0.7, "aws": 0.75},
        "docs_url": "https://developer.hashicorp.com/terraform/docs",
        "free_courses": ["HashiCorp Learn Terraform Tutorials", "freeCodeCamp Terraform Course"],
        "project_idea": "Write modular Infrastructure as Code to provision an entire multi-region VPC with state locking."
    },
    "ci_cd": {
        "name": "CI/CD Pipelines (GitHub Actions / GitLab CI)",
        "category": "cloud_devops",
        "weight": 2.0,
        "related": {"docker": 0.75, "git": 0.8},
        "docs_url": "https://docs.github.com/en/actions",
        "free_courses": ["GitHub Skills - Continuous Integration", "GitLab CI/CD Guide"],
        "project_idea": "Build an automated pipeline that lints, runs matrix unit tests, builds Docker containers, and deploys."
    },
    "linux": {
        "name": "Linux / Unix Administration",
        "category": "cloud_devops",
        "weight": 1.8,
        "related": {"bash": 0.85},
        "docs_url": "https://tldp.org/LDP/intro-linux/html/",
        "free_courses": ["Linux Foundation - Introduction to Linux (edX)", "Linux Journey (linuxjourney.com)"],
        "project_idea": "Harden an Ubuntu/Debian server with SSH keys, UFW firewall, fail2ban, and automated patch cron."
    },

    # ------------------- DEVELOPER TOOLS -------------------
    "git": {
        "name": "Git & GitHub",
        "category": "developer_tools",
        "weight": 1.8,
        "related": {"ci_cd": 0.7},
        "docs_url": "https://git-scm.com/doc",
        "free_courses": ["Pro Git Book (Free)", "Learn Git Branching Interactive Tutorial"],
        "project_idea": "Establish a production Git branching workflow with protected branches, semantic release, and PR templates."
    },
    "pytest": {
        "name": "Pytest / Automated Testing",
        "category": "developer_tools",
        "weight": 1.7,
        "related": {"python": 0.8},
        "docs_url": "https://docs.pytest.org/",
        "free_courses": ["TestDriven.io Testing Guides", "Real Python Testing in Python"],
        "project_idea": "Write a thorough suite with parameterization, fixtures, mock HTTP servers, and code coverage >90%."
    },
    "postman": {
        "name": "Postman / API Testing",
        "category": "developer_tools",
        "weight": 1.4,
        "related": {"rest_api": 0.8},
        "docs_url": "https://learning.postman.com/docs/",
        "free_courses": ["Postman Academy Badges"],
        "project_idea": "Create an automated Postman test collection with environment variables and Newman CLI CI integration."
    },

    # ------------------- CERTIFICATIONS -------------------
    "aws_certified": {
        "name": "AWS Certified Solutions Architect / Developer",
        "category": "certifications",
        "weight": 1.8,
        "related": {"aws": 0.95},
        "docs_url": "https://aws.amazon.com/certification/",
        "free_courses": ["freeCodeCamp AWS Certified Solutions Architect Associate Course"],
        "project_idea": "Design an enterprise disaster-recovery architecture meeting 99.99% availability SLA."
    },
    "cka": {
        "name": "CKA (Certified Kubernetes Administrator)",
        "category": "certifications",
        "weight": 1.9,
        "related": {"kubernetes": 0.95},
        "docs_url": "https://www.cncf.io/certification/cka/",
        "free_courses": ["Kubernetes The Hard Way by Kelsey Hightower"],
        "project_idea": "Bootstrap a production Kubernetes cluster from scratch using containerd and systemd services."
    },
    "gcp_data_engineer": {
        "name": "GCP Professional Data Engineer",
        "category": "certifications",
        "weight": 1.8,
        "related": {"gcp": 0.9, "bigquery": 0.85},
        "docs_url": "https://cloud.google.com/learn/certification/data-engineer",
        "free_courses": ["Google Cloud Training Courses on Coursera"],
        "project_idea": "Build a streaming data pipeline with Cloud Pub/Sub, Dataflow, and BigQuery analytics."
    },

    # ------------------- SOFT SKILLS & PRACTICES -------------------
    "system_design": {
        "name": "System Design & Architecture",
        "category": "soft_skills",
        "weight": 2.0,
        "related": {"microservices": 0.85, "rest_api": 0.7},
        "docs_url": "https://github.com/donnemartin/system-design-primer",
        "free_courses": ["System Design Primer on GitHub", "ByteByteGo YouTube Channel"],
        "project_idea": "Author an Architectural Decision Record (ADR) and high-level diagram for a distributed URL shortener."
    },
    "agile_scrum": {
        "name": "Agile / Scrum Methodologies",
        "category": "soft_skills",
        "weight": 1.4,
        "related": {"jira": 0.7},
        "docs_url": "https://scrumguides.org/",
        "free_courses": ["Scrum.org Open Assessments", "Atlassian Agile Coach"],
        "project_idea": "Run sprint planning, backlog grooming, and write user stories with acceptance criteria."
    },
    "code_review": {
        "name": "Code Review & Technical Mentorship",
        "category": "soft_skills",
        "weight": 1.6,
        "related": {"git": 0.7},
        "docs_url": "https://google.github.io/eng-practices/review/",
        "free_courses": ["Google Engineering Practices Documentation"],
        "project_idea": "Review open-source pull requests adhering to industry conventions, readability, and security standards."
    },
    "problem_solving": {
        "name": "Analytical Problem Solving",
        "category": "soft_skills",
        "weight": 1.7,
        "related": {"system_design": 0.6},
        "docs_url": "https://en.wikipedia.org/wiki/Problem_solving",
        "free_courses": ["MIT OpenCourseWare Introduction to Algorithms (6.006)"],
        "project_idea": "Analyze and optimize an algorithmic bottleneck from O(N^2) to O(N log N) with telemetry."
    },
}

# Alias Map: maps common variations, colloquialisms, and acronyms to canonical skill ID
ALIAS_MAP: Dict[str, str] = {
    # Languages
    "js": "javascript",
    "javascript": "javascript",
    "vanilla js": "javascript",
    "ecmascript": "javascript",
    "es6": "javascript",
    "ts": "typescript",
    "typescript": "typescript",
    "py": "python",
    "python": "python",
    "python3": "python",
    "python 3": "python",
    "golang": "go",
    "go": "go",
    "rust": "rust",
    "rustlang": "rust",
    "cpp": "c++",
    "c++": "c++",
    "c plus plus": "c++",
    "c#": "c#",
    "c-sharp": "c#",
    "csharp": "c#",
    "java": "java",
    "kotlin": "kotlin",
    "scala": "scala",
    "r": "r",
    "r language": "r",
    "rlang": "r",
    "bash": "bash",
    "shell": "bash",
    "sh": "bash",
    "zsh": "bash",
    "powershell": "bash",
    "sql": "sql",
    "structured query language": "sql",

    # Frameworks & Libraries
    "fastapi": "fastapi",
    "fast api": "fastapi",
    "django": "django",
    "django rest framework": "django",
    "drf": "django",
    "flask": "flask",
    "react": "react",
    "reactjs": "react",
    "react.js": "react",
    "next": "nextjs",
    "nextjs": "nextjs",
    "next.js": "nextjs",
    "node": "nodejs",
    "nodejs": "nodejs",
    "node.js": "nodejs",
    "express": "express",
    "expressjs": "express",
    "express.js": "express",
    "vue": "vue",
    "vuejs": "vue",
    "vue.js": "vue",
    "angular": "angular",
    "angularjs": "angular",
    "tailwind": "tailwind",
    "tailwindcss": "tailwind",
    "tailwind css": "tailwind",
    "spring": "spring_boot",
    "spring boot": "spring_boot",
    "springboot": "spring_boot",
    "graphql": "graphql",
    "rest": "rest_api",
    "rest api": "rest_api",
    "restful": "rest_api",
    "restful apis": "rest_api",
    "rest apis": "rest_api",

    # AI & ML
    "pytorch": "pytorch",
    "torch": "pytorch",
    "tensorflow": "tensorflow",
    "tf": "tensorflow",
    "scikit-learn": "scikit_learn",
    "scikit": "scikit_learn",
    "sklearn": "scikit_learn",
    "huggingface": "huggingface",
    "hugging face": "huggingface",
    "transformers": "huggingface",
    "langchain": "langchain",
    "langgraph": "langgraph",
    "lang graph": "langgraph",
    "llm": "llms",
    "llms": "llms",
    "large language model": "llms",
    "large language models": "llms",
    "genai": "llms",
    "generative ai": "llms",
    "rag": "rag",
    "retrieval augmented generation": "rag",
    "retrieval-augmented generation": "rag",
    "vector db": "vector_databases",
    "vector database": "vector_databases",
    "vector databases": "vector_databases",
    "chroma": "vector_databases",
    "chromadb": "vector_databases",
    "pinecone": "vector_databases",
    "qdrant": "vector_databases",
    "milvus": "vector_databases",
    "weaviate": "vector_databases",
    "faiss": "vector_databases",
    "nlp": "nlp",
    "natural language processing": "nlp",
    "spacy": "nlp",
    "nltk": "nlp",
    "computer vision": "computer_vision",
    "cv": "computer_vision",
    "opencv": "computer_vision",
    "yolo": "computer_vision",
    "mlops": "mlops",
    "machine learning operations": "mlops",
    "mlflow": "mlops",
    "prompt engineering": "prompt_engineering",
    "prompt design": "prompt_engineering",

    # Databases & Data
    "postgres": "postgresql",
    "postgresql": "postgresql",
    "psql": "postgresql",
    "mongo": "mongodb",
    "mongodb": "mongodb",
    "redis": "redis",
    "kafka": "apache_kafka",
    "apache kafka": "apache_kafka",
    "spark": "apache_spark",
    "apache spark": "apache_spark",
    "pyspark": "apache_spark",
    "snowflake": "snowflake",
    "bigquery": "bigquery",
    "google bigquery": "bigquery",
    "elasticsearch": "elasticsearch",
    "elastic search": "elasticsearch",
    "opensearch": "elasticsearch",
    "data warehouse": "data_warehousing",
    "data warehousing": "data_warehousing",
    "dwh": "data_warehousing",
    "star schema": "data_warehousing",
    "snowflake schema": "data_warehousing",

    # Cloud & DevOps
    "aws": "aws",
    "amazon web services": "aws",
    "amazon aws": "aws",
    "gcp": "gcp",
    "google cloud": "gcp",
    "google cloud platform": "gcp",
    "azure": "azure",
    "microsoft azure": "azure",
    "docker": "docker",
    "containerization": "docker",
    "containers": "docker",
    "k8s": "kubernetes",
    "kubernetes": "kubernetes",
    "kube": "kubernetes",
    "terraform": "terraform",
    "iac": "terraform",
    "infrastructure as code": "terraform",
    "ci/cd": "ci_cd",
    "cicd": "ci_cd",
    "ci cd": "ci_cd",
    "github actions": "ci_cd",
    "gitlab ci": "ci_cd",
    "jenkins": "ci_cd",
    "continuous integration": "ci_cd",
    "continuous deployment": "ci_cd",
    "linux": "linux",
    "unix": "linux",
    "ubuntu": "linux",
    "centos": "linux",
    "redhat": "linux",

    # Developer Tools
    "git": "git",
    "github": "git",
    "gitlab": "git",
    "pytest": "pytest",
    "unit testing": "pytest",
    "automated testing": "pytest",
    "postman": "postman",

    # Certifications
    "aws certified": "aws_certified",
    "aws solutions architect": "aws_certified",
    "cka": "cka",
    "certified kubernetes administrator": "cka",
    "gcp data engineer": "gcp_data_engineer",

    # Soft Skills & Architecture
    "system design": "system_design",
    "software architecture": "system_design",
    "microservices": "system_design",
    "distributed systems": "system_design",
    "agile": "agile_scrum",
    "scrum": "agile_scrum",
    "kanban": "agile_scrum",
    "code review": "code_review",
    "code reviews": "code_review",
    "mentorship": "code_review",
    "problem solving": "problem_solving",
    "critical thinking": "problem_solving",
    "analytical skills": "problem_solving",
}


def normalize_skill_name(raw_text: str) -> Optional[str]:
    """Normalize a raw skill string to its canonical taxonomy ID.
    
    Handles punctuation, case differences, and known alias mappings.
    Returns None if not recognized.
    """
    if not raw_text:
        return None
    
    cleaned = raw_text.strip().lower()
    
    # Direct alias match
    if cleaned in ALIAS_MAP:
        return ALIAS_MAP[cleaned]
    
    # Strip non-alphanumeric except '+', '#', '.', '-', '/'
    sanitized = re.sub(r"[^\w\+\#\.\-\/ ]", "", cleaned)
    if sanitized in ALIAS_MAP:
        return ALIAS_MAP[sanitized]
    
    # Check canonical dictionary keys directly
    if sanitized in SKILL_TAXONOMY:
        return sanitized
        
    return None


def get_skill_metadata(skill_id: str) -> Optional[dict]:
    """Retrieve complete metadata for a canonical skill ID."""
    if skill_id in SKILL_TAXONOMY:
        meta = SKILL_TAXONOMY[skill_id].copy()
        meta["id"] = skill_id
        return meta
    return None


def get_all_canonical_skills() -> List[dict]:
    """Return list of all canonical skills with category and metadata."""
    results = []
    for skill_id, data in SKILL_TAXONOMY.items():
        item = data.copy()
        item["id"] = skill_id
        results.append(item)
    return results


def calculate_skill_similarity(skill_a_id: str, skill_b_id: str) -> float:
    """Calculate semantic similarity coefficient between two canonical skills.
    
    Returns:
        1.0 for identical skill
        0.5 - 0.95 for related skills mapped in ontology
        0.2 for skills sharing the same broad category
        0.0 for unrelated skills
    """
    if not skill_a_id or not skill_b_id:
        return 0.0
    if skill_a_id == skill_b_id:
        return 1.0
    
    data_a = SKILL_TAXONOMY.get(skill_a_id)
    data_b = SKILL_TAXONOMY.get(skill_b_id)
    
    if not data_a or not data_b:
        return 0.0
        
    # Check explicitly documented relation
    related_a = data_a.get("related", {})
    if skill_b_id in related_a:
        return float(related_a[skill_b_id])
        
    related_b = data_b.get("related", {})
    if skill_a_id in related_b:
        return float(related_b[skill_a_id])
        
    # Same category bonus
    if data_a.get("category") == data_b.get("category"):
        return 0.2
        
    return 0.0
