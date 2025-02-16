import { useState, useEffect } from 'react';
import './ItemInfo.css'

function ItemInfo(props) {
    const [open, setOpen] = useState(false);
    const [tab, setTab] = useState("impact");

    const toggle = () => {
        setOpen(!open);
      };

    return (
        <div className="ItemInfo">
            <button onClick={toggle}>{props.label}</button>
            {open && (
            <div className="toggle">
                <div className="card-container">
                    {/* Image Section */}
                    <img 
                        src="/mnt/data/image.png" 
                        alt="Recycling Bins" 
                        className="card-image"
                    />

                    {/* Toggle Buttons */}
                    <div className="button-group">
                        <button 
                            className={`button ${tab === "impact" ? "active" : ""}`} 
                            onClick={() => setTab("impact")}
                        >
                            Impact
                        </button>
                        <button 
                            className={`button ${tab === "alter" ? "active" : ""}`} 
                            onClick={() => setTab("alter")}
                        >
                            Alternatives
                        </button>
                    </div>

                    {/* Content Section */}
                    <div className="content">
                    {tab === "impact" ? (
                        <>
                            <strong><p>Impact:</p></strong>
                            {props.impact.map((r, i) => (
                                <p key={i}>{r}</p>
                            ))}

                            <strong><p>Current Impact:</p></strong>
                            {props.current_impact.map((r, i) => (
                                <p key={i}>{r}</p>
                            ))}
                        </>
                    ) : (
                        <>
                            <strong><p>Alternatives:</p></strong>
                            {props.alternatives.map((r, i) => (
                                <div key={i}>
                                    <p>{r.name} - {r.company}</p>
                                    <p>{r.description}</p>
                                    <p>{r.link}</p>
                                </div>
                            ))}
                        </>
                    )}
                    </div>
                </div>
            </div>
            )}
        </div>
    );
}

export default ItemInfo;