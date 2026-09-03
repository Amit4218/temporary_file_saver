import { useEffect, useState } from "react";
import {
  File,
  FileText,
  Image as ImageIcon,
  Music,
  Upload,
  Video,
  X,
} from "lucide-react";
import { Button } from "@/components/ui/button";

const MAX_FILE_SIZE = 25 * 1024 * 1024; // 25 MB

type FileUploaderProps = {
  onFileChange?: (file: File | null) => void;
};

export function FileUploader({ onFileChange }: FileUploaderProps) {
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState("");
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  const handleFile = (selectedFile: File) => {
    setError("");

    if (selectedFile.size > MAX_FILE_SIZE) {
      setFile(null);
      setPreviewUrl(null);
      setError("File size cannot be larger than 25 MB.");
      return;
    }

    setFile(selectedFile);
    onFileChange?.(selectedFile);
  };

  // Automatically remove the error
  useEffect(() => {
    if (!error) return;

    const timeout = setTimeout(() => {
      setError("");
    }, 2500);

    return () => clearTimeout(timeout);
  }, [error]);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];

    if (selectedFile) {
      handleFile(selectedFile);
    }
  };

  const removeFile = () => {
    setFile(null);
    setError("");
    setPreviewUrl(null);
    onFileChange?.(null);
  };

  const submitFile = async () => {
    if (!file || isUploading) return;

    setIsUploading(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(
        `${process.env.BUN_PUBLIC_BASE_URL}/api/v1/upload`,
        {
          method: "POST",
          body: formData,
        },
      );

      if (!response.ok) {
        throw new Error("File upload failed.");
      }

      removeFile();
    } catch (uploadError) {
      setError(
        uploadError instanceof Error
          ? uploadError.message
          : "File upload failed.",
      );
    } finally {
      setIsUploading(false);
    }
  };

  // Create preview URL
  useEffect(() => {
    if (!file) {
      setPreviewUrl(null);
      return;
    }

    const isPreviewable =
      file.type.startsWith("image/") ||
      file.type.startsWith("video/") ||
      file.type.startsWith("audio/") ||
      file.type === "application/pdf";

    if (!isPreviewable) {
      setPreviewUrl(null);
      return;
    }

    const url = URL.createObjectURL(file);

    setPreviewUrl(url);

    return () => {
      URL.revokeObjectURL(url);
    };
  }, [file]);

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";

    const units = ["Bytes", "KB", "MB", "GB"];
    const index = Math.floor(Math.log(bytes) / Math.log(1024));

    return `${(bytes / Math.pow(1024, index)).toFixed(2)} ${units[index]}`;
  };

  const getFileIcon = () => {
    if (!file) {
      return <Upload className="h-8 w-8" />;
    }

    if (file.type.startsWith("image/")) {
      return <ImageIcon className="h-8 w-8" />;
    }

    if (file.type.startsWith("video/")) {
      return <Video className="h-8 w-8" />;
    }

    if (file.type.startsWith("audio/")) {
      return <Music className="h-8 w-8" />;
    }

    if (file.type === "application/pdf") {
      return <FileText className="h-8 w-8" />;
    }

    return <File className="h-8 w-8" />;
  };

  return (
    <div className="w-full space-y-4">
      {/* Upload area */}
      {!file && (
        <div
          className={`w-full cursor-pointer border-2 border-dashed p-10 transition-colors ${
            isDragging
              ? "border-primary bg-primary/5"
              : "border-muted-foreground/25 hover:border-muted-foreground/50"
          }`}
          onDragOver={(event) => {
            event.preventDefault();
            setIsDragging(true);
          }}
          onDragLeave={() => {
            setIsDragging(false);
          }}
          onDrop={(event) => {
            event.preventDefault();
            setIsDragging(false);

            const droppedFile = event.dataTransfer.files?.[0];

            if (droppedFile) {
              handleFile(droppedFile);
            }
          }}
        >
          <div className="flex flex-col items-center justify-center gap-3 text-center">
            <div className="rounded-full bg-muted p-4">
              <Upload className="h-6 w-6 text-muted-foreground" />
            </div>

            <div>
              <p className="font-medium">Drop your file here</p>

              <p className="text-sm text-muted-foreground">
                or click to browse
              </p>
            </div>

            <p className="text-xs text-muted-foreground">
              Any file type · Maximum 25 MB
            </p>

            <Button asChild variant="outline">
              <label className="cursor-pointer">
                Choose file
                <input
                  type="file"
                  className="hidden"
                  onChange={handleInputChange}
                />
              </label>
            </Button>
          </div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="border border-destructive/50 bg-destructive/10 px-4 py-3 text-sm text-destructive">
          {error}
        </div>
      )}

      {/* Selected file */}
      {file && (
        <div className="w-full space-y-4">
          {/* File header */}
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-muted">
              {getFileIcon()}
            </div>

            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-medium">{file.name}</p>

              <p className="text-xs text-muted-foreground">
                {formatFileSize(file.size)}
              </p>
            </div>

            <Button
              variant="ghost"
              size="icon"
              onClick={removeFile}
              aria-label="Remove file"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>

          {/* Image preview */}
          {previewUrl && file.type.startsWith("image/") && (
            <div className="overflow-hidden border">
              <img
                src={previewUrl}
                alt={file.name}
                className="max-h-125 w-full object-contain"
              />
            </div>
          )}

          {/* Video preview */}
          {previewUrl && file.type.startsWith("video/") && (
            <div className="overflow-hidden bg-black">
              <video src={previewUrl} controls className="max-h-125 w-full" />
            </div>
          )}

          {/* Audio preview */}
          {previewUrl && file.type.startsWith("audio/") && (
            <div className="p-4">
              <audio src={previewUrl} controls className="w-full" />
            </div>
          )}

          {/* PDF preview */}
          {previewUrl && file.type === "application/pdf" && (
            <div className="overflow-hidden">
              <iframe
                src={previewUrl}
                title={file.name}
                className="h-125 w-full"
              />
            </div>
          )}

          {/* Unsupported preview */}
          {!previewUrl && (
            <div className="flex flex-col items-center justify-center border border-dashed py-12 text-center">
              {getFileIcon()}

              <p className="mt-3 text-sm font-medium">Preview not available</p>

              <p className="mt-1 text-xs text-muted-foreground">
                This file type cannot be previewed in the browser.
              </p>
            </div>
          )}
          <Button
            className="mt-5 w-full"
            type="button"
            onClick={submitFile}
            disabled={isUploading}
          >
            {isUploading ? "Uploading..." : "Upload file"}
          </Button>
        </div>
      )}
    </div>
  );
}
