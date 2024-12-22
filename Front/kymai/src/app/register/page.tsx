"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";

export default function Register() {
    const [formData, setFormData] = useState({
        name: "",
        email: "",
        password: "",
        confirmPassword: "",
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

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (formData.password !== formData.confirmPassword) {
            setError("Passwords do not match");
            return;
        }

        if (!formData.name || !formData.email || !formData.password) {
            setError("All fields are required");
            return;
        }

        // Tutaj możesz dodać logikę wysyłania danych do API

        setSuccess(true); // Po udanej rejestracji
        setError(null); // Resetujemy błąd
        // Możesz przekierować użytkownika na stronę logowania po rejestracji
        router.push("/login");
    };

    return (
        <div className="min-h-screen flex flex-col items-center justify-center p-8 bg-custom-bg">
            <div className="border-2 border-neutral-400 bg-neutral-400 p-8 w-full max-w-lg">
                <h1 className="text-4xl font-bold text-white text-center mb-6">Register</h1>

                {/* Komunikat o błędzie */}
                {error && <p className="text-red-500 text-center mb-4">{error}</p>}

                {/* Komunikat o sukcesie */}
                {success && (
                    <p className="text-green-500 text-center mb-4">Registration successful!</p>
                )}

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-white" htmlFor="name">
                            Name
                        </label>
                        <input
                            id="name"
                            name="name"
                            type="text"
                            value={formData.name}
                            onChange={handleInputChange}
                            className="w-full p-2 rounded-lg border-2 border-neutral-400 bg-neutral-300 text-black"
                            required
                        />
                    </div>

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

                    <div>
                        <label className="block text-white" htmlFor="confirmPassword">
                            Confirm Password
                        </label>
                        <input
                            id="confirmPassword"
                            name="confirmPassword"
                            type="password"
                            value={formData.confirmPassword}
                            onChange={handleInputChange}
                            className="w-full p-2 rounded-lg border-2 border-neutral-400 bg-neutral-300 text-black"
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        className="w-full p-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                    >
                        Register
                    </button>
                </form>
            </div>
        </div>
    );
}