import React, { useState } from "react";
import { ScrollText, Download } from "lucide-react";
import { Modal, Card } from "antd";

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
          return (
            <Card
              size="small"
              title={"Layer " + (layer.id).toString()}
              className="mb-4"
            >
              <code>OPERATION: <code className="p-1 bg-slate-100 rounded-md">{layer.metadata.op}</code></code>
                {layer.metadata.params && <div class="pt-2 pb-2">
                  <code className="font-lg">PARAMETERS:</code>
                  <div class="flex flex-col">{layer.metadata.params.map(param => (
                    <span class="pl-2"><code className="ml-2 p-1 bg-slate-100 rounded-md">{param}</code></span>
                  ))}</div>
                </div>}
                {layer.metadata.options && Object.keys(layer.metadata.options).length > 0 && <div class="pb-2">
                  <code>OPTIONS:</code>
                  <div class="flex flex-col">{Object.entries(layer.metadata.options).map(([key, value]) => (
                    <span class="pl-2"><span className="text-gray-500 ">{key}:</span><code className="ml-2 p-1 bg-slate-100 rounded-md">{value}</code></span>
                  ))}</div>
                </div>}
            </Card>
          )
        })}
 
        <a
          href={`data:text/json;charset=utf-8,${encodeURIComponent(JSON.stringify(currentState))}`}
          download="workflow.json"
          className="flex hover:text-white rounded-md bg-violet-950 w-full px-3.5 py-2.5 my-4 text-sm font-semibold text-white shadow-sm hover:bg-violet-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-zinc-600"
        >
          Export Workflow <Download size={18} class="ml-2"></Download>
        </a>
      </Modal>
      <a
        onClick={() => {
          if (currentState) {
            setIsModalOpen(true)
          } else {
            alert("No workflow to view!")
          }
        }}
        className="flex cursor-pointer items-center justify-center rounded-md bg-zinc-900 w-full px-3.5 py-2.5 my-4 text-sm font-semibold text-white shadow-sm hover:bg-zinc-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-zinc-600"
      >
        View Workflow
        <ScrollText size={18} class="ml-2"></ScrollText>
      </a>
    </>
  );
};

export default ViewWorkflowButton;
