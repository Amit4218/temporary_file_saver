import { ApiPlayground } from "@/components/Api";
import { FileUploader } from "@/components/FileUpload";

export function Home() {
  return (
    <main id="home" className="min-h-screen bg-background no-scrollbar">
      <div className="mx-auto w-full max-w-4xl px-4 py-16 sm:px-6">
        {/* Page Header */}
        <header className="mb-16 text-center">
          <h1 className="text-2xl font-bold tracking-tight">
            ShareLink - Share your files online using a simple link
          </h1>

          <p className="mt-2 text-muted-foreground">
            All uploaded files are deleted after 60 minutes.
          </p>
        </header>

        {/* File Upload */}
        <section id="file-upload" className="mb-30">
          <div className="mb-6">
            <h2 className="text-lg font-semibold">Upload File</h2>

            <p className="mt-1 text-sm text-muted-foreground">
              Any file up to 25 MB is accepted.
            </p>
          </div>

          <FileUploader />
        </section>

        {/* API */}
        <ApiPlayground />

        {/* About */}
        <section id="about" className="scroll-mt-24">
          <div className="mb-6 pt-10">
            <h2 className="text-lg font-semibold">About ShareLink</h2>

            <p className="mt-1 text-sm text-muted-foreground">
              A simple and lightweight way to share files online.
            </p>
          </div>

          <div className="space-y-8 text-sm leading-6 text-muted-foreground">
            <div>
              <h3 className="mb-2 font-semibold text-foreground">
                Simple file sharing
              </h3>

              <p>
                ShareLink lets you upload a file and instantly get a shareable
                link. No complicated setup or accounts are required to share a
                file.
              </p>
            </div>

            <div>
              <h3 className="mb-2 font-semibold text-foreground">
                Temporary storage
              </h3>

              <p>
                Files uploaded to ShareLink are automatically deleted after 60
                minutes. This keeps the service lightweight and helps prevent
                unnecessary files from staying on the server.
              </p>
            </div>

            <div>
              <h3 className="mb-2 font-semibold text-foreground">
                Built for developers
              </h3>

              <p>
                In addition to the web uploader, ShareLink provides an API that
                allows applications and scripts to upload files
                programmatically.
              </p>
            </div>

            <div className="pt-2">
              <p className="font-medium text-foreground">
                Fast, temporary, and simple.
              </p>

              <p className="mt-1">
                Upload a file, share the link, and let ShareLink handle the
                rest.
              </p>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
