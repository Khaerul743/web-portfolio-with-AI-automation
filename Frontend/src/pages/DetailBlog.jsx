import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchBlogDetail } from "../service/blog";

const defaultDetail = {
  email: "contact@aiorchestrator.com",
  socials: [
    { name: "LinkedIn", url: "https://linkedin.com/in/aiorchestrator" },
    { name: "GitHub", url: "https://github.com/aiorchestrator" },
    { name: "Twitter", url: "https://twitter.com/aiorchestrator" }
  ],
  copyright: "© 2024 AI Orchestrator. All rights reserved."
};

const DetailBlog = () => {
  const { id } = useParams();
  const [blogDetail, setBlogDetail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const getDetail = async () => {
      setLoading(true);
      setError("");
      const res = await fetchBlogDetail(id);
      if (res && res.data) {
        setBlogDetail(res.data);
      } else {
        setError(res?.error || "Gagal memuat detail blog.");
      }
      setLoading(false);
    };
    getDetail();
  }, [id]);

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center text-lg text-muted-foreground">Loading blog detail...</div>;
  }
  if (error) {
    return <div className="min-h-screen flex items-center justify-center text-lg text-red-500">{error}</div>;
  }
  if (!blogDetail) return null;

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 text-gray-900 font-sans">
      {/* Spacer to push content below fixed navbar */}
      <div className="h-32" style={{ minHeight: 90 }} />
      {/* Header with top padding to avoid navbar overlap */}
      <header className="pt-8 pb-8 px-4 bg-white shadow-sm">
        <div className="max-w-4xl mx-auto">
          <div className="flex flex-wrap gap-2 mb-4">
            {(blogDetail.tags || []).map((tag, i) => (
              <span key={i} className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                {tag.name || tag}
              </span>
            ))}
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-4 text-gray-900 leading-tight">
            {blogDetail.title}
          </h1>
          <div className="flex items-center gap-4 text-gray-600 text-sm">
            <span className="font-medium">By {blogDetail.author}</span>
            <span>•</span>
            <span>{blogDetail.created_at ? new Date(blogDetail.created_at).toLocaleDateString() : "-"}</span>
            <span>•</span>
            <span>{blogDetail.read_time ? `${blogDetail.read_time} min read` : "-"}</span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-4xl mx-auto py-8 px-4">
        <article className="prose prose-lg max-w-none">
          <div className="mb-8 p-6 bg-blue-50 rounded-lg border-l-4 border-blue-500">
            <h2 className="text-2xl font-bold mb-4 text-gray-900">{blogDetail.headline}</h2>
            <p className="text-xl text-gray-700 mb-4 leading-relaxed">{blogDetail.introduction?.hook}</p>
            <p className="text-lg text-gray-600 leading-relaxed">{blogDetail.introduction?.purpose}</p>
          </div>

          {(blogDetail.body || []).map((section, idx) => (
            <section key={idx} className="mb-10">
              {/* Subtitle as list if contains multiple points, with pt-4 for spacing */}
              <div className="pt-4">
                {Array.isArray(section.subtitle)
                  ? (
                    <ul className="list-disc pl-6">
                      {section.subtitle.map((point, i) => (
                        <li key={i} className="text-2xl font-bold mb-2 text-gray-900">{point}</li>
                      ))}
                    </ul>
                  ) : (
                    // If subtitle contains "," or ";" or numbered points, split and render as list
                    typeof section.subtitle === "string" && (section.subtitle.match(/[;,]|\d+\./g))
                      ? (
                        <ul className="list-disc pl-6">
                          {section.subtitle.split(/[,;]|\d+\./).filter(Boolean).map((point, i) => (
                            <li key={i} className="text-2xl font-bold mb-2 text-gray-900">{point.trim()}</li>
                          ))}
                        </ul>
                      ) : (
                        <h3 className="text-2xl font-bold mb-6 text-gray-900 border-b-2 border-gray-200 pb-2">{section.subtitle}</h3>
                      )
                  )
                }
              </div>
              <div className="space-y-4">
                {/* API: section.content bisa string atau array, handle keduanya */}
                {Array.isArray(section.content)
                  ? section.content.map((paragraph, i) => (
                      <p key={i} className="text-gray-700 leading-relaxed text-lg">{paragraph}</p>
                    ))
                  : <p className="text-gray-700 leading-relaxed text-lg">{section.content}</p>
                }
              </div>
            </section>
          ))}

          {blogDetail.conclusion && (
            <section className="mt-12 p-6 bg-green-50 rounded-lg border-l-4 border-green-500">
              <h3 className="text-2xl font-bold mb-4 text-gray-900">Conclusion</h3>
              <p className="text-lg text-gray-700 leading-relaxed">{blogDetail.conclusion}</p>
            </section>
          )}
        </article>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 py-8 px-4 bg-white mt-12">
        <div className="max-w-4xl mx-auto text-center">
          <div className="mb-4">
            <span className="font-semibold text-gray-900">Get in touch: </span>
            <a 
              href={`mailto:${defaultDetail.email}`} 
              className="text-blue-600 hover:text-blue-800 underline transition-colors"
            >
              {defaultDetail.email}
            </a>
          </div>
          <div className="flex justify-center gap-6 mb-4">
            {defaultDetail.socials.map((social, i) => (
              <a 
                key={i} 
                href={social.url} 
                target="_blank" 
                rel="noopener noreferrer" 
                className="text-blue-600 hover:text-blue-800 underline transition-colors font-medium"
              >
                {social.name}
              </a>
            ))}
          </div>
          <div className="text-sm text-gray-500">{defaultDetail.copyright}</div>
        </div>
      </footer>
    </div>
  );
};

export default DetailBlog;