"use client";

import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import Link from "next/link";
import { useState, useEffect } from "react";

const geistSans = localFont({
    src: "./fonts/GeistVF.woff",
    variable: "--font-geist-sans",
    weight: "100 900",
});
const geistMono = localFont({
    src: "./fonts/GeistMonoVF.woff",
    variable: "--font-geist-mono",
    weight: "100 900",
});

// export const metadata: Metadata = {
//     title: "Create Next App",
//     description: "Generated by create next app",
// };

export default function RootLayout({
                                       children,
                                   }: Readonly<{
    children: React.ReactNode;
}>) {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [username, setUsername] = useState<string | null>(null);

    useEffect(() => {
        const updateAuthStatus = () => {
            const token = sessionStorage.getItem("authToken");
            const user = sessionStorage.getItem("username");
            setIsLoggedIn(!!token);
            setUsername(user);
        };

        // Nasłuch na zdarzenie
        window.addEventListener("storageUpdate", updateAuthStatus);

        // Wywołanie początkowe
        updateAuthStatus();

        return () => {
            window.removeEventListener("storageUpdate", updateAuthStatus);
        };
    }, []);


    const handleLogout = () => {
        sessionStorage.removeItem("authToken");
        sessionStorage.removeItem("username");
        window.dispatchEvent(new Event("storageUpdate"));
        setIsLoggedIn(false);
        setUsername(null);
    };

    return (
        <html lang="en">
        <body className="bg-custom-bg min-h-screen">
        <div className="bg-neutral-500 text-white py-3">
            <div className="container mx-auto flex justify-between items-center">
                <div className="flex gap-8">
                    <Link href="/" className="text-2xl">Home</Link>
                    {isLoggedIn && (
                        <Link href="/choosePhoto" className="text-2xl">Choose Photo</Link>
                    )}
                </div>
                <div className="flex gap-8 items-center">
                    {isLoggedIn ? (
                        <>
                            <button
                                onClick={handleLogout}
                                className="text-2xl bg-red-500 px-4 py-2 rounded-lg hover:bg-red-600"
                            >
                                Log Out
                            </button>
                        </>
                    ) : (
                        <>
                            <Link href="/login" className="text-2xl">Log in</Link>
                            <Link href="/register" className="text-2xl">Register</Link>
                        </>
                    )}
                </div>

            </div>
        </div>

        <div className="flex justify-center items-center w-full">
            {children}
        </div>
        </body>
        </html>
    );
}
