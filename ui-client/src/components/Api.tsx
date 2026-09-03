import { useState } from "react";
import { Check, Copy, ExternalLink, Loader2, Play } from "lucide-react";
import exampleImage from "@/example_image.jpg";

const API_ENDPOINT = `${process.env.BUN_PUBLIC_BASE_URL}/api/v1/upload`;

export function ApiPlayground() {
  const [copied, setCopied] = useState(false);
  const [apiLoading, setApiLoading] = useState(false);
  const [apiResponse, setApiResponse] = useState<unknown>(null);
  const [apiStatus, setApiStatus] = useState<number | null>(null);
  const [apiError, setApiError] = useState("");

  const curlCommand = `curl -X POST -F "file=@./example_image.jpg" ${process.env.BUN_PUBLIC_BASE_URL}${API_ENDPOINT}`;

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(curlCommand);

      setCopied(true);

      setTimeout(() => {
        setCopied(false);
      }, 2000);
    } catch (error) {
      console.error("Failed to copy:", error);
    }
  };

  const handleApiTest = async () => {
    setApiLoading(true);
    setApiResponse(null);
    setApiStatus(null);
    setApiError("");

    try {
      // get the example image file
      const imageResponse = await fetch(exampleImage);
      const imageBlob = await imageResponse.blob();

      const formData = new FormData();
      formData.append("file", imageBlob, "example_image.jpg");

      // send the image to the upload endpoint
      const uploadResponse = await fetch(API_ENDPOINT, {
        method: "POST",
        body: formData,
      });

      setApiStatus(uploadResponse.status);

      const contentType = uploadResponse.headers.get("content-type");

      if (contentType?.includes("application/json")) {
        const data = await uploadResponse.json();
        setApiResponse(data);
      } else {
        const text = await uploadResponse.text();
        setApiResponse(text);
      }
    } catch (error) {
      console.error("API request failed:", error);

      setApiError(
        error instanceof Error ? error.message : "Something went wrong.",
      );
    } finally {
      setApiLoading(false);
    }
  };

  const getPreviewUrl = () => {
    if (
      !apiResponse ||
      typeof apiResponse !== "object" ||
      apiResponse === null
    ) {
      return null;
    }

    if ("url" in apiResponse && typeof apiResponse.url === "string") {
      return apiResponse.url;
    }

    return null;
  };

  const previewUrl = getPreviewUrl();

  return (
    <section id="api" className="scroll-mt-24 mb-30">
      <div className="mb-6">
        <h2 className="text-lg font-semibold">Upload via API</h2>

        <p className="mt-1 text-sm text-muted-foreground">
          Upload files programmatically using the ShareLink API.
        </p>
      </div>

      {/* API Playground */}
      <div className="space-y-6">
        {/* Request */}
        <div>
          <div className="mb-2 flex items-center justify-between">
            <span className="text-xs font-semibold">Try it</span>

            <span className="text-xs text-muted-foreground">
              POST {API_ENDPOINT}
            </span>
          </div>

          <div className="grid gap-6 md:grid-cols-2">
            {/* Example Image */}
            <div>
              <p className="mb-2 text-xs text-muted-foreground">Example file</p>

              <div className="overflow-hidden rounded-lg border bg-muted">
                <img
                  src={exampleImage}
                  alt="API example"
                  className="aspect-video w-full object-contain"
                />
              </div>
            </div>

            {/* Request Details */}
            <div className="flex flex-col">
              <p className="mb-2 text-xs text-muted-foreground">Request</p>

              <div className="flex flex-1 flex-col rounded-lg bg-muted p-4">
                <code className="text-xs leading-6">
                  POST {API_ENDPOINT}
                  <br />
                  Content-Type: multipart/form-data
                  <br />
                  <br />
                  file: api-example.png
                </code>

                <button
                  type="button"
                  onClick={handleApiTest}
                  disabled={apiLoading}
                  className="mt-auto flex items-center justify-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {apiLoading ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      Uploading...
                    </>
                  ) : (
                    <>
                      <Play className="h-4 w-4" />
                      Try API
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Response */}
        {(apiResponse !== null || apiError) && (
          <div>
            <div className="mb-2 flex items-center justify-between">
              <span className="text-xs font-semibold">Response</span>

              {apiStatus !== null && (
                <span
                  className={`text-xs font-medium ${
                    apiStatus >= 200 && apiStatus < 300
                      ? "text-green-600"
                      : "text-destructive"
                  }`}
                >
                  HTTP {apiStatus}
                </span>
              )}
            </div>

            {apiError ? (
              <div className="rounded-lg border border-destructive/50 bg-destructive/10 p-4 text-sm text-destructive">
                {apiError}
              </div>
            ) : (
              <pre className="overflow-x-auto rounded-lg bg-muted p-4 text-xs leading-6">
                {typeof apiResponse === "string"
                  ? apiResponse
                  : JSON.stringify(apiResponse, null, 2)}
              </pre>
            )}

            {/* Preview URL */}
            {previewUrl && (
              <a
                href={previewUrl}
                target="_blank"
                rel="noreferrer"
                className="mt-4 inline-flex items-center gap-2 text-sm font-medium text-primary hover:underline"
              >
                Preview uploaded file
                <ExternalLink className="h-4 w-4" />
              </a>
            )}
          </div>
        )}
      </div>

      {/* cURL */}
      <div className="mt-4">
        <span className="text-xs font-semibold">cURL example:</span>

        <div className="mt-2 flex w-full items-center justify-between gap-3 rounded-lg bg-muted p-4">
          <code className="min-w-0 overflow-x-auto text-xs">{curlCommand}</code>

          <button
            type="button"
            onClick={handleCopy}
            className="shrink-0 rounded-md p-2 transition-colors hover:bg-background"
            aria-label={copied ? "Copied" : "Copy cURL command"}
          >
            {copied ? <Check size={15} /> : <Copy size={15} />}
          </button>
        </div>
      </div>
    </section>
  );
}
