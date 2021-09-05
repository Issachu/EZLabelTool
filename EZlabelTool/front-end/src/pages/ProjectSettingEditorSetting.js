/*
Date: 24 April 2021
Author：Pingyi Hu a1805597
Description：front-end for editor setting in project module
*/


import React, { useEffect } from "react";
import "antd/dist/antd.css";
import HttpUtil from "../Utils/HttpUtil";
import ApiUtil from "../Utils/ApiUtil";

import { Layout, Button, Select, Input, Form, Space, message, Divider } from "antd";
import { MinusCircleOutlined, PlusOutlined } from "@ant-design/icons";

const { Option } = Select;

const { Content } = Layout;

const objectType = [
  { label: "Bounding Box", value: "Bounding Box" },
  { label: "Polygon", value: "Polygon" },
];

const classType = [
  { label: "Radio", value: "Radio" },
  { label: "Multiple Choice", value: "Multiple Choice" },
];

let edit_id = "";

function ProjectSettingEditorSetting(props) {
  const [form] = Form.useForm();

  useEffect(() => {
    getData();
  }, []);

  // edit the objects and classifications of editor
  const addSetting = (values) => {
    if (values.objects === undefined) {
      values.objects = []
    }
    if (values.classifications === undefined) {
      values.classifications = []
    }

    let duplicate = false;
    for (var i = 0; i < values.objects.length; i++) {
      for (var j = i+1; j < values.objects.length; j++){
        console.log(values.objects[i]);
        console.log(values.objects[j]);
        if (values.objects[i].name === values.objects[j].name){
          duplicate = true;
          message.info("Duplicate object names!");
        }
      }
    }
    for (var m = 0; m < values.classifications.length; m++) {
      console.log(values.classifications[m]);
      for (var n = m+1; n < values.classifications.length; n++){
        if (values.classifications[m].name === values.classifications[n].name){
          duplicate = true;
          message.info("Duplicate classifications names!");
        }
      }
      console.log(values.classifications[m].classes.length);
      for (var k = 0; k < values.classifications[m].classes.length; k++){
        console.log(values.classifications[m].classes[k]);
        for (var l = k+1; l < values.classifications[m].classes.length; l++){
          if (values.classifications[m].classes[k] === values.classifications[m].classes[l]){
            duplicate = true;
          message.info("Duplicate classifications option names!");
          }
        }
      }
    }
    if (!duplicate){
      let request = {
        id: edit_id,
        objects: values.objects,
        classifications: values.classifications,
      }
  
      HttpUtil.post(ApiUtil.API_EDITOR_COPY_SETTING_EDIT, request)
        .then(
          re => {
            message.info(re.message);
            window.history.back(-1);
          }
        )
        .catch(error => {
          message.error(error.message);
        });
    }
  };

  const getData = () => {
    let json = { id: props.editor_copy_id };
    edit_id = props.editor_copy_id;

    HttpUtil.post(ApiUtil.API_EDITOR_COPY_SETTING, json)
      .then((datasetList) => {
        console.log(datasetList);
        datasetList.classifications.forEach((v, i) => {
          console.log(datasetList.classifications[i].classes)
          const classesArray = datasetList.classifications[i].classes.split(',');
          datasetList.classifications[i].classes = [].concat(classesArray);
        });
        form.setFieldsValue({
          objects: datasetList.objects,
          classifications: datasetList.classifications,
        });
      })
      .catch((error) => {
        message.error(error.message);
      });
  };

  return (
    <Layout>
      <Content>
        <div style={{ background: '#fff', padding: 24, minHeight: 480 ,width:'40%'}}>
          <Form
            form={form}
            name="dynamic_form_nest_item"
            onFinish={addSetting}
            autoComplete="off"
          >
            <Divider orientation="left">Objects</Divider>
            <Form.List name="objects">
              {(fields, { add, remove }) => {
                return (
                  <div>
                    {fields.map((field) => (
                      <Space
                        key={field.key}
                        style={{ display: "flex", marginBottom: 8 }}
                        align="start"
                      >
                        <Form.Item
                          {...field}
                          name={[field.name, "name"]}
                          fieldKey={[field.fieldKey, "name"]}
                          rules={[
                            { required: true, message: "Missing name" },
                          ]}
                        >
                          <Input placeholder="Name" />
                        </Form.Item>

                        <Form.Item noStyle shouldUpdate>
                          {() => (
                            <Form.Item
                              {...field}
                              label=""
                              name={[field.name, "shape"]}
                              fieldKey={[field.fieldKey, "shape"]}
                              rules={[
                                { required: true, message: "Missing shape" },
                              ]}
                            >
                              <Select
                                options={objectType}
                                style={{ width: 150 }}
                                placeholder="Shape"
                              ></Select>
                            </Form.Item>
                          )}
                        </Form.Item>

                        <Form.Item noStyle shouldUpdate>
                          {() => (
                            <Form.Item
                              {...field}
                              label=""
                              name={[field.name, "color"]}
                              fieldKey={[field.fieldKey, "color"]}
                              rules={[
                                { required: true, message: "Missing color" },
                              ]}
                            >
                              <Select
                                style={{ width: 100 }}
                                placeholder={'Color'}
                              >
                                <Option value="green" label="green">
                                  <div style={{ background: "#52BE80", color: "white" }}>
                                    Green
                                  </div>
                                </Option>
                                <Option value="red" label="red">
                                  <div style={{ background: "#CD5C5C", color: "white" }}>
                                    Red
                                  </div>
                                </Option>
                                <Option value="blue" label="blue">
                                  <div style={{ background: "#3498DB", color: "white" }}>
                                    Blue
                                  </div>
                                </Option>
                                <Option value="grey" label="grey">
                                  <div style={{ background: "#95A5A6", color: "white" }}>
                                    Grey
                                  </div>
                                </Option>
                                <Option value="pink" label="pink">
                                  <div style={{ background: "#FFB6C1", color: "white" }}>
                                    Pink
                                  </div>
                                </Option>
                                <Option value="yellow" label="yellow">
                                  <div style={{ background: "#F7DC6F", color: "white" }}>
                                    Yellow
                                  </div>
                                </Option>
                                <Option value="purple" label="purple">
                                  <div style={{ background: "	#9370DB", color: "white" }}>
                                    Purple
                                  </div>
                                </Option>
                              </Select>
                            </Form.Item>
                          )}
                        </Form.Item>
                        <MinusCircleOutlined className="dynamic-delete-button" onClick={() => {remove(field.name);}}/>
                      </Space>
                    ))}

                    <Form.Item>
                      <Button
                        style={{ width: '100%', marginTop: '20px'}}
                        type="primary" ghost
                        onClick={() => {
                          add();
                        }}
                        block
                      >
                        <PlusOutlined /> Object
                      </Button>
                    </Form.Item>
                  </div>
                );
              }}
            </Form.List>

            <Divider orientation="left">Classifications</Divider>

            <Form.List name="classifications" key="classifications">
              {(fields, { add, remove }) => {
                return (
                  <div>
                    {fields.map((field) => (
                      <div key={'${field.name}_${field.key}'+field.key}>
                        <Space
                          key={field.key}
                          style={{ display: "flex", marginBottom: 8 }}
                          align="start"
                        >
                          <Form.Item
                            {...field}
                            name={[field.name, "name"]}
                            fieldKey={[field.fieldKey, "c_name"]}
                            rules={[
                              { required: true, message: "Missing name" },
                            ]}
                          >
                            <Input placeholder="Name" style={{ width: 150 }}/>
                          </Form.Item>

                          <Form.Item noStyle shouldUpdate>
                            {() => (
                              <Form.Item
                                {...field}
                                label=""
                                name={[field.name, "type"]}
                                fieldKey={[field.fieldKey, "type"]}
                                placeholder="Type"
                                rules={[
                                  { required: true, message: "Missing type" },
                                ]}
                              >
                                <Select
                                  options={classType}
                                  key={"type"}
                                  style={{ width: 155 }}
                                  placeholder={'Type'}
                                ></Select>
                              </Form.Item>
                            )}
                          </Form.Item>

                          <MinusCircleOutlined
                            onClick={() => {
                              remove(field.name);
                            }}
                          />

                        </Space>

                        <Form.List
                          fieldKey={[field.fieldKey, "classes"]}
                          name={[field.name, "classes"]}
                        >
                          {(options, { add, remove }) => {
                            return (
                              <div>
                                {options.map((option) => (
                                  <Space key={option.key} align="start">
                                    <Form.Item
                                      {...option}
                                      label=""
                                      fieldKey={[option.fieldKey, "option"]}
                                      rules={[
                                        {
                                          required: true,
                                          message: "Missing option",
                                        },
                                      ]}
                                    >
                                      <Input placeholder="Option" style={{ width: 415 }}/>
                                    </Form.Item>

                                    <MinusCircleOutlined
                                      onClick={() => {
                                        remove(option.name);
                                      }}
                                    />
                                  </Space>
                                ))}

                                <Form.Item>
                                  <Button
                                    type="dashed"
                                    style={{ width: '30%', marginTop: '20px' }}
                                    onClick={() => {
                                      add();
                                    }}
                                    block
                                  >
                                    <PlusOutlined /> Option
                                      </Button>
                                </Form.Item>
                              </div>
                            );
                          }}
                        </Form.List>
                      </div>
                    ))}

                    <Form.Item>
                      <Button
                        type="primary" ghost
                        style={{ width: '100%', marginTop: '20px' }}
                        onClick={() => {
                          add();
                        }}
                        block
                      >
                        <PlusOutlined /> Classification
                        </Button>
                    </Form.Item>
                  </div>
                );
              }}
            </Form.List>
            <Form.Item>
              <Button type="primary" htmlType="submit" style={{ width: '100%', marginTop: '20px' }}>
                Submit
                </Button>
            </Form.Item>
          </Form>
        </div>
      </Content>
    </Layout>
  );
};

export default ProjectSettingEditorSetting;
