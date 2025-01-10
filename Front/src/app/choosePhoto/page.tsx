"use client";

import React, { useState } from "react";
import axios from "axios";

export default function ChoosePhoto() {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [emotion, setEmotion] = useState<string | null>(null);

    const handleFileChange = (e: Event) => {
        const target = e.target as HTMLInputElement;
        if (target.files && target.files.length > 0) {
            setSelectedFile(target.files[0]);
        } else {
            setSelectedFile(null);
        }
    };

    // Obsługa przeciągania plików do dropboxa
    const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        e.stopPropagation();

        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            setSelectedFile(e.dataTransfer.files[0]);
            e.dataTransfer.clearData();
        }
    };

    const handleFileClick = () => {
        const input = document.createElement("input");
        input.type = "file";
        input.accept = "image/*";
        input.onchange = handleFileChange;
        input.click();
    };

    const handleAccept = async () => {
        if (!selectedFile) {
            alert("Please select a file.");
            return;
        }

        const formData = new FormData();
        formData.append("file", selectedFile);

        try {
            const response = await axios.post(
                "http://localhost:8000/analyze-emotion/", // URL do Twojego backendu
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                }
            );
            setEmotion(response.data.emotion); // Zakładając, że odpowiedź zawiera pole "emotion"
        } catch (error) {
            console.error("Error uploading file", error);
        }
    };

    const handleChangePhoto = () => {
        setSelectedFile(null);
        setEmotion(null);
    };

    return (
        <div className="min-h-screen flex flex-col items-center justify-start gap-8 p-8 bg-custom-bg">
            {/* Tytuł */}
            <div className="border-2 border-neutral-400 bg-neutral-400 p-4 text-center w-full max-w-lg">
                <h1 className="text-4xl font-bold text-white">
                    Choose Your Photo
                </h1>
            </div>

            {/* Dropbox */}
            <div
                className="w-full max-w-lg border-4 border-dashed border-neutral-400 bg-white p-16 rounded-lg cursor-pointer hover:border-neutral-300 transition text-center"
                onClick={handleFileClick}
                onDragOver={handleDragOver}
                onDrop={handleDrop}
            >
                <p className="text-xl text-neutral-500">
                    {selectedFile
                        ? `Selected file: ${selectedFile.name}`
                        : "Drag and drop your file here or click to upload"}
                </p>
            </div>

            {/* Podgląd wybranego zdjęcia */}
            {selectedFile && (
                <div className="border-2 border-neutral-400 bg-neutral-400 p-4 w-full max-w-lg">
                    <p className="text-3xl text-white text-center mb-4">
                        Preview
                    </p>
                    <div className="flex justify-center">
                        <img
                            src={URL.createObjectURL(selectedFile)}
                            alt="Selected file preview"
                            className="max-w-full h-auto border-2 border-neutral-300 mb-4"
                        />
                    </div>

                    <div className="flex justify-center gap-4">
                        <button
                            className="border-2 border-neutral-400 bg-neutral-400 text-white py-2 px-6 rounded-lg hover:bg-neutral-500"
                            onClick={handleAccept}
                        >
                            Accept
                        </button>
                        <button
                            className="border-2 border-neutral-400 bg-neutral-400 text-white py-2 px-6 rounded-lg hover:bg-neutral-500"
                            onClick={handleChangePhoto}
                        >
                            Change Photo
                        </button>
                    </div>
                </div>
            )}

            {/* Display emotion result */}
            {emotion && (
                <div className="mt-4 p-4 bg-green-500 text-white rounded-lg">
                    <h2>Predicted Emotion: {emotion}</h2>
                </div>
            )}
        </div>
    );
}
