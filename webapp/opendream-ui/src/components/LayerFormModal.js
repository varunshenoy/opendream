import React from "react";
import { Modal, Input, Button, Form } from "antd";

const convertToBase64 = (e) => {
  const file = e.target.files[0];
  const reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = () => {
    console.log(reader.result);
  };
};

const generateFieldComponent = (field, placeholder) => {
  switch (field.type) {
    case "password":
      return <Input.Password />;
    // TODO: add filepicker
    // case "filepicker":
    //   return <Input type="file" onChange={convertToBase64}/>;
    default:
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
}) => {
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
            rules={[
              {
                required: field.required,
                message:
                  "Please input your " + titleCapitalize(field.label) + "!",
              },
            ]}
          >
            {generateFieldComponent(field, field.placeholder)}
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
