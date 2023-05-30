import React from "react";
import { Layers } from "lucide-react";

export const Navbar = () => {
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
                <a
                  href="#"
                  class="text-zinc-900 hover:bg-zinc-200 hover:text-black px-3 py-2 rounded-md text-sm font-medium transition-all duration-300 ease-in-out transform hover:scale-110"
                >
                  Import
                </a>
                <a
                  href="#"
                  class="text-zinc-900 hover:bg-zinc-200 hover:text-black px-3 py-2 rounded-md text-sm font-medium transition-all duration-300 ease-in-out transform hover:scale-110"
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
