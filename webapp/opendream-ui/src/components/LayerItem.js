import { useState } from "react";
import { Paintbrush2, Eye, Trash2, EyeOff } from "lucide-react";
import MaskModal from "./MaskModal";

const LayerItem = ({ imgSrc, title, isMask, setCurrentState, setImage }) => {
  const [isVisible, setIsVisible] = useState(true);
  const [isMaskModalOpen, setIsMaskModalOpen] = useState(false);

  const showMaskModal = () => {
    setIsMaskModalOpen(true);
  };

  const handleOk = (URI) => {
    // send post request to backend
    const postMask = async (URI) => {
      try {
        // POST request using fetch with async/await
        const response = await fetch("http://127.0.0.1:8000/add_mask/", {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ mask: URI }),
        });

        const responseData = await response.json();
        console.log(responseData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    const getLayerData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/state/");
        const responseData = await response.json();
        console.log(responseData);

        setCurrentState(responseData["layers"].reverse());

        setImage(responseData["layers"][0]["image"]);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    postMask(URI).then(() => {
      getLayerData().then(() => {
        setIsMaskModalOpen(false);
      });
    });
  };
  const handleCancel = () => {
    setIsMaskModalOpen(false);
  };

  return (
    <div class="p-6 flex justify-between items-center py-4">
      <MaskModal
        imgSrc={imgSrc}
        title={title}
        open={isMaskModalOpen}
        handleOk={handleOk}
        handleCancel={handleCancel}
      />
      <span class="flex items-center text-left">
        <img
          src={imgSrc}
          alt="Layer icon"
          class={`w-20 h-20 mr-4 ${isVisible ? "" : "opacity-50"}`}
          onClick={() => {
            setImage(imgSrc);
          }}
        />
        Layer {title}
        {isMask && (
          <span class="inline-block ml-2 px-2 py-1 text-xs font-semibold text-white bg-indigo-600 rounded-md">
            MASK
          </span>
        )}
      </span>
      <div class="flex text-right space-x-2">
        <a
          onClick={() => showMaskModal()}
          class="text-zinc-500 hover:text-zinc-900"
        >
          <Paintbrush2 size={18}></Paintbrush2>
        </a>
        <a
          onClick={() => setIsVisible(!isVisible)}
          class="text-zinc-500 hover:text-zinc-900"
        >
          {isVisible ? <Eye size={18}></Eye> : <EyeOff size={18}></EyeOff>}
        </a>
        <a href="#" class="text-zinc-500 hover:text-zinc-900">
          <Trash2 size={18}></Trash2>
        </a>
      </div>
    </div>
  );
};

export default LayerItem;
