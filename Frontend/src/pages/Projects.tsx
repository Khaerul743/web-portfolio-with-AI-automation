import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { motion } from "framer-motion";
import { Github } from "lucide-react";
import Chatbot from "../components/chatbot";
import cafeShop from "../pictures/cafe_shop.png";

const Projects = () => {
  const projects = [
    {
      id: 1,
      title: "Cafe Shop Online Platform",
      description: "An online coffee ordering website that showcases various coffee products from a local café. Customers can read a short description about the shop, browse the menu, and place orders directly through an online payment system integrated with Midtrans.",
      thumbnail: cafeShop,
      technologies: ["JavaScript", "Express.js", "Midtrans", "MySQL", "Payment Gateway"],
      demoLink: "#",
      githubLink: "#"
    },
    {
      id: 2,
      title: "AI-Powered Financial Assistant 1.0",
      description: "A financial management application equipped with an intelligent chatbot that provides personal finance recommendations based on user transaction data.",
      thumbnail: "https://media.istockphoto.com/id/1185122140/id/foto/konsep-teknologi-finansial.jpg?s=612x612&w=0&k=20&c=kK2xELCgG2WZgJVJmxfpkHiXdl6MdH_Vz5me2GcUo_E=",
      technologies: ["React.js", "MySQL", "LangChain", "Flask", "OpenAI API"],
      demoLink: "#",
      githubLink: "https://github.com/Khaerul743/Financial-management-AI"
    },
    {
      id: 3,
      title: "AI-Powered Financial Assistant 2.0",
      description: "An enhanced version of the financial management app with a smart chatbot that offers personalized financial advice by analyzing user transaction data.",
      thumbnail: "https://media.istockphoto.com/id/2173640157/id/foto/obrolan-chatbot-dengan-ai-kecerdasan-buatan-pengusaha-menggunakan-teknologi-robot-pintar-ai.jpg?s=612x612&w=0&k=20&c=gkLZGns8-cNTDNfL3Y4_kMqPb9QgKHV19bR1qQ-v9_o=",
      technologies: ["React.js", "Express.js", "Flask", "LangChain", "Docker", "Redis", "Nginx"],
      demoLink: "#",
      githubLink: "https://github.com/Khaerul743/finance_ai_project"
    },
    {
      id: 4,
      title: "Inventory Management",
      description: "An inventory management system that provides full CRUD features to create, read, update, and delete product data. Ideal for helping business owners efficiently manage their stock.",
      thumbnail: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=500&h=300&fit=crop",
      technologies: ["Node.js", "Express.js", "MySQL", "Sequelize"],
      demoLink: "#",
      githubLink: "https://github.com/Khaerul743/management-inventory-app-backend"
    },
    {
      id: 5,
      title: "Crypto News & Insights AI Agent",
      description: "An AI agent system powered by LangGraph that automatically gathers the latest cryptocurrency news and data — including events, coin prices, and market updates. The AI analyzes the data to provide recommendations, which are then sent to n8n and forwarded to Telegram.",
      thumbnail: "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?ixid=M3w3ODI5MDF8MHwxfHNlYXJjaHwzfHxjcnlwdG98ZW58MHx8fHwxNzUzNzcyNzc2fDA&ixlib=rb-4.1.0&w=500&h=300&fit=crop",
      technologies: ["LangGraph", "LangChain", "OpenAI", "n8n", "Telegram Bot API", "FastApi"],
      demoLink: "#",
      githubLink: "https://github.com/Khaerul743/Crypto-news-agent"
    }
    
  ];

  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
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
    hidden: { opacity: 0, y: 30 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.5 }
    }
  };

  const cardVariants = {
    hidden: { opacity: 0, scale: 0.9 },
    visible: {
      opacity: 1,
      scale: 1,
      transition: { duration: 0.4 }
    }
  };

  return (
    <>
    <motion.div 
      className="min-h-screen bg-background px-6 pt-24 pb-12"
      initial="hidden"
      animate="visible"
      variants={containerVariants}
    >
      <div className="container mx-auto max-w-6xl">
        <motion.div variants={itemVariants} className="text-center mb-16">
          <h1 className="text-4xl font-bold font-inter text-foreground mb-6">My Projects</h1>
          <p className="text-lg text-muted-foreground font-inter leading-relaxed max-w-3xl mx-auto">
            A collection of projects showcasing my expertise in AI orchestration, backend development, 
            and automation engineering. Each project represents innovative solutions to complex technical challenges.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {projects.map((project, index) => (
            <motion.div
              key={project.id}
              variants={cardVariants}
              custom={index}
              whileHover={{ y: -5 }}
              transition={{ duration: 0.2 }}
            >
              <Card className="bg-card border-border hover:shadow-lg transition-all duration-300 group h-full">
                <div className="relative overflow-hidden rounded-t-lg">
                  <img
                    src={project.thumbnail}
                    alt={project.title}
                    className="w-full h-48 object-cover transition-transform duration-300 group-hover:scale-105"
                  />
                  <div className="absolute inset-0 bg-background/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                </div>
                
                <CardHeader>
                  <CardTitle className="text-xl font-inter text-card-foreground">{project.title}</CardTitle>
                  <CardDescription className="text-muted-foreground font-inter">
                    {project.description}
                  </CardDescription>
                </CardHeader>
                
                <CardContent className="space-y-4">
                  <div className="flex flex-wrap gap-2">
                    {project.technologies.map((tech, index) => (
                      <span
                        key={index}
                        className="px-3 py-1 bg-secondary text-secondary-foreground text-xs rounded-lg font-inter"
                      >
                        {tech}
                      </span>
                    ))}
                  </div>
                  
                  <div className="flex gap-2 pt-2">
                    {/* <Button size="sm" variant="outline" className="flex-1">
                      <ExternalLink className="w-4 h-4 mr-2" />
                      Demo
                    </Button> */}
                    
                    <Button asChild size="sm" variant="outline" className="flex-1">
                      <a href={project.githubLink} target="_blank" rel="noopener noreferrer">
                        <Github className="w-4 h-4 mr-2" />
                        Code
                      </a>
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </motion.div>
    <Chatbot/>
    </>
  );
};

export default Projects;