import React from "react";
import { Paintbrush2, Eye, Trash2, EyeOff } from "lucide-react";

const LayerItem = ({ imgSrc, title, isMask }) => {
  const [isVisible, setIsVisible] = React.useState(true);

  return (
    <div class="p-6 flex justify-between items-center py-4">
      <span class="flex items-center text-left">
        <img
          src={imgSrc}
          alt="Layer icon"
          class={`w-20 h-20 mr-4 ${isVisible ? "" : "opacity-50"}`}
        />
        {title}
        {isMask && (
          <span class="inline-block ml-2 px-2 py-1 text-xs font-semibold text-white bg-indigo-600 rounded-md">
            MASK
          </span>
        )}
      </span>
      <div class="flex text-right space-x-2">
        <a href="#" class="text-zinc-500 hover:text-zinc-900">
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
