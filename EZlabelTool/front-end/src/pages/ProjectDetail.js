/*
Date: 11 April 2021
Author：Yan Zhou a1807782
Description：front-end for project module
*/

import React from 'react';
import { Layout, message, Button, Modal, Table, Tabs, Typography, Tag, Image, Popover, Card, Input, Row, Col, Select } from 'antd';
import { LeftOutlined, CaretRightOutlined } from '@ant-design/icons';

import HttpUtil from '../Utils/HttpUtil';
import ApiUtil from '../Utils/ApiUtil';

const { Content } = Layout;
const { TabPane } = Tabs;
const { Title } = Typography;
const { Option } = Select;

class ProjectDetail extends React.Component {
  reviewedColumn = [
    {
      title: 'NAME',
      dataIndex: 'filename',
      width: "100px",
    },
    {
      title: 'IMAGE',
      dataIndex: 'url',
      width: "80px",
      render: (text, record) => {
        return (
          <span>
            <Image
              width={80}
              src={record.url}
            />
          </span>
        );
      },
    },
    // {
    //   title: 'TYPE',
    //   dataIndex: 'type',
    //   width: "100px",
    //   render: (status) => {
    //     let color = '';
    //     let tag = '';
    //     if (status === "0") {
    //       color = 'geekblue';
    //       tag = 'SKIPPED';
    //     } else {
    //       color = 'green';
    //       tag = 'SUBMITTED';
    //     }
    //     return (
    //       <Tag color={color} key={tag}>
    //         {tag.toUpperCase()}
    //       </Tag>
    //     );
    //   },
    // },
    {
      title: 'L_LABELLER',
      dataIndex: 'last_labeller',
      width: "100px",
    },
    {
      title: 'LABEL TIME',
      dataIndex: 'label_time',
      width: "100px",
      align: 'center',
      render: (text, record) => {
        if (record.label_time_info.length > 0) {
          return (
            <span>
              <Popover content={
                <Table
                  key={'0'}
                  columns={this.labelTimeColumn}
                  dataSource={record.label_time_info}
                  rowKey={item => item.id}
                  pagination={{ pageSize: 10 }}
                />
              } title="Label Actions" trigger="click">
                <Button type="link">{record.label_time}</Button>
              </Popover>
            </span>
          );
        }
        else {
          return (
            <span>
              {record.label_time}
            </span>
          );
        }
      },
    },
    {
      title: 'COMMENT',
      dataIndex: 'review',
      width: "100px",
      render: (review) => {
        let color = '';
        let tag = '';
        if (review === "1") {
          color = 'volcano';
          tag = 'BAD';
        } else if (review === "2") {
          color = 'default';
          tag = 'UNSURE';
        } else if (review === "3") {
          color = 'green';
          tag = 'GOOD';
        }
        return (
          <Tag color={color} key={tag}>
            {tag.toUpperCase()}
          </Tag>
        );
      },
    },
    {
      title: 'REVIEWER',
      dataIndex: 'last_reviewer',
      width: "100px",
    },
    {
      title: 'UUID',
      dataIndex: 'uuid',
      width: "260px",
    },
    {
      title: 'DATASET',
      dataIndex: 'dataset_name',
      width: "100px",
    },
    {
      title: 'ACTION',
      key: 'operation',
      width: "120px",
      align: 'center',
      render: (text, record) => {
        // admin or owner
        if (this.state.member.role === "0" | this.state.member.role === "3") {
          return (
            <span>
              <Button type="link" style={{ margin: "10px" }} onClick={() => this.handleLabel(this.state.project,record.id)} >label</Button>
              <Button type="link" style={{ margin: "10px" }} onClick={() => this.handleReview(this.state.project,record.id)}>review</Button>
            </span>
          )
        }
        //labeer
        if(this.state.member.role === "1") {
          return <Button type="link" style={{ margin: "10px" }} onClick={() => this.handleLabel(this.state.project,record.id)} >label</Button>
        }
        //reviewer
        if(this.state.member.role === "2") {
          return <Button type="link" style={{ margin: "10px" }} onClick={() => this.handleReview(this.state.project,record.id)}>review</Button>
        }
      },
    },
  ];

