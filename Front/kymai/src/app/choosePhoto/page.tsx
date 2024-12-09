"use client";

import React, { useState } from "react";

const FileUpload = () => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            setSelectedFile(e.target.files[0]);
        } else {
            setSelectedFile(null);
        }
    };

    const handleFileClick = () => {
        const input = document.createElement("input");
        input.type = "file";
        input.accept = "image/*";
        input.onchange = handleFileChange;
        input.click();
    };

    return (
        <div>
            <button onClick={handleFileClick}>Open Gallery</button>
            {selectedFile && (
                <div>
                    <p>Selected file: {selectedFile.name}</p>
                    <img
                        src={URL.createObjectURL(selectedFile)}
                        alt="Selected"
                        style={{ width: "1000px", height: "1000px" }}
                    />
                </div>
            )}
        </div>
    );
};

export default FileUpload;
