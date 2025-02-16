import '../App.css';
import React from 'react';
import { useNavigate } from 'react-router-dom';
import Card from './Card';

function Home() {
    const navigate = useNavigate();

  return (
    <div className="Home">
        <div className="app-name">
            <p>Home</p>
        </div>
        <div className="how-it-works">
            <div className="header">

            </div>
            <div className="desc">

            </div>
        </div>
        <div className="steps">
            <div className="step1">
                <img className="step1-img" />
                <div className="step1-header">

                </div>
                <div className="step1-desc">

                </div>
            </div>
            <img className="arrow-img" />
            <div className="step2">
                <img className="step2-img" />
                <div className="step2-header">
                    
                </div>
                <div className="step2-desc">
                    
                </div>
            </div>
            <img className="arrow-img" />
            <div className="step3">
                <img className="step3-img" />
                <div className="step3-header">
                    
                </div>
                <div className="step3-desc">
                    
                </div>
            </div>
        </div>

        <Card infoContent={"This is infomation"} resourcesContent={"This is some resources"} />
        
        <button onClick={() => navigate('/scan')}>Click</button>
    </div>
  );
}

export default Home;
