import React from "react";
import { Layers, ArrowUpFromLine, Forward, Boxes, Link } from "lucide-react";
import { useState } from "react";
import { Button, Modal, Input, message } from "antd";

export const Navbar = ({ setCurrentState, setImage }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [extensionLink, setExtensionLink] = useState("");
  const [messageApi, contextHolder] = message.useMessage();

  const showModal = () => {
    setIsModalOpen(true);
  };

  const success = () => {
    messageApi.open({
      type: "success",
      content: "Extension sucessfully loaded 🎉",
    });
  };

  const handleOk = () => {
    const downloadExtension = async (url) => {
      try {
        // POST request using fetch with async/await
        const response = await fetch("http://127.0.0.1:8000/save_extension/", {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ link: url }),
        });
        const responseData = await response.json();

        console.log(responseData);
      } catch (error) {
        console.error("Error fetching data:", error);
        setIsModalOpen(false);
      }
    };

    downloadExtension(extensionLink).then(() => {
      console.log("downloaded extension");
      setExtensionLink("");
      success();
      setIsModalOpen(false);
      window.location.reload(true);
    });
  };
  const handleCancel = () => {
    setIsModalOpen(false);
  };

  const downloadWorkflow = () => {
    const getLayerData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/state/");
        const responseData = await response.json();
        console.log(responseData);

        return responseData["workflow"];
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    getLayerData().then((currentWorkflow) => {
      const element = document.createElement("a");
      const file = new Blob([JSON.stringify(currentWorkflow)], {
        type: "application/json",
      });
      element.href = URL.createObjectURL(file);
      element.download = "workflow.json";
      document.body.appendChild(element); // Required for this to work in FireFox
      element.click();
    });
  };

  const uploadWorkflow = () => {
    const input = document.createElement("input");
    input.type = "file";
    // accept only json files
    input.accept = ".json";
    // click the input to trigger the file picker
    input.click();

    input.onchange = (e) => {
      const file = e.target.files[0];
      const reader = new FileReader();
      reader.readAsText(file, "UTF-8");
      reader.onload = (readerEvent) => {
        const content = readerEvent.target.result;
        const workflow = JSON.parse(content);
        console.log(workflow);

        const postWorkflow = async (workflow) => {
          try {
            // POST request using fetch with async/await
            const response = await fetch(
              "http://127.0.0.1:8000/load_workflow/",
              {
                method: "POST",
                headers: {
                  Accept: "application/json",
                  "Content-Type": "application/json",
                },
                body: JSON.stringify(workflow),
              }
            );
            const responseData = await response.json();

            console.log(responseData);
            setCurrentState(responseData["layers"].reverse());
            setImage(responseData["layers"][0]["image"]);
          } catch (error) {
            console.error("Error fetching data:", error);
          }
        };

        postWorkflow(workflow).then(() => {
          console.log("workflow loaded");
        });
      };
    };
  };

  return (
    <>
      {contextHolder}
      <Modal
        title="Load an Extension"
        open={isModalOpen}
        onCancel={handleCancel}
        footer={[<Button onClick={handleOk}>Download</Button>]}
      >
        <p className="pt-2 pb-4 text-xs italic">
          Installing an extension will refresh your state. Please save before
          proceeding.
        </p>
        <Input
          size="large"
          placeholder="Enter a URL (e.g. a file on GitHub)"
          prefix={<Link />}
          onInput={(e) => setExtensionLink(e.target.value)}
        />
      </Modal>
      <nav class="border-b border-zinc-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex items-center justify-between h-16">
            <div class="flex items-center">
              <div class="flex-shrink-0 flex items-center">
                <h1 class="text-grey-900 font-bold text-2xl">Opendream</h1>
                <Layers class="ml-2"></Layers>
              </div>
            </div>
            <div class="hidden md:block">
              <div class="ml-auto flex items-center">
                <div class="ml-10 flex items-baseline space-x-4">
                  <a
                    onClick={showModal}
                    class="flex items-center text-zinc-900 cursor-pointer hover:bg-zinc-200 hover:text-black px-3 py-2 rounded-md text-sm font-medium transition-all duration-300 ease-in-out transform hover:scale-110"
                  >
                    Load Extension
                    <Boxes class="ml-2" size={18}></Boxes>
                  </a>
                  <a
                    onClick={uploadWorkflow}
                    class="flex items-center text-zinc-900 cursor-pointer hover:bg-zinc-200 hover:text-black px-3 py-2 rounded-md text-sm font-medium transition-all duration-300 ease-in-out transform hover:scale-110"
                  >
                    Load Workflow
                    <ArrowUpFromLine class="ml-2" size={18}></ArrowUpFromLine>
                  </a>

                  <a
                    onClick={downloadWorkflow}
                    class="flex items-center text-zinc-900 cursor-pointer hover:bg-zinc-200 hover:text-black px-3 py-2 rounded-md text-sm font-medium transition-all duration-300 ease-in-out transform hover:scale-110"
                  >
                    Export Workflow
                    <Forward class="ml-2" size={18}></Forward>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </nav>
    </>
  );
};
