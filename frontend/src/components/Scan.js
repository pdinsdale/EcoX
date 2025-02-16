import React from 'react';
import "../App.css";

import Camera from './Camera';
import Info from './Info';

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