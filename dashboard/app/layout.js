import localFont from "next/font/local";
import "./globals.css";

const fd = localFont({
  src: "./fonts/fd.ttf",
  variable: "--fd"
});
const ku = localFont({
  src: "./fonts/ku.ttf",
  variable: "--ku"
});
export const metadata = {
  title: "Dashboard",
  description: "",
};

export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <body className={`${ku.variable} ${fd.variable}`}>
        {children}
      </body>
    </html>
  );
}
