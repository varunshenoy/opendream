import React from "react";
import { Layers } from "lucide-react";

export const Navbar = ({ setCurrentState, setImage }) => {
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
            const response = await fetch("http://127.0.0.1:8000/load_workflow/", {
              method: "POST",
              headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
              },
              body: JSON.stringify(workflow),
            });
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
      }
    }
  }


  return (
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

                {/* // TODO: this needs to show a filepicker, and that file should become a layer */}
                <a 
                  onClick={uploadWorkflow}
                  class="text-zinc-900 cursor-pointer hover:bg-zinc-200 hover:text-black px-3 py-2 rounded-md text-sm font-medium transition-all duration-300 ease-in-out transform hover:scale-110"
                >
                  Load
                </a>
                <a
                  onClick={downloadWorkflow}
                  class="text-zinc-900 cursor-pointer hover:bg-zinc-200 hover:text-black px-3 py-2 rounded-md text-sm font-medium transition-all duration-300 ease-in-out transform hover:scale-110"
                >
                  Export
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};
