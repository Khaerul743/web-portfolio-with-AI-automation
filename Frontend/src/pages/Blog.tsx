import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { motion } from "framer-motion";
import { Calendar, Clock } from "lucide-react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Chatbot from "../components/chatbot";
import { fetchBlogs } from "../service/blog";

const Blog = () => {
  const navigate = useNavigate();
  const [blogPosts, setBlogPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const getBlogs = async () => {
      setLoading(true);
      setError("");
      const res = await fetchBlogs();
      if (res && res.data) {
        setBlogPosts(res.data);
      } else {
        setError(res?.error || "Gagal memuat data blog.");
      }
      setLoading(false);
    };
    getBlogs();
  }, []);

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
          <h1 className="text-4xl font-bold font-inter text-foreground mb-6">Blog</h1>
          <p className="text-lg text-muted-foreground font-inter leading-relaxed max-w-3xl mx-auto">
            Insights, tutorials, and thoughts on AI orchestration, backend development, automation engineering, 
            and the latest trends in technology.
          </p>
        </motion.div>

        {loading ? (
          <div className="text-center text-muted-foreground py-16">Loading blog posts...</div>
        ) : error ? (
          <div className="text-center text-red-500 py-16">{error}</div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {blogPosts.map((post, index) => (
              <motion.div
                key={post.id}
                variants={cardVariants}
                custom={index}
                whileHover={{ y: -5 }}
                transition={{ duration: 0.2 }}
              >
                <Card className="bg-card border-border hover:shadow-lg transition-all duration-300 group h-full">
                  <div className="relative overflow-hidden rounded-t-lg">
                    <img
                      src={post.thumbnail}
                      alt={post.title}
                      className="w-full h-48 object-cover transition-transform duration-300 group-hover:scale-105"
                    />
                    <div className="absolute top-4 left-4">
                      <span className="px-3 py-1 bg-primary text-primary-foreground text-xs rounded-lg font-inter">
                        {/* Use first tag or fallback */}
                        {post.tags && post.tags.length > 0 ? post.tags[0].name : "Blog"}
                      </span>
                    </div>
                  </div>
                  <CardHeader>
                    <CardTitle className="text-xl font-inter text-card-foreground line-clamp-2">
                      {post.title || post.headline}
                    </CardTitle>
                    <CardDescription className="text-muted-foreground font-inter line-clamp-3">
                      {post.description}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center gap-4 text-sm text-muted-foreground">
                      <div className="flex items-center gap-1">
                        <Calendar className="w-4 h-4" />
                        {/* Format date */}
                        {post.created_at ? new Date(post.created_at).toLocaleDateString() : "-"}
                      </div>
                      <div className="flex items-center gap-1">
                        <Clock className="w-4 h-4" />
                        {post.read_time ? `${post.read_time} min read` : "-"}
                      </div>
                    </div>
                    <Button className="w-full" variant="outline" onClick={() => navigate(`/blog/${post.id}`)}>
                      Read More
                    </Button>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </motion.div>
    <Chatbot/>
    </>
  );
};

export default Blog;