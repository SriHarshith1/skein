import type { Metadata } from "next";
import { Big_Shoulders, Literata, Martian_Mono } from "next/font/google";
import "@xyflow/react/dist/style.css";
import "./globals.css";

const shoulders = Big_Shoulders({ variable: "--font-shoulders", subsets: ["latin"], weight: ["600", "800"] });
const literata = Literata({ variable: "--font-literata", subsets: ["latin"], weight: ["400", "500", "600"] });
const martian = Martian_Mono({ variable: "--font-martian", subsets: ["latin"], weight: ["400"] });

export const metadata: Metadata = {
  title: "Skein",
  description: "Lore timelines you can edit, with alternate continuities, relationship graphs and a lore Q&A agent.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${shoulders.variable} ${literata.variable} ${martian.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
