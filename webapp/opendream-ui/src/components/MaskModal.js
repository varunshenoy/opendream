import { useEffect, useState, useRef } from "react";
import { Modal, Button, Select } from "antd";
import { Stage, Layer, Image, Line } from "react-konva";

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
    return stageRef.current.toDataURL();
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
              width={600}
              height={600}
              opacity={0.8}
            ></Image>
          </Layer>
          <Layer>
            {lines.map((line, i) => (
              <Line
                key={i}
                points={line.points}
                stroke="black"
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
