import React, { useState } from "react";

function Card({ infoContent, resourcesContent }) {
    const [toggle, setToggle] = useState("info");

    return (
        <div className="max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden">
            {/* Image Section */}
            <img src="/path-to-your-image.png" alt="Recycling Bins" className="w-full h-48 object-cover" />

            {/* Toggle Buttons */}
            <div className="flex">
                <button 
                    className={`w-1/2 py-2 ${toggle === "info" ? "bg-green-600 text-white" : "bg-gray-200"}`} 
                    onClick={() => setToggle("info")}
                >
                    Information
                </button>
                <button 
                    className={`w-1/2 py-2 ${toggle === "res" ? "bg-green-600 text-white" : "bg-gray-200"}`} 
                    onClick={() => setToggle("res")}
                >
                    Resources
                </button>
            </div>

            {/* Content Section */}
            <div className="p-4 text-gray-700">
                {toggle === "info" ? (
                    <p>{infoContent}</p>
                ) : (
                    <p>{resourcesContent}</p>
                )}
            </div>
        </div>
    );
}

export default Card;