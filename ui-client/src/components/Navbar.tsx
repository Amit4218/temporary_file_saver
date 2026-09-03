import { GitFork, Moon, Sun } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

export function NavBarComponent() {
  return (
    <nav className="sticky top-0 z-50 w-full border-b bg-background/95 p-2 font-bold backdrop-blur supports-backdrop-filter:bg-background/60">
      <div className="mx-auto flex h-10 max-w-7xl items-center justify-between px-4">
        {/* 1. Logo */}
        <div className="flex flex-1 items-center">
          <Link to="/" className="text-xl font-bold tracking-tight">
            ShareLink
          </Link>
        </div>

        {/* 2. Navigation Links */}
        <div className="hidden flex-1 items-center justify-center gap-8 md:flex">
          <a
            href="/#home"
            className="scroll-mt-24 text-xs font-semibold text-muted-foreground transition-colors hover:text-foreground"
          >
            Home
          </a>

          <a
            href="/#api"
            className="scroll-mt-24 text-xs font-semibold text-muted-foreground transition-colors hover:text-foreground"
          >
            Api
          </a>

          <a
            href="/#about"
            hrefLang=""
            className="scroll-mt-24 text-xs font-semibold text-muted-foreground transition-colors hover:text-foreground"
          >
            About
          </a>
        </div>

        {/* 3. Actions */}
        <div className="flex flex-1 items-center justify-end gap-2">
          {/* Theme Switcher */}
          <Button variant="ghost" size="icon" aria-label="Toggle theme">
            <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
            <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
          </Button>

          {/* GitHub */}
          <Button variant="ghost" size="icon" asChild>
            <Link
              to="https://github.com/Amit4218"
              target="_blank"
              rel="noreferrer"
              aria-label="GitHub"
            >
              <GitFork className="h-5 w-5" />
            </Link>
          </Button>
        </div>
      </div>
    </nav>
  );
}
