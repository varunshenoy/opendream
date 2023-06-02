import React from "react";
import { ScrollText } from "lucide-react";

// TODO: have this show the actual workflow 
const ViewWorkflowButton = () => {
  return (
    <a
      href="#"
      className="flex items-center justify-center rounded-md bg-zinc-900 w-full px-3.5 py-2.5 my-4 text-sm font-semibold text-white shadow-sm hover:bg-zinc-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-zinc-600"
    >
      View Workflow
      <ScrollText size={18} class="ml-2"></ScrollText>
    </a>
  );
};

export default ViewWorkflowButton;
