import { GitFork } from "lucide-react";
import { Link } from "react-router-dom";

export function Footer() {
  return (
    <footer className="mt-20">
      <div className="mx-auto flex w-full max-w-4xl flex-col items-center justify-between gap-4 px-4 py-6 sm:flex-row sm:px-6">
        {/* Logo */}
        <div className="text-center sm:text-left">
          <Link to="/" className="font-semibold tracking-tight">
            ShareLink
          </Link>

          <p className="mt-1 text-xs text-muted-foreground">
            Simple and temporary file sharing.
          </p>
        </div>

        {/* Copyright */}
        <p className="text-center text-xs text-muted-foreground">
          © {new Date().getFullYear()}{" "}
          <span className="font-medium">amitbhagat621@gmail.com</span> - All
          rights reserved.
        </p>

        {/* Links */}
        <nav className="flex items-center gap-5">
          <a
            href="/#home"
            className="text-xs font-semibold text-muted-foreground transition-colors hover:text-foreground"
          >
            Home
          </a>

          <a
            href="/#api"
            className="text-xs font-semibold text-muted-foreground transition-colors hover:text-foreground"
          >
            API
          </a>

          <a
            href="/#about"
            className="text-xs font-semibold text-muted-foreground transition-colors hover:text-foreground"
          >
            About
          </a>

          <a
            href="https://github.com"
            target="_blank"
            rel="noreferrer"
            aria-label="GitHub"
            className="text-muted-foreground transition-colors hover:text-foreground"
          >
            <GitFork className="h-4 w-4" />
          </a>
        </nav>
      </div>
    </footer>
  );
}
