import type { Metadata, Viewport } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "Agentic RAG — Research workspace", description: "Ask questions across your documents with an agentic retrieval-augmented generation assistant." };
export const viewport: Viewport = { width: "device-width", initialScale: 1, themeColor: "#101113" };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en" suppressHydrationWarning><body>{children}</body></html>; }
