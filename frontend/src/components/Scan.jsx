import React from 'react';
import "../App.css";

import Camera from './Camera.jsx';
import Info from './Info.jsx';

import { Routes, Route } from 'react-router-dom';

function Scan() {
  return (
   <div className="Scan">
    <Camera />
    <Info />
   </div>
  );
}

export default Scan;