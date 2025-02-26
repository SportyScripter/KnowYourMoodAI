"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";

export default function Login() {
    const [formData, setFormData] = useState({
        email: "",
        password: "",
    });

    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState(false);

    const router = useRouter();

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleSubmit = async (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();

        try {
            const response = await fetch('{process.env.NEXT_PUBLIC_API_URL}/login/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `username=${formData.email}&password=${formData.password}`,
            });

            if (!response.ok) {
                throw new Error('Failed to login');
            }

            const data = await response.json();
            sessionStorage.setItem("authToken", data.token);
            sessionStorage.setItem("username", data.username);
            window.dispatchEvent(new Event("storageUpdate"));
            setSuccess(true);

            router.push('/');
        } catch (error) {
            if (error instanceof Error) {
                setError(error.message);
            } else {
                setError('An unknown error occurred');
            }
        }
    };


    return (
        <div className="min-h-screen flex flex-col items-center justify-center p-8 bg-custom-bg">
            <div className="border-2 border-neutral-400 bg-neutral-400 p-8 w-full max-w-lg">
                <h1 className="text-4xl font-bold text-white text-center mb-6">Login</h1>

                {/* Komunikat o błędzie */}
                {error && <p className="text-red-500 text-center mb-4">{error}</p>}

                {/* Komunikat o sukcesie */}
                {success && (
                    <p className="text-green-500 text-center mb-4">Login successful!</p>
                )}

                <form className="space-y-4">
                    <div>
                        <label className="block text-white" htmlFor="email">
                            Email
                        </label>
                        <input
                            id="email"
                            name="email"
                            type="email"
                            value={formData.email}
                            onChange={handleInputChange}
                            className="w-full p-2 rounded-lg border-2 border-neutral-400 bg-neutral-300 text-black"
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-white" htmlFor="password">
                            Password
                        </label>
                        <input
                            id="password"
                            name="password"
                            type="password"
                            value={formData.password}
                            onChange={handleInputChange}
                            className="w-full p-2 rounded-lg border-2 border-neutral-400 bg-neutral-300 text-black"
                            required
                        />
                    </div>

                    <button
                        onClick={handleSubmit}
                        className="w-full p-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                    >
                        Log In
                    </button>
                </form>

                {/* Link do strony rejestracji */}
                <div className="text-center mt-4">
                    <p className="text-white">
                        Don't have an account?{" "}
                        <a href="/register" className="text-blue-500 hover:underline">
                            Register here
                        </a>
                    </p>
                </div>
            </div>
        </div>
    );
}
