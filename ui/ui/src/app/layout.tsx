import "~/styles/globals.css";

import Navbar from "~/components/nav/Nav";
import { Inter } from "next/font/google";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
});

export default function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`font-sans ${inter.variable}`}>
          <div className="pr-32">
            {children}
          </div>
          <Navbar/>
      </body>
    </html>
  );
}