  labelledColumn = [
    {
      title: 'NAME',
      dataIndex: 'filename',
      width: "100px",
    },
    {
      title: 'IMAGE',
      dataIndex: 'url',
      width: "100px",
      render: (text, record) => {
        return (
          <span>
            <Image
              width={80}
              src={record.url}
            />
          </span>
        );
      },
    },
    {
      title: 'TYPE',
      dataIndex: 'type',
      width: "100px",
      render: (status) => {
        let color = '';
        let tag = '';
        if (status === "0") {
          color = 'geekblue';
          tag = 'SKIPPED';
        } else {
          color = 'green';
          tag = 'SUBMITTED';
        }
        return (
          <Tag color={color} key={tag}>
            {tag.toUpperCase()}
          </Tag>
        );
      },
    },
    {
      title: 'L_LABELLER',
      dataIndex: 'last_labeller',
      width: "100px",
    },
    {
      title: 'LABEL TIME',
      dataIndex: 'label_time',
      width: "100px",
      align: 'center',
      render: (text, record) => {
        if (record.label_time_info.length > 0) {
          return (
            <span>
              <Popover content={
                <Table
                  key={'1'}
                  columns={this.labelTimeColumn}
                  dataSource={record.label_time_info}
                  rowKey={item => item.id}
                  pagination={{ pageSize: 10 }}
                />
              } title="Labellers" trigger="click">
                <Button type="link">{record.label_time}</Button>
              </Popover>
            </span>
          );
        }
        else {
          return (
            <span>
              {record.label_time}
            </span>
          );
        }
      },
    },
    {
      title: 'UUID',
      dataIndex: 'uuid',
      width: "240px",
    },
    {
      title: 'DATASET',
      dataIndex: 'dataset_name',
      width: "100px",
    },
    {
      title: 'ACTION',
      key: 'operation',
      width: "100px",
      align: 'center',
      render: (text, record) => {
        // admin or owner
        if (this.state.member.role === "0" | this.state.member.role === "3") {
          return (
            <span>
              <Button type="link" style={{ margin: "10px" }} onClick={() => this.handleLabel(this.state.project,record.id)} >label</Button>
              <Button type="link" style={{ margin: "10px" }} onClick={() => this.handleReview(this.state.project,record.id)}>review</Button>
            </span>
          )
        }
        //labeer
        if(this.state.member.role === "1") {
          return <Button type="link" style={{ margin: "10px" }} onClick={() => this.handleLabel(this.state.project,record.id)} >label</Button>
        }
        //reviewer
        if(this.state.member.role === "2") {
          return <Button type="link" style={{ margin: "10px" }} onClick={() => this.handleReview(this.state.project,record.id)}>review</Button>
        }
      },
    },
  ];

  unlabelledColumn = [
    {
      title: 'NAME',
      dataIndex: 'filename',
      width: "100px",
    },
    {
      title: 'IMAGE',
      dataIndex: 'url',
      width: "100px",
      render: (text, record) => {
        return (
          <span>
            <Image
              width={80}
              src={record.url}
            />
          </span>
        );
      },
    },
    {
      title: 'UUID',
      dataIndex: 'uuid',
      width: "240px",
    },
    {
      title: 'DATASET',
      dataIndex: 'dataset_name',
      width: "200px",
    }
  ];

  labelTimeColumn = [
    {
      title: 'EDITOR',
      dataIndex: 'editor',
      width: "100px",
    },
    {
      title: 'EDIT DATE',
      dataIndex: 'edit_date',
      width: "180px",
    },
    {
      title: 'LABEL TIME',
      dataIndex: 'label_time',
      width: "150px",
    }
  ];

  mAllData = [];
  state = {
    reviews: [],
    labells: [],
    queues: [],
    member: {}, // current user
    role: "",
    permission: "",
    project: {},
    projectName: "",
    projectDesc: "",
    totalLabels: "",
    labelledLabels: "",
    reviewedLabels: "",

    commentSel:"",// used for comment selected value storage
  }

  // React life cycle
  componentDidMount() {
    this.getData();
  }

  // get all the data
  getData = () => {
    let parameters = this.props.location.search.split('=');
    let id = parameters[1];
    let json = { "id": id }

    HttpUtil.post(ApiUtil.API_PROJECT_DETAILS, json)
      .then(
        datasetList => {
          this.mAllData = datasetList;
          this.setState({
            reviews: datasetList.reviews,
            labells: datasetList.labells,
            queues: datasetList.queues,
            project: datasetList.project,
            member: datasetList.member,
            role: datasetList.member.role,
            permission: datasetList.member.permission,
            projectName: datasetList.project.name,
            projectDesc: datasetList.project.desc,
            totalLabels: datasetList.project.totalLabels,
            labelledLabels: datasetList.project.labelledLabels,
            reviewedLabels: datasetList.project.reviewedLabels,
          });
        }
      ).catch(error => {
        message.error(error.message);
      });
  }

  // return back to the previous page
  return = () => {
    window.history.back(-1)
  }

  // search select event
  handleChange = (value) =>{
    this.setState({
      commentSel:`${value}`,
    });
  }
  
  // search the labels
  search = () => {
    let parameters = this.props.location.search.split('=');
    let q_id = parameters[1];
    let q_uuid = document.getElementById("q_uuid").value;
    let q_dataset = document.getElementById("q_dataset").value;
    let q_comment = this.state.commentSel;
    if (q_comment === undefined) {
      q_comment = "";
    }
    let q_labeler = document.getElementById("q_labeler").value;
    let q_reviewer = document.getElementById("q_reviewer").value;
    let queryParams= {id:q_id,uuid:q_uuid,dataset:q_dataset,comment:q_comment,labeler:q_labeler,reviewer:q_reviewer};

    HttpUtil.post(ApiUtil.API_PROJECT_DETAILS_SEARCH, queryParams)
      .then(
        datasetList => {
          this.mAllData = datasetList;
          this.setState({
            reviews: datasetList.reviews,
            labells: datasetList.labells,
            queues: datasetList.queues,
            project: datasetList.project,
            member: datasetList.member,
            role: datasetList.member.role,
            permission: datasetList.member.permission,
            projectName: datasetList.project.name,
            projectDesc: datasetList.project.desc,
            totalLabels: datasetList.project.totalLabels,
            labelledLabels: datasetList.project.labelledLabels,
            reviewedLabels: datasetList.project.reviewedLabels,
          });
        }
      ).catch(error => {
        message.error(error.message);
      });

  }

  //delete comfirm information
  deleteConfirm = (project) => {
    var that = this;
    const modal = Modal.confirm({
      title: 'Confirm',
      content: 'Do you want to delete the project?',
      okText: 'Yes',
      cancelText: 'Cancel',
      onOk() {
        that.removeData(project);
        modal.destroy();

      },
      onCancel() { },
    });
  }

