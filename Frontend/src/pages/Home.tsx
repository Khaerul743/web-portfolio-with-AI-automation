import { motion } from "framer-motion";
import { FaGithub, FaInstagram, FaLinkedin } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { Typewriter } from "react-simple-typewriter";
import BackroundParticle from "../components/BackroundParticle";
import Chatbot from "../components/chatbot";
import profileImg from "../pictures/profile.jpg";

const Home = () => {
  const roles = [
    "Agentic AI Orchestrator",
    "Backend Developer", 
    "AI Automation Engineer"
  ];
  const navigate = useNavigate();

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        duration: 0.8,
        staggerChildren: 0.2
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: { opacity: 1, y: 0 }
  };

  const photoVariants = {
    hidden: { opacity: 0, scale: 0.8, rotate: -10 },
    visible: { opacity: 1, scale: 1, rotate: 0 }
  };

  const floatingVariants = {
    animate: { y: [0, -10, 0] }
  };

  const glowVariants = {
    animate: {
      boxShadow: [
        "0 0 20px rgba(255, 255, 255, 0.3)",
        "0 0 40px rgba(255, 255, 255, 0.5)",
        "0 0 20px rgba(255, 255, 255, 0.3)"
      ]
    }
  };

  return (
    <>
      <BackroundParticle />
      <motion.div 
        className="min-h-screen bg-gradient-to-br from-background via-background to-background/50 flex items-center justify-center px-4 sm:px-6 lg:px-8 pt-16 sm:pt-20"
        initial="hidden"
        animate="visible"
        variants={containerVariants}
      >
        {/* Background decorative elements */}
        {/* <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-20 left-10 w-72 h-72 bg-white/10 rounded-full blur-3xl opacity-20"></div>
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-gray-500/10 rounded-full blur-3xl opacity-20"></div>
        </div> */}

        <div className="relative w-full max-w-7xl mx-auto">
          <div className="flex flex-col lg:flex-row items-center justify-between gap-8 lg:gap-16">
            {/* Content Section */}
            <div className="flex-1 flex flex-col items-center lg:items-start text-center lg:text-left space-y-4 sm:space-y-6 lg:space-y-8 order-2 lg:order-1">
              <motion.h2 
                variants={itemVariants} 
                transition={{ duration: 0.6, ease: 'easeOut' }}
                className="text-xl sm:text-2xl lg:text-3xl font-inter text-muted-foreground"
              >
                Hi There,
              </motion.h2>
              
              <motion.h1 
                variants={itemVariants} 
                transition={{ duration: 0.6, ease: 'easeOut' }}
                className="text-3xl sm:text-4xl lg:text-5xl xl:text-6xl font-bold font-inter text-foreground leading-tight"
              >
                I'm Khaerul{" "}
                <span>
                  Lutfi
                </span>
              </motion.h1>
              
              <motion.div 
                variants={itemVariants} 
                transition={{ duration: 0.6, ease: 'easeOut' }}
                className="text-base sm:text-lg lg:text-xl xl:text-2xl font-inter text-foreground min-h-[2em]"
              >
                I Am Into{" "}
                <span className="text-primary font-semibold">
                  <Typewriter
                    words={roles}
                    loop={true}
                    cursor
                    cursorStyle="|"
                    typeSpeed={70}
                    deleteSpeed={50}
                    delaySpeed={2000}
                  />
                </span>
              </motion.div>
              
              <motion.button
                variants={itemVariants}
                transition={{ duration: 0.6, ease: 'easeOut' }}
                whileHover={{ 
                  scale: 1.05,
                  boxShadow: "0 10px 25px rgba(0,0,0,0.15)"
                }}
                whileTap={{ scale: 0.95 }}
                className="mt-4 px-8 py-3 sm:px-10 sm:py-4 rounded-full bg-gradient-to-r from-gray-800 to-black text-white font-semibold shadow-lg hover:shadow-xl transition-all duration-300 text-sm sm:text-base"
                onClick={() => navigate("/about")}
              >
                About Me
              </motion.button>
              
              <motion.div 
                variants={itemVariants} 
                transition={{ duration: 0.6, ease: 'easeOut' }}
                className="flex items-center gap-4 sm:gap-6 mt-6"
              >
                {[
                  { Icon: FaLinkedin, url: "https://linkedin.com", color: "hover:text-blue-600" },
                  { Icon: FaGithub, url: "https://github.com", color: "hover:text-gray-800" },
                  { Icon: FaInstagram, url: "https://instagram.com", color: "hover:text-pink-600" }
                ].map(({ Icon, url, color }, index) => (
                  <motion.a
                    key={index}
                    href={url}
                    target="_blank"
                    rel="noopener noreferrer"
                    whileHover={{ scale: 1.2, rotate: 5 }}
                    whileTap={{ scale: 0.9 }}
                    className={`transition-all duration-300 ${color}`}
                    aria-label={`Visit ${Icon.name.replace('Fa', '')}`}
                  >
                    <Icon className="w-6 h-6 sm:w-7 sm:h-7 lg:w-8 lg:h-8" />
                  </motion.a>
                ))}
              </motion.div>
            </div>

            {/* Profile Image Section */}
            <motion.div 
              variants={photoVariants}
              transition={{ duration: 1, ease: 'easeOut', type: 'spring', bounce: 0.4 }}
              animate="animate"
              className="flex-1 flex items-center justify-center order-1 lg:order-2"
            >
              <motion.div
                variants={floatingVariants}
                transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
                animate="animate"
                className="relative"
              >
                <motion.div 
                  variants={glowVariants}
                  transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
                  animate="animate"
                  className="w-48 h-48 sm:w-56 sm:h-56 md:w-64 md:h-64 lg:w-72 lg:h-72 xl:w-80 xl:h-80 rounded-full flex items-center justify-center bg-gradient-to-br from-gray-200 via-white to-gray-300 shadow-2xl relative overflow-hidden"
                >
                  {/* Decorative ring */}
                  <div className="absolute inset-2 rounded-full border-4 border-black/20 animate-pulse"></div>
                  
                  <motion.img
                    src={profileImg}
                    alt="Khaerul Lutfi"
                    className="w-44 h-44 sm:w-52 sm:h-52 md:w-60 md:h-60 lg:w-68 lg:h-68 xl:w-76 xl:h-76 rounded-full object-cover border-4 border-black/30 shadow-inner"
                    whileHover={{ scale: 1.05 }}
                    transition={{ duration: 0.3 }}
                  />
                  
                  {/* Floating particles */}
                  <div className="absolute top-4 right-4 w-2 h-2 bg-black/40 rounded-full animate-ping"></div>
                  <div className="absolute bottom-6 left-6 w-1 h-1 bg-black/60 rounded-full animate-pulse"></div>
                  <div className="absolute top-1/2 left-2 w-1.5 h-1.5 bg-black/30 rounded-full animate-bounce"></div>
                </motion.div>
              </motion.div>
            </motion.div>
          </div>
        </div>
      </motion.div>
      <Chatbot />
    </>
  );
};

export default Home;