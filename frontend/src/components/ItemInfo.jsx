import { useState, useEffect } from 'react';
import './ItemInfo.css'
import earthIcon from '../assets/earth.png';

function ItemInfo(props) {
    const [open, setOpen] = useState(false);
    const [tab, setTab] = useState("impact");

    const processText = (str) => {
        const colonIndex = str.indexOf(':');
        if (colonIndex === -1) {
          // If no colon found, return text without underlining
          return <span>{str}</span>;
        }
        
        return (
          <>
            <span className="underline">{str.slice(0, colonIndex + 1)}</span>
            {str.slice(colonIndex + 1)}
          </>
        );
      };

    const toggle = () => {
        setOpen(!open);
      };

    return (
        <div className="ItemInfo">
            <button className="button" onClick={toggle}>{props.label}</button>
            {open && (
            <div className="toggle">
                <div className="card-container">
                    {/* Image Section */}
                    {/* <img 
                        src="/mnt/data/image.png" 
                        alt="Recycling Bins" 
                        className="card-image"
                    /> */}

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
                            <strong><p>Environmental Impact of Manufacturing:</p></strong>
                            {props.impact.map((r, i) => (
                                <>
                                    <p key={i}>{processText(r)}</p>
                                </>
                            ))}

                            <br />

                            <strong><p>Environmental Impact of Regular Use:</p></strong>
                            {props.current_impact.map((r, i) => (
                                <p key={i}>{r}</p>
                            ))}
                        </>
                    ) : (
                        <>
                            <strong><p>Alternatives:</p></strong>
                            {props.alternatives.map((r, i) => (
                                <div key={i}>
                                    <p>{processText(r.name)}{r.company !== "N/A" ? ` - ${r.company}` : ""}</p>
                                    <p>{r.description}</p>
                                    <p>{r.link !== "N/A" ? r.link : ""}</p>
                                    <br />
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