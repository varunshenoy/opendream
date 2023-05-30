import {
  PlusCircle,
  Eye,
  Trash2,
  Paintbrush2,
  ScrollText,
  Layers,
} from "lucide-react";
import "./App.css";
import { Button, Dropdown, Space } from "antd";

const items = [
  {
    key: "0",
    label: <a href="#">Load Image</a>,
  },
  {
    key: "1",
    label: <a href="#">Dream</a>,
  },
  {
    key: "2",
    label: <a href="#">Inpaint</a>,
  },
  {
    key: "3",
    label: <a href="#">Instruct Pix2Pix</a>,
  },
  {
    key: "4",
    label: "ControlNet",
    children: [
      {
        key: "2-1",
        label: "Canny",
      },
      {
        key: "2-2",
        label: "OpenPose",
      },
    ],
  },
];

function App() {
  return (
    <>
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
      <main className="mt-10 pb-8">
        <div className="mx-auto max-w-3xl lg:max-w-7xl">
          <div className="grid grid-cols-1 items-start gap-4 lg:grid-cols-3 lg:gap-8">
            <div className="grid grid-cols-1">
              <section aria-labelledby="section-2-title">
                <div className="overflow-hidden rounded-md border border-zinc-200 bg-white">
                  <div>
                    <div class="p-6 flex justify-between items-center pb-2 border-b border-zinc-20 mb-3">
                      <span class="text-left font-bold text-lg">Layers</span>
                      <span class="text-right">
                        <Space direction="vertical">
                          <Space wrap>
                            <Dropdown
                              menu={{
                                items,
                              }}
                              placement="bottomRight"
                              trigger="click"
                            >
                              <a class="text-zinc-500 hover:text-zinc-900 hover:cursor-pointer">
                                <PlusCircle size={20}></PlusCircle>
                              </a>
                            </Dropdown>
                          </Space>
                        </Space>
                      </span>
                    </div>

                    <div class="p-6 flex justify-between items-center py-4">
                      <span class="flex items-center text-left">
                        <img
                          src="https://raw.githubusercontent.com/CompVis/latent-diffusion/main/data/inpainting_examples/overture-creations-5sI6fQgYIuo.png"
                          alt="Layer icon"
                          class="w-20 h-20 mr-4"
                        ></img>
                        Layer 1
                      </span>
                      <div class="flex text-right space-x-2">
                        <a href="#" class="text-zinc-500 hover:text-zinc-900">
                          <Paintbrush2 size={18}></Paintbrush2>
                        </a>
                        <a href="#" class="text-zinc-500 hover:text-zinc-900">
                          <Eye size={18}></Eye>
                        </a>
                        <a href="#" class="text-zinc-500 hover:text-zinc-900">
                          <Trash2 size={18}></Trash2>
                        </a>
                      </div>
                    </div>

                    <div class="p-6 flex justify-between items-center py-4">
                      <span class="flex items-center text-left">
                        <img
                          src="https://raw.githubusercontent.com/CompVis/latent-diffusion/main/data/inpainting_examples/overture-creations-5sI6fQgYIuo_mask.png"
                          alt="Layer icon"
                          class="w-20 h-20 mr-4"
                        ></img>
                        Layer 2
                        <span class="inline-block ml-2 px-2 py-1 text-xs font-semibold text-white bg-indigo-600 rounded-md">
                          MASK
                        </span>
                      </span>
                      <div class="flex text-right space-x-2">
                        <a href="#" class="text-zinc-500 hover:text-zinc-900">
                          <Paintbrush2 size={18}></Paintbrush2>
                        </a>
                        <a href="#" class="text-zinc-500 hover:text-zinc-900">
                          <Eye size={18}></Eye>
                        </a>
                        <a href="#" class="text-zinc-500 hover:text-zinc-900">
                          <Trash2 size={18}></Trash2>
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              </section>

              <a
                href="#"
                className="flex items-center justify-center rounded-md bg-zinc-900 w-full px-3.5 py-2.5 my-4 text-sm font-semibold text-white shadow-sm hover:bg-zinc-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-zinc-600"
              >
                View Workflow
                <ScrollText size={18} class="ml-2"></ScrollText>
              </a>
            </div>
            {/* Left column */}
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
          </div>
        </div>
      </main>
    </>
  );
}

export default App;
