import React, { useState, useEffect } from "react";
import { LayersPanel } from "./components/LayersPanel";
import { Navbar } from "./components/Navbar";
import { Canvas } from "./components/Canvas";
import "./App.css";

function App() {
  const [image, setImage] = useState("");

  return (
    <>
      <Navbar />
      <div className="mt-10 pb-8">
        <div className="mx-auto max-w-3xl lg:max-w-7xl">
          <div className="grid grid-cols-1 items-start gap-4 lg:grid-cols-3 lg:gap-8">
            <LayersPanel setImage={setImage} />
            <Canvas image={image} />
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
