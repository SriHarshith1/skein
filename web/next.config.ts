import type { NextConfig } from "next";

// STATIC_EXPORT=1 builds a read-only copy for GitHub Pages: data comes from
// public/data/*.json, API routes (route.ts) are left out, editing and Ask are hidden.
const STATIC = process.env.STATIC_EXPORT === "1";
const basePath = STATIC ? "/skein" : "";

const nextConfig: NextConfig = {
  output: STATIC ? "export" : undefined,
  basePath,
  trailingSlash: STATIC,
  pageExtensions: STATIC ? ["tsx"] : ["tsx", "ts", "jsx", "js"],
  env: { NEXT_PUBLIC_STATIC: STATIC ? "1" : "", NEXT_PUBLIC_BASE_PATH: basePath },
  serverExternalPackages: ["postgres"],
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
};

export default nextConfig;
