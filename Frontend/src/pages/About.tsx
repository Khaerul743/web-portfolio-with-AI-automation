import { motion } from "framer-motion";
import { useEffect, useRef, useState } from "react";
import { FaEnvelope, FaPaperPlane, FaPhone, FaRegCommentDots, FaUser } from "react-icons/fa";
import {
  SiCplusplus,
  SiDocker,
  SiExpress,
  SiFlask,
  SiGit,
  SiGithub,
  SiGraphql,
  SiHuggingface,
  SiJavascript,
  SiJupyter,
  SiMongodb,
  SiMysql,
  SiN8N,
  SiNodedotjs,
  SiOpenai,
  SiPostman,
  SiPython,
  SiReact,
  SiRedis,
  SiTensorflow,
  SiTypescript
} from "react-icons/si";
import Chatbot from "../components/chatbot";
import contactImg from "../pictures/contact1.png";

const About = () => {
  const skillCategories = [
    {
      name: "Programming Languages",
      skills: [
        { name: "JavaScript", level: 90, icon: SiJavascript, color: "#F7DF1E" },
        { name: "TypeScript", level: 90, icon: SiTypescript, color: "#3776AB" },
        { name: "Python", level: 90, icon: SiPython, color: "#3776AB" },
        { name: "C++", level: 70, icon: SiCplusplus, color: "#0397ad" },
      ]
    },
    {
      name: "Database",
      skills: [
        { name: "MongoDB", level: 75, icon: SiMongodb, color: "#47A248" },
        { name: "MySQL", level: 85, icon: SiMysql, color: "#4479A1" },
        { name: "Redis", level: 80, icon: SiRedis, color: "#DC382D" }
      ]
    },
    {
      name: "Frameworks & Libraries",
      skills: [
        { name: "React", level: 30, icon: SiReact, color: "#61DAFB" },
        { name: "Node.js", level: 85, icon: SiNodedotjs, color: "#339933" },
        { name: "Express.js", level: 85, icon: SiExpress, color: "#ffffff" },
        { name: "Flask", level: 80, icon: SiFlask, color: "#ffffff" },
        { name: "AI/ML", level: 70, icon: SiTensorflow, color: "#FF6F00" },
        { name: "Autogen", level: 60, icon: SiOpenai, color: "#ffffff" },
        { name: "CrewAI", level: 80, icon: SiOpenai, color: "#ffffff" },
        { name: "Langchain", level: 80, icon: SiOpenai, color: "#ffffff" },
        { name: "Langgraph", level: 85, icon: SiGraphql, color: "#ffffff" },
      ]
    },
    {
      name: "Other Tools",
      skills: [
        { name: "N8n", level: 90, icon: SiN8N, color: "#F05032" },
        { name: "Jupyter Notebook", level: 90, icon: SiJupyter, color: "#F05032" },
        { name: "Huggingface", level: 75, icon: SiHuggingface, color: "#ffffff" },
        { name: "Git", level: 75, icon: SiGit, color: "#F05032" },
        { name: "GitHub", level: 75, icon: SiGithub, color: "#ffffff" },
        { name: "Docker", level: 85, icon: SiDocker, color: "#2496ED" },
        { name: "Postman", level: 85, icon: SiPostman, color: "#F05032" },
      ]
    }
  ];

  const experiences = [
    {
      title: "Agentic AI Orchestrator & AI Engineer",
      company: "Personal Research Project – saving.my.id",
      period: "Present",
      description: "Membangun sistem AI Agent end-to-end untuk analisis keuangan pribadi. Mengimplementasikan reasoning, task delegation, dan memory management dengan LangGraph dan LangChain. AI Agent mampu menjalankan reasoning kompleks, decision-making, serta integrasi ke tools seperti n8n dan Telegram.",
      technologies: ["LangChain", "LangGraph", "OpenAI API", "Docker", "n8n", "React", "flask", "express"]
    },
    {
      title: "Backend Developer & System Architect",
      company: "Independent Project",
      period: "2024 - Present",
      description: "Merancang dan membangun backend scalable menggunakan Express, Flask, Mysql, dan MongoDB. Terlibat langsung dalam pembuatan Arsitektur Microservice, Merancang struktur Database, REST API, manajemen state AI Agent, dan deployment berbasis container di VPS dengan Nginx & HTTPS.",
      technologies: ["Flask", "MongoDB", "Docker", "Nginx", "VPS", "Express", "Mysql"]
    },
    {
      title: "Automation Engineer & Workflow Integrator",
      company: "Self-built Automation Stack",
      period: "Present",
      description: "Menggunakan n8n untuk membangun workflow otomatis yang menghubungkan berbagai layanan seperti AI agent, Telegram, dan webhook custom. Workflow digunakan untuk trigger otomatis, notifikasi, hingga Human-in-the-Loop Approval.",
      technologies: ["n8n", "Webhook", "Telegram Bot", "Flask", "LangChain"]
    }
  ];

  const achievements = [
    {
      title: "AI-Powered Finance Agent",
      description: "Mengembangkan AI agent yang mampu menganalisis pengeluaran, memahami percakapan, dan memberikan insight finansial secara otomatis.",
      metric: "100% AI-driven"
    },
    {
      title: "LangGraph Flow Architect",
      description: "Membangun flow reasoning kompleks dengan node AI agent yang saling berinteraksi secara modular menggunakan LangGraph.",
      metric: "15+ AI nodes"
    },
    {
      title: "Zero-UI DevOps Deployment",
      description: "Menyelesaikan deployment fullstack app berbasis AI agent ke VPS dengan HTTPS, container, dan multi-service routing tanpa antarmuka UI khusus.",
      metric: "100% CLI & API-based"
    },
    {
      title: "Independent Learning & Execution",
      description: "Mempelajari web development dan AI secara mandiri, Membagi waktu antara belajar materi kuliah dan belajar mandiri tentang proses dibalik sebuah sistem dan AI.",
      metric: "Self-Learning"
    }
  ];

  const [inView, setInView] = useState(false);
  const skillsRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setInView(true);
        }
      },
      { threshold: 0.3 }
    );

    if (skillsRef.current) {
      observer.observe(skillsRef.current);
    }

    return () => observer.disconnect();
  }, []);

  const containerVariants = {
    hidden: { opacity: 0, y: 50 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.5 }
    }
  };

  const SkillBar = ({ skill, index }) => {
    const [progress, setProgress] = useState(0);

    useEffect(() => {
      if (inView) {
        const timer = setTimeout(() => {
          setProgress(skill.level);
        }, index * 100);
        return () => clearTimeout(timer);
      }
    }, [inView, skill.level, index]);

    const IconComponent = skill.icon;

    return (
      <motion.div variants={itemVariants} className="space-y-2 sm:space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 sm:gap-3">
            <IconComponent 
              className="w-5 h-5 sm:w-6 sm:h-6 flex-shrink-0" 
              style={{ color: skill.color }} 
            />
            <span className="text-xs sm:text-sm font-medium font-inter text-foreground">
              {skill.name}
            </span>
          </div>
          <span className="text-xs sm:text-sm text-muted-foreground">{skill.level}%</span>
        </div>
        
        <div className="relative w-full bg-secondary rounded-full h-2 sm:h-3 overflow-hidden">
          <div 
            className="h-full bg-primary rounded-full flex items-center justify-end pr-1 sm:pr-2 transition-all duration-1000 ease-out"
            style={{ width: `${progress}%` }}
          >
            {progress > 20 && (
              <span className="text-xs font-medium text-primary-foreground hidden sm:inline">
                {skill.level}%
              </span>
            )}
          </div>
        </div>
      </motion.div>
    );
  };

  const SkillCategory = ({ category, categoryIndex }) => {
    return (
      <motion.div variants={itemVariants} className="space-y-3 sm:space-y-4">
        <h3 className="text-base sm:text-lg font-semibold font-inter text-foreground border-b border-border pb-2">
          {category.name}
        </h3>
        <div className="space-y-3 sm:space-y-4">
          {category.skills.map((skill, skillIndex) => (
            <SkillBar 
              key={skillIndex} 
              skill={skill} 
              index={categoryIndex * 10 + skillIndex} 
            />
          ))}
        </div>
      </motion.div>
    );
  };

  const ExperienceCard = ({ experience, index }) => {
    return (
      <motion.div 
        variants={itemVariants}
        className="bg-card border border-border rounded-lg p-4 sm:p-6 shadow-sm hover:shadow-md transition-shadow duration-300"
      >
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-3 sm:mb-4">
          <div>
            <h3 className="text-base sm:text-lg font-semibold font-inter text-foreground">
              {experience.title}
            </h3>
            <p className="text-sm sm:text-base text-muted-foreground font-inter">
              {experience.company}
            </p>
          </div>
          <span className="text-xs sm:text-sm text-muted-foreground font-inter mt-1 sm:mt-0">
            {experience.period}
          </span>
        </div>
        
        <p className="text-sm sm:text-base text-muted-foreground font-inter leading-relaxed mb-3 sm:mb-4">
          {experience.description}
        </p>
        
        <div className="flex flex-wrap gap-1 sm:gap-2">
          {experience.technologies.map((tech, techIndex) => (
            <span 
              key={techIndex}
              className="px-2 sm:px-3 py-1 bg-secondary text-secondary-foreground rounded-full text-xs sm:text-sm font-medium"
            >
              {tech}
            </span>
          ))}
        </div>
      </motion.div>
    );
  };

  const AchievementCard = ({ achievement, index }) => {
    return (
      <motion.div 
        variants={itemVariants}
        className="bg-card border border-border rounded-lg p-4 sm:p-6 text-center shadow-sm hover:shadow-md transition-shadow duration-300"
      >
        <div className="text-2xl sm:text-3xl font-bold text-primary mb-2 sm:mb-3">
          {achievement.metric}
        </div>
        <h3 className="text-base sm:text-lg font-semibold font-inter text-foreground mb-2">
          {achievement.title}
        </h3>
        <p className="text-sm sm:text-base text-muted-foreground font-inter">
          {achievement.description}
        </p>
      </motion.div>
    );
  };

  return (
    <>
    <motion.div 
      className="min-h-screen bg-background px-4 sm:px-6 lg:px-8 pt-16 sm:pt-20 lg:pt-24 pb-8 sm:pb-12"
      initial="hidden"
      animate="visible"
      variants={containerVariants}
    >
      <div className="container mx-auto max-w-6xl">
        {/* Hero Section */}
        <motion.div variants={itemVariants} className="text-center mb-12 sm:mb-16">
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold font-inter text-foreground mb-4 sm:mb-6">
            About Me
          </h1>
          <p className="text-base sm:text-lg text-muted-foreground font-inter leading-relaxed max-w-4xl mx-auto">
          I'm a backend & AI systems developer focused on building intelligent, agentic, and automated infrastructures.
          From LangGraph to real-world deployment, I turn AI from just a model into a thinking system not just chatbots, but digital problem-solvers.
          </p>
        </motion.div>

        {/* Main Content Grid */}
        <div className="grid lg:grid-cols-2 gap-8 sm:gap-12 mb-12 sm:mb-16">
          {/* Description */}
          <motion.div variants={itemVariants} className="space-y-4 sm:space-y-6">
            {/* <h2 className="text-xl sm:text-2xl font-semibold font-inter text-foreground mb-3 sm:mb-4">
              My Journey
            </h2>
            <p className="text-sm sm:text-base text-muted-foreground font-inter leading-relaxed">
              As an Agentic AI Orchestrator, I design and implement intelligent systems that can work autonomously 
              while maintaining human oversight. My expertise in backend development ensures robust, scalable 
              architectures that power these AI-driven applications.
            </p>
            <p className="text-sm sm:text-base text-muted-foreground font-inter leading-relaxed">
              I believe in creating technology that not only solves complex problems but also enhances human 
              capabilities. Whether it's automating repetitive tasks or building sophisticated AI workflows, 
              I focus on delivering solutions that make a real impact.
            </p>
            <p className="text-sm sm:text-base text-muted-foreground font-inter leading-relaxed">
              My approach combines technical excellence with practical problem-solving, ensuring that every solution 
              is not just innovative but also sustainable and maintainable in the long term.
            </p> */}
            <h2 className="text-xl sm:text-2xl font-semibold font-inter text-foreground mb-3 sm:mb-4">
              My Journey
            </h2>
            <p className="text-sm sm:text-base text-muted-foreground font-inter leading-relaxed">
              As a self-driven Agentic AI Orchestrator, I build systems where intelligent agents, backend logic, and tools work 
              together in harmony not just to respond, but to reason, automate, and take real action. I’ve spent the last few 
              months deep-diving into technologies like LangGraph, CrewAI, and LLM-based architecture to make this possible.
            </p>
            <p className="text-sm sm:text-base text-muted-foreground font-inter leading-relaxed">
              My strength in backend engineering, creating scalable infrastructures that serve as the brain of AI-powered 
              applications. I don’t just write code, I design thinking systems. I focus on what makes the system actually think, respond, and solve problems.
            </p>
            <p className="text-sm sm:text-base text-muted-foreground font-inter leading-relaxed">
              Beyond orchestrating AI agents, I also dive deep into the core of artificial intelligence, exploring areas like 
              machine learning, deep learning, and how large language models operate under the hood. With hands-on experience in 
              frameworks such as TensorFlow and PyTorch, I gain a deeper understanding of how AI systems learn, adapt, and reason. 
              This empowers me not just to integrate AI, but to fine-tune, optimize, and even experiment with custom models tailored 
              for specific real-world use cases.
            </p>
            <p className="text-sm sm:text-base text-muted-foreground font-inter leading-relaxed">
              My mission is to build impactful solutions by leveraging the full potential of AI not just as a tool, 
              but as a collaborator. I believe in practical innovation: building systems that are powerful, adaptive, 
              and ready for the future.
            </p>
          </motion.div>

          {/* Skills */}
          <motion.div variants={itemVariants} className="space-y-6 sm:space-y-8" ref={skillsRef}>
            <h2 className="text-xl sm:text-2xl font-semibold font-inter text-foreground mb-4 sm:mb-6">
              Technical Skills
            </h2>
            <motion.div className="space-y-6 sm:space-y-8" variants={containerVariants}>
              {skillCategories.map((category, index) => (
                <SkillCategory key={index} category={category} categoryIndex={index} />
              ))}
            </motion.div>
          </motion.div>
        </div>

        {/* Achievements Section */}
        <motion.div variants={itemVariants} className="mb-12 sm:mb-16">
          <h2 className="text-xl sm:text-2xl font-semibold font-inter text-foreground text-center mb-6 sm:mb-8">
            Key Achievements
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
            {achievements.map((achievement, index) => (
              <AchievementCard key={index} achievement={achievement} index={index} />
            ))}
          </div>
        </motion.div>

        {/* Experience Section */}
        <motion.div variants={itemVariants}>
          <h2 className="text-xl sm:text-2xl font-semibold font-inter text-foreground text-center mb-6 sm:mb-8">
            Experience
          </h2>
          <div className="space-y-4 sm:space-y-6">
            {experiences.map((experience, index) => (
              <ExperienceCard key={index} experience={experience} index={index} />
            ))}
          </div>
        </motion.div>

        {/* Call to Action */}
        <motion.div variants={itemVariants} className="mt-12 sm:mt-16 flex flex-col md:flex-row items-center justify-center bg-background rounded-2xl shadow-lg p-4 sm:p-8 gap-8">
          {/* Left: Image */}
          <div className="flex-1 flex items-center justify-center w-full md:w-auto">
            <img src={contactImg} alt="Contact" className="max-w-xs sm:max-w-sm md:max-w-md w-full h-auto object-contain" />
          </div>
          {/* Right: Contact Form */}
          <form className="flex-1 w-full max-w-md flex flex-col gap-4">
            <h2 className="text-2xl font-bold font-inter text-white mb-2 text-center md:text-left">Get In <span className="text-primary">Touch</span></h2>
            <div className="flex items-center bg-black border border-white rounded px-3 py-2">
              <FaUser className="text-white mr-2" />
              <input type="text" placeholder="Name" className="flex-1 bg-transparent outline-none text-white placeholder:text-gray-400" required/>
            </div>
            <div className="flex items-center bg-black border border-white rounded px-3 py-2">
              <FaEnvelope className="text-white mr-2" />
              <input type="email" placeholder="Email" className="flex-1 bg-transparent outline-none text-white placeholder:text-gray-400" required/>
            </div>
            <div className="flex items-center bg-black border border-white rounded px-3 py-2">
              <FaPhone className="text-white mr-2" />
              <input type="tel" placeholder="Phone" className="flex-1 bg-transparent outline-none text-white placeholder:text-gray-400" required/>
            </div>
            <div className="flex items-start bg-black border border-white rounded px-3 py-2">
              <FaRegCommentDots className="text-white mr-2 mt-1" />
              <textarea placeholder="Message" className="flex-1 bg-transparent outline-none text-white placeholder:text-gray-400 min-h-[80px] resize-none" required/>
            </div>
            <button type="submit" className="self-end mt-2 bg-primary text-black font-semibold px-8 py-3 rounded-lg shadow hover:scale-105 transition-transform flex items-center gap-2">
              Submit <FaPaperPlane className="ml-1" />
            </button>
          </form>
        </motion.div>
      </div>
    </motion.div>
    <Chatbot/>
    </>
  );
};

export default About;