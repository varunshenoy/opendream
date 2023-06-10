import React, { useState } from "react";
import { ScrollText } from "lucide-react";
import { Modal } from "antd";

// TODO: have this show the actual workflow 
const ViewWorkflowButton = ({currentState}) => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <>
      <Modal
        title={"Workflow"}
        open={isModalOpen}
        onOk={() => {setIsModalOpen(false)}}
        onCancel={() => {setIsModalOpen(false)}}
        width={window.innerWidth}
        style={{ maxWidth: 600 }}
        footer={[]}
      >
        {currentState && currentState.map((layer, index) => {
          return <div key={index} class="flex flex-col py-2">
            <span class="font-bold text-base">Layer {layer.id} - {layer.metadata.op}</span>
            {layer.metadata.params && <>
              <span class="font-bold">Parameters:</span>
              <div class="flex flex-col">{layer.metadata.params.map(param => (
                <span class="pl-8">{param}</span>
              ))}</div>
            </>}
            {layer.metadata.options && Object.keys(layer.metadata.options).length > 0 && <>
              <span class="font-bold">Options:</span>
              <div class="flex flex-col">{Object.entries(layer.metadata.options).map(([key, value]) => (
                <span class="pl-8"><span class="underline">{key}</span>: {value}</span>
              ))}</div>
            </>}
          </div>
        })}
      </Modal>
      <a
        onClick={setIsModalOpen}
        className="flex items-center justify-center rounded-md bg-zinc-900 w-full px-3.5 py-2.5 my-4 text-sm font-semibold text-white shadow-sm hover:bg-zinc-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-zinc-600"
      >
        View Workflow
        <ScrollText size={18} class="ml-2"></ScrollText>
      </a>
    </>
  );
};

export default ViewWorkflowButton;
