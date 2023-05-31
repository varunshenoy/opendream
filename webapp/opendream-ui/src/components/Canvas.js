import React from "react";

export const Canvas = ({ image }) => {
  return (
    <div className="grid grid-cols-1 gap-4 lg:col-span-2">
      <section aria-labelledby="section-1-title">
        <div className="overflow-hidden rounded-md border border-zinc-200 bg-white">
          <div className="p-6">
            {image !== "" && (
              <img
                src={image}
                alt="Layer image"
                class="object-cover w-full h-full"
              ></img>
            )}
          </div>
        </div>
      </section>
    </div>
  );
};
