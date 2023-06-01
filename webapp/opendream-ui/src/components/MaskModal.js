import { useEffect, useState, useRef } from "react";
import { Modal, Button, Select } from "antd";
import { Stage, Layer, Image, Line } from "react-konva";

// mask should have context of the size of the image
const MaskModal = ({ imgSrc, title, open, handleOk, handleCancel }) => {
  const [windowImg, setWindowImg] = useState(null);
  const [tool, setTool] = useState("pen");
  const [lines, setLines] = useState([]);
  const isDrawing = useRef(false);
  const stageRef = useRef(null);

  useEffect(() => {
    function getImage(src) {
      return new Promise(function (resolve, reject) {
        const img = new window.Image();
        img.src = src;
        img.onload = function () {
          resolve(img);
        };
        img.crossOrigin = "Anonymous";
        img.error = function (e) {
          reject(e);
        };
      });
    }
    getImage(imgSrc).then(setWindowImg);
  }, [imgSrc]);

  const reset = () => {
    setLines([]);
    setTool("pen");
  };

  const getCanvasURI = () => {
    const offScreenCanvas = document.createElement("canvas");
    offScreenCanvas.width = windowImg.width;
    offScreenCanvas.height = windowImg.height;
    const ctx = offScreenCanvas.getContext("2d");

    // Fill the off-screen canvas with black color
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, windowImg.width, windowImg.height);

    // Draw the masked area using only white lines
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.strokeStyle = "white";
    lines.forEach((line) => {
      ctx.lineWidth = line.tool === "eraser" ? 0 : 50;
      ctx.beginPath();
      ctx.moveTo(line.points[0], line.points[1]);
      for (let i = 2; i < line.points.length; i += 2) {
        ctx.lineTo(line.points[i], line.points[i + 1]);
      }
      ctx.stroke();
    });

    return offScreenCanvas.toDataURL();
  };

  const handleMouseDown = (e) => {
    isDrawing.current = true;
    const pos = e.target.getStage().getPointerPosition();
    setLines([...lines, { tool, points: [pos.x, pos.y] }]);
  };

  const handleMouseMove = (e) => {
    if (!isDrawing.current) {
      return;
    }
    const stage = e.target.getStage();
    const point = stage.getPointerPosition();
    let lastLine = lines[lines.length - 1];
    lastLine.points = lastLine.points.concat([point.x, point.y]);
    lines.splice(lines.length - 1, 1, lastLine);
    setLines(lines.concat());
  };

  const handleMouseUp = () => {
    isDrawing.current = false;
  };

  return (
    <Modal
      title={`[MASK] ${title}`}
      open={open}
      onOk={() => handleOk(getCanvasURI())}
      onCancel={handleCancel}
      width={window.innerWidth}
      top={0}
      style={{ top: 20 }}
      footer={[
        <Button type="secondary" onClick={reset}>
          Reset
        </Button>,
        <Button
          key="submit"
          type="primary"
          htmlType="submit"
          onClick={() => handleOk(getCanvasURI())}
          className="bg-blue-800"
        >
          Submit
        </Button>,
      ]}
    >
      <Select
        defaultValue="pen"
        style={{ width: 120 }}
        options={[
          { value: "pen", label: "Pen" },
          { value: "eraser", label: "Eraser" },
        ]}
        onChange={(value) => setTool(value)}
      />
      <div className="flex items-center justify-center">
        <Stage
          width={600}
          height={600}
          onMouseDown={handleMouseDown}
          onMousemove={handleMouseMove}
          onMouseup={handleMouseUp}
          ref={stageRef}
        >
          <Layer>
            <Image
              image={windowImg}
              width={512}
              height={512}
              opacity={0.8}
            ></Image>
          </Layer>
          <Layer>
            {lines.map((line, i) => (
              <Line
                key={i}
                points={line.points}
                stroke="white"
                strokeWidth={50}
                tension={0.5}
                lineCap="round"
                lineJoin="round"
                globalCompositeOperation={
                  line.tool === "eraser" ? "destination-out" : "source-over"
                }
              />
            ))}
          </Layer>
        </Stage>
      </div>
    </Modal>
  );
};

export default MaskModal;
