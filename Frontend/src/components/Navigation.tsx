import { useState } from "react";
import { FiMenu, FiX } from "react-icons/fi";
import { NavLink } from "react-router-dom";

const Navigation = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div className="container mx-auto px-4 sm:px-6 py-4">
        <div className="flex items-center justify-between">
          <NavLink to="/" className="text-xl font-semibold font-inter text-foreground">
            Khaerul®
          </NavLink>

          {/* Hamburger for mobile */}
          <button
            className="md:hidden p-2 rounded focus:outline-none focus:ring-2 focus:ring-primary"
            onClick={() => setMenuOpen((v) => !v)}
            aria-label={menuOpen ? "Close menu" : "Open menu"}
          >
            {menuOpen ? <FiX className="w-7 h-7" /> : <FiMenu className="w-7 h-7" />}
          </button>

          {/* Desktop nav links */}
          <div className="hidden md:flex items-center space-x-8">
            <NavLink
              to="/"
              className={({ isActive }) =>
                `font-inter text-sm transition-all duration-200 transform hover:scale-105 hover:shadow-md ${
                  isActive ? "text-primary" : "text-muted-foreground hover:text-foreground"
                }`
              }
            >
              Home
            </NavLink>
            <NavLink
              to="/about"
              className={({ isActive }) =>
                `font-inter text-sm transition-all duration-200 transform hover:scale-105 hover:shadow-md ${
                  isActive ? "text-primary" : "text-muted-foreground hover:text-foreground"
                }`
              }
            >
              About
            </NavLink>
            <NavLink
              to="/projects"
              className={({ isActive }) =>
                `font-inter text-sm transition-all duration-200 transform hover:scale-105 hover:shadow-md ${
                  isActive ? "text-primary" : "text-muted-foreground hover:text-foreground"
                }`
              }
            >
              Projects
            </NavLink>
            <NavLink
              to="/blog"
              className="bg-primary text-primary-foreground px-4 py-2 rounded-lg text-sm font-inter transition-all duration-200 transform hover:scale-105 hover:shadow-lg"
            >
              Blog
            </NavLink>
          </div>
        </div>

        {/* Mobile nav links dropdown */}
        {menuOpen && (
          <div className="md:hidden mt-4 bg-background rounded-lg shadow-lg border border-border py-4 px-6 flex flex-col space-y-4 animate-fade-in-down">
            <NavLink
              to="/"
              className={({ isActive }) =>
                `font-inter text-base transition-all duration-200 transform hover:scale-105 hover:shadow-md ${
                  isActive ? "text-primary" : "text-muted-foreground hover:text-foreground"
                }`
              }
              onClick={() => setMenuOpen(false)}
            >
              Home
            </NavLink>
            <NavLink
              to="/about"
              className={({ isActive }) =>
                `font-inter text-base transition-all duration-200 transform hover:scale-105 hover:shadow-md ${
                  isActive ? "text-primary" : "text-muted-foreground hover:text-foreground"
                }`
              }
              onClick={() => setMenuOpen(false)}
            >
              About
            </NavLink>
            <NavLink
              to="/projects"
              className={({ isActive }) =>
                `font-inter text-base transition-all duration-200 transform hover:scale-105 hover:shadow-md ${
                  isActive ? "text-primary" : "text-muted-foreground hover:text-foreground"
                }`
              }
              onClick={() => setMenuOpen(false)}
            >
              Projects
            </NavLink>
            <NavLink
              to="/blog"
              className="bg-primary text-primary-foreground px-4 py-2 rounded-lg text-base font-inter transition-all duration-200 transform hover:scale-105 hover:shadow-lg"
              onClick={() => setMenuOpen(false)}
            >
              Blog
            </NavLink>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navigation;