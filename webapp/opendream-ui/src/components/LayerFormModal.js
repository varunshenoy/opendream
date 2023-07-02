import React from "react";
import { Modal, Input, Button, Form, Select, Space } from "antd";
import TextArea from "antd/es/input/TextArea";

const convertToBase64 = (e) => {
  const file = e.target.files[0];
  const reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = () => {
    console.log(reader.result);
  };
};

const generateFieldComponent = (
  field,
  placeholder,
  allLayers,
  maskLayers,
  imageLayers
) => {
  switch (field.type) {
    case "MaskLayer":
      return (
        <Select placeholder="Select a layer" optionLabelProp="label">
          {maskLayers.map((l) => (
            <Select.Option
              value={l.id}
              label={l.id}
              class="flex flex-row justify-center items-center"
            >
              <Space>
                <span role="img" aria-label={l.id}>
                  <img src={l.image} style={{ width: 80 }} />
                </span>
                Layer {l.id}
              </Space>
            </Select.Option>
          ))}
        </Select>
      );
    case "ImageLayer":
      return (
        <Select placeholder="Select a layer" optionLabelProp="label">
          {imageLayers.map((l) => (
            <Select.Option
              value={l.id}
              label={l.id}
              class="flex flex-row justify-center items-center"
            >
              <Space>
                <span role="img" aria-label={l.id}>
                  <img src={l.image} style={{ width: 80 }} />
                </span>
                Layer {l.id}
              </Space>
            </Select.Option>
          ))}
        </Select>
      );
    case "Layer":
      return (
        <Select placeholder="Select a layer" optionLabelProp="label">
          {allLayers.map((l) => (
            <Select.Option
              value={l.id}
              label={l.id}
              class="flex flex-row justify-center items-center"
            >
              <Space>
                <span role="img" aria-label={l.id}>
                  <img src={l.image} style={{ height: 80, width: 80 }} />
                </span>
                Layer {l.id}
              </Space>
            </Select.Option>
          ))}
        </Select>
      );
    // TODO: add filepicker
    // case "filepicker":
    //   return <Input type="file" onChange={convertToBase64}/>;
    default:
      if (field.label.includes("prompt")) {
        return (
          <TextArea
            placeholder={placeholder}
            autoSize={{ minRows: 3, maxRows: 6 }}
          />
        );
      }
      return <Input placeholder={placeholder} />;
  }
};

const LayerFormModal = ({
  title,
  open,
  handleOk,
  handleCancel,
  onFinish,
  onFinishFailed,
  fields,
  loading,
  currentState,
}) => {
  const maskLayers = currentState.filter(
    (layer) =>
      layer["metadata"]["op"] === "mask" || layer["metadata"]["op"] === "sam"
  );
  const imageLayers = currentState.filter(
    (layer) =>
      layer["metadata"]["op"] !== "mask" && layer["metadata"]["op"] !== "sam"
  );

  function titleCapitalize(str) {
    return str
      .split("_") // Split the string at underscores
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()) // Capitalize the first character of each word and make the rest lowercase
      .join(" "); // Join the words back together with space
  }
  return (
    <Modal
      title={title}
      open={open}
      onOk={handleOk}
      onCancel={handleCancel}
      maskClosable={false}
      footer={[]}
    >
      <Form
        name="basic"
        labelCol={{
          span: 8,
        }}
        wrapperCol={{
          span: 16,
        }}
        style={{
          maxWidth: 600,
        }}
        initialValues={{
          remember: true,
        }}
        onFinish={onFinish}
        onFinishFailed={onFinishFailed}
        autoComplete="off"
      >
        {fields.map((field, index) => (
          <Form.Item
            key={index}
            label={titleCapitalize(field.label)}
            name={field.label}
            required={field.placeholder === ""}
            rules={[
              {
                required: field.placeholder === "",
                message:
                  "Please input your " + titleCapitalize(field.label) + "!",
              },
            ]}
          >
            {generateFieldComponent(
              field,
              field.placeholder,
              currentState,
              maskLayers,
              imageLayers
            )}
          </Form.Item>
        ))}

        <Form.Item
          wrapperCol={{
            offset: 19,
            span: 16,
          }}
        >
          <Button
            type="primary"
            htmlType="submit"
            onClick={handleOk}
            loading={loading}
            className="bg-blue-800"
          >
            Submit
          </Button>
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default LayerFormModal;
