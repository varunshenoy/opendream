import React from "react";

export const Canvas = () => {
  return (
    <div className="grid grid-cols-1 gap-4 lg:col-span-2">
      <section aria-labelledby="section-1-title">
        <div className="overflow-hidden rounded-md border border-zinc-200 bg-white">
          <div className="p-6">
            <img
              src="https://raw.githubusercontent.com/CompVis/latent-diffusion/main/data/inpainting_examples/overture-creations-5sI6fQgYIuo.png"
              alt="Layer icon"
              class="object-cover w-full h-full"
            ></img>
          </div>
        </div>
      </section>
    </div>
  );
};