  //delete the project
  removeData = (project) => {
    HttpUtil.post(ApiUtil.API_PROJECT_DELETE, project)
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

  // open a new page and get setting data
  getSettingData = (project) => {
    // get request
    this.props.history.push('/setting/?id=' + project.id + '&name=' + project.name);
  }

  handleStartLabel = (project) => {
    // get request
    this.props.history.push('/label/?id=' + project.id);
  }

  handleStartReview = (project) => {
    // get request
    this.props.history.push('/review/?id=' + project.id);
  }

  handleLabel = (project, image_id) => {
    // get request
    this.props.history.push('/labelView/?id=' + project.id + '&name=' + image_id);
  }

  handleReview = (project, image_id) => {
    // get request
    this.props.history.push('/reviewView/?id=' + project.id + '&name=' + image_id);
  }

  handleExport = (project) => {
    let json = { id: project.id };
    HttpUtil.post(ApiUtil.API_EXPORT, json)
      .then(
        re => {
          message.info(re.message);
          let url = re.url;
          const oa = document.createElement('a');
          oa.href = url;
          oa.setAttribute('target', '_blank');
          document.body.appendChild(oa);
          oa.click();
        }
      )
      .catch(error => {
        message.error(error.message);
      });
  }

  render() {
    return (
      <Layout >
        <Content style={{ background: '#fff' }}>
          <div style={{ height: "50px" }}>
            <Button style={{ display: "inline-block", margin: "20px" }} type="primary" ghost icon={<LeftOutlined />} onClick={() => this.return()}>BACK</Button>
            <Title level={4} style={{ display: "inline-block", margin: "20px" }}>{this.state.projectName}</Title>
            {(() => {
              if (this.state.permission.indexOf("2") !== -1) {
                return <Button style={{ display: "inline-block", margin: "10px" }} type="primary" onClick={() => this.handleExport(this.state.project)}>EXPORT</Button>
              }
            })()}
            {(() => {
              if (this.state.permission.indexOf("1") !== -1) {
                return <Button style={{ display: "inline-block", float: "right", margin: "20px" }} type="primary" onClick={() => this.getSettingData(this.state.project)}>SETUP</Button>
              }
            })()}
            {(() => {
              if (this.state.permission.indexOf("0") !== -1) {
                return <Button style={{ display: "inline-block", float: "right", marginTop: "20px", marginRight: "0px" }} type="" onClick={() => this.deleteConfirm((this.state.project))}>DELETE</Button>
              }
            })()}
          </div>
          <div style={{ display: "flex", justifyContent: "space-between", width: "100%" }}>
            <Card style={{ margin: "20px", width: "80%" }}>
              <Input.Group>
                <Row gutter={8}>
                  <Col span={8}>
                    <Input id="q_uuid" placeholder="UUID" allowClear/>
                  </Col>
                  <Col span={8}>
                    <Input id="q_dataset" placeholder="Dataset" allowClear/>
                  </Col>
                  <Col span={8}>
                    <Select id="q_comment" placeholder="Comment" style={{ width: 240 }} onChange={this.handleChange} allowClear>
                      <Option key="1" value="1">BAD</Option>
                      <Option key="2" value="2">UNSURE</Option>
                      <Option key="3" value="3">GOOD</Option>
                    </Select>
                  </Col>
                </Row>
                <br />
                <Row gutter={8}>                 
                  <Col span={8}>
                    <Input id="q_labeler" placeholder="Last Labeler" allowClear/>
                  </Col>
                  <Col span={8}>
                    <Input id="q_reviewer" placeholder="Last Reviewer" allowClear/>
                  </Col>
                  <Col span={8}>
                    <Button type="primary" onClick={() => this.search()}>SEARCH</Button>
                  </Col>
                </Row>
              </Input.Group>

            </Card>
            <Card style={{ margin: "20px", width: "40%" }}>
              <Title level={5} style={{ display: "inline-block" }}>Have labelled: {this.state.labelledLabels}/{this.state.totalLabels}</Title>
              {(() => {
                if (this.state.member.role === "0" | this.state.member.role === "1" | this.state.member.role === "3") {
                  return <Button type="primary" style={{ margin: "10px" }} ghost icon={<CaretRightOutlined />} onClick={() => this.handleStartLabel(this.state.project)}>Start Labelling</Button>
                } else {
                  return <Button type="primary" style={{ margin: "10px" }} ghost icon={<CaretRightOutlined />} disabled>Start Labelling</Button>
                }
              })()}
              <br/>
              <Title level={5} style={{ display: "inline-block" }}>Have reviewed: {this.state.reviewedLabels}/{this.state.labelledLabels}</Title>
              {(() => {
                if (this.state.member.role === "0" | this.state.member.role === "2" | this.state.member.role === "3") {
                  return <Button type="primary" style={{ margin: "10px" }} ghost icon={<CaretRightOutlined />} onClick={() => this.handleStartReview(this.state.project)}>Start Reviewing</Button>
                } else {
                  return <Button type="primary" style={{ margin: "10px" }} ghost icon={<CaretRightOutlined />} disabled>Start Reviewing</Button>
                }
              })()}
            </Card>
          </div>
          <div style={{ background: '#fff', paddingLeft: 24, paddingRight: 24, minHeight: 480, marginTop: "0px" }}>
            <Tabs defaultActiveKey="1" >
              <TabPane tab="REVIEWED" key="1">
                <Table
                  columns={this.reviewedColumn}
                  dataSource={this.state.reviews}
                  rowKey={item => item.id}
                  pagination={{ pageSize: 10 }}
                  scroll={{ y: 340 }} />
              </TabPane>
              <TabPane tab="LABELLED" key="2">
                <Table
                  columns={this.labelledColumn}
                  dataSource={this.state.labells}
                  rowKey={item => item.id}
                  pagination={{ pageSize: 10 }}
                  scroll={{ y: 340 }} />
              </TabPane>
              <TabPane tab="QUEUE" key="3">
                <Table
                  columns={this.unlabelledColumn}
                  dataSource={this.state.queues}
                  rowKey={item => item.id}
                  pagination={{ pageSize: 10 }}
                  scroll={{ y: 340 }} />
              </TabPane>
            </Tabs>
          </div>
        </Content>
      </Layout>
    )
  }
}
export default ProjectDetail;