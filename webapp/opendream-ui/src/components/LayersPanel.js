import { useEffect, useState } from "react";
import { PlusCircle } from "lucide-react";
import { Dropdown, Space } from "antd";
import ViewWorkflowButton from "./ViewWorkflowButton";
import LayerItem from "./LayerItem";
import LayerFormModal from "./LayerFormModal";
import { titleCapitalize } from "../App";

export const LayersPanel = () => {
  const [items, setItems] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedMethod, setSelectedMethod] = useState("");
  const [fields, setFields] = useState([]);

  const showModal = (method) => {
    // make query to schema here
    const fetchData = async (method) => {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/schema/" + method + "/"
        );
        const responseData = await response.json();
        const cleanedResponseData = responseData.params.map((param, index) => {
          return {
            type: "input",
            label: param["name"],
            placeholder: param["default"] == null ? "" : param["default"],
          };
        });

        console.log(cleanedResponseData);

        setFields(cleanedResponseData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData(method).then(() => {
      setSelectedMethod(method);
      setIsModalOpen(true);
    });
  };
  const handleOk = () => {
    // setIsModalOpen(false);
  };
  const handleCancel = () => {
    setIsModalOpen(false);
  };

  const onFinish = (values) => {
    console.log("Success:", values);
  };

  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };

  function titleCapitalize(str) {
    return str
      .split("_") // Split the string at underscores
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()) // Capitalize the first character of each word and make the rest lowercase
      .join(" "); // Join the words back together with space
  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/available_operations/"
        );
        const responseData = await response.json();
        const cleanedResponseData = responseData.operators.map(
          (method, index) => {
            return {
              key: index,
              label: (
                <a onClick={() => showModal(method)}>
                  {titleCapitalize(method)}
                </a>
              ),
            };
          }
        );

        console.log(cleanedResponseData);

        setItems(cleanedResponseData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="grid grid-cols-1">
      <LayerFormModal
        title={titleCapitalize(selectedMethod)}
        open={isModalOpen}
        handleOk={handleOk}
        handleCancel={handleCancel}
        onFinish={onFinish}
        onFinishFailed={onFinishFailed}
        fields={fields}
      />
      <section aria-labelledby="section-2-title">
        <div className="overflow-hidden rounded-md border border-zinc-200 bg-white">
          <div>
            <div class="p-6 flex justify-between items-center pb-2 border-b border-zinc-20 mb-3">
              <span class="text-left font-bold text-lg">Layers</span>
              <span class="text-right">
                <Space direction="vertical">
                  <Space wrap>
                    <Dropdown
                      menu={{ items }}
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

            <LayerItem
              imgSrc="https://raw.githubusercontent.com/CompVis/latent-diffusion/main/data/inpainting_examples/overture-creations-5sI6fQgYIuo.png"
              title="Layer 1"
              isMask={false}
            />

            <LayerItem
              imgSrc="https://raw.githubusercontent.com/CompVis/latent-diffusion/main/data/inpainting_examples/overture-creations-5sI6fQgYIuo_mask.png"
              title="Layer 2"
              isMask={true}
            />
          </div>
        </div>
      </section>

      <ViewWorkflowButton />
    </div>
  );
};
