/*
Date: 11 April 2021
Author：Yan Zhou a1807782
Description：front-end for project module
*/

import React from 'react';
import { Layout, message, Button, Table, Tag, Tabs, Typography } from 'antd';
import { LeftOutlined } from '@ant-design/icons';

import HttpUtil from '../Utils/HttpUtil';
import ApiUtil from '../Utils/ApiUtil';
import ProjectSettingRole from './ProjectSettingRole';
import ProjectSettingPermission from './ProjectSettingPermission';
import ProjectSettingEditor from './ProjectSettingEditor';

const { Content } = Layout;
const { TabPane } = Tabs;
const { Title } = Typography;

class Setting extends React.Component {

  // colunms for member table
  memberColumns = [
    {
      title: 'MEMBER',
      dataIndex: 'name',
      width: "160px",
      align: 'center',
    },
    {
      title: 'PROJECT ROLE',
      dataIndex: 'role',
      width: "160px",
      key: 'role',
      align: 'center',
      // return the tag style of different roles
      render: (role) => {
        let color = '';
        let tag = '';
        if (role === "0") {
          color = 'volcano';
          tag = 'ADMIN';
        } else if (role === "1") {
          color = 'geekblue';
          tag = 'LABELLER';
        } else if (role === "2") {
          color = 'blue';
          tag = 'REVIEWER';
        } else if (role === "3") {
          color = 'green';
          tag = 'OWNER';
        } else {
          color = 'default';
          tag = 'NO ROLE';
        }
        return (
          <Tag color={color} key={tag}>
            {tag.toUpperCase()}
          </Tag>
        );
      },
    },
    {
      title: 'PROJECT PERMISSION',
      dataIndex: 'permission',
      width: "300px",
      align: 'center',
      render: (permission) => {
        let permissions = permission.split(',')
        if (permissions.length !== 1) {
          permissions.pop();
          let text = ['DELETE', 'SETUP', 'EXPORT']
          return (
            permissions.map((el, index) => {
              return (
                <Tag color={"blue"} key={el}>
                  {text[el]}
                </Tag>
              )
            })
          )
        }
      }
    },
    {
      title: 'OPERATION',
      key: 'action',
      align: 'center',
      render: (text, record) => {
        if (record.role === '0' | record.role === '3' | this.state.setup === -1) {
          return (
            <span>
              <Button type="link" disabled >change role</Button>
              <Button type="link" disabled >change permission</Button>
            </span>
          );
        } else {
          return (
            <span>
              <Button type="link" onClick={() => this.showRoleDialog(record)}>change role</Button>
              <Button type="link" onClick={() => this.showPermissionDialog(record)}>change permission</Button>
            </span>
          );
        }
      },
    },
  ];

  // colunms for dataset table
  datasetColumns = [
    {
      title: 'DATASET',
      dataIndex: 'name',
      width: "160px",
      align: 'center',
    },
    {
      title: 'CREATOR',
      dataIndex: 'creator',
      width: "160px",
      align: 'center',
    },
    {
      title: 'ROWS',
      dataIndex: 'rows',
      width: "160px",
      align: 'center',
    },
    {
      title: 'CREATE DATE',
      dataIndex: 'create_date',
      width: "160px",
      align: 'center',
    },
    {
      title: 'ATTACHED',
      dataIndex: 'isAttached',
      width: "160px",
      align: 'center',
      render: (isAttached) => {
        let color = '';
        let tag = '';
        if (isAttached === "1") {
          color = 'green';
          tag = 'YES';
        } else {
          color = 'default';
          tag = 'NO';
        }
        return (
          <Tag color={color} key={tag}>
            {tag.toUpperCase()}
          </Tag>
        );
      },
    },
    {
      title: 'OPERATION',
      key: 'action',
      align: 'center',
      render: (text, record) => {
        if (record.isAttached === "0") {
          if(this.state.setup !== -1){
            return (
              <Button type="link" onClick={() => this.attachOrDettach(record)}>attach</Button>
            );
          }else{
            return (
              <Button type="link" disabled>attach</Button>
            );
          }
        } else {
          if(this.state.setup !== -1){
            return (
              <Button type="link" onClick={() => this.attachOrDettach(record)}>detach</Button>
            );
          }else{
            return (
              <Button type="link" disabled>detach</Button>
            );
          }
        }
      },
    },
  ];

  editorColumns = [
    {
      title: 'Editor id',
      dataIndex: 'id',
      width: "160px",
    },
    {
      title: 'Name',
      dataIndex: 'name',
      width: "160px",
    },
    {
      title: 'Description',
      dataIndex: 'desc',
      width: "160px",
    },
  ];

  mAllData = [];
  state = {
    members: [],
    datasets: [],
    editor: {},
    role: "",
    permission: "",
    setup:-1,
    projectId: "",
    projectName: "",
    roleSetting: false,
    permissionSetting: false,
    editingItem: null,
  }

  // React life cycle
  componentDidMount() {
    this.getData();
  }

  // attach or dettach the dataset
  attachOrDettach = (record) => {
    HttpUtil.post(ApiUtil.API_PROJECT_JOIN_DATASET, record)
      .then(
        re => {
          message.info(re.message);
          this.getData();
          this.setState({
            key: '2',
          });
        }
      )
      .catch(error => {
        message.error(error.message);
      });
  }

  // show the role or permission change dialog
  showRoleDialog(record) {
    this.setState({
      roleSetting: true,
      editingItem: record,
    });
  }

  showPermissionDialog(record) {
    this.setState({
      permissionSetting: true,
      editingItem: record,
    });
  }

  // get all the data
  getData = () => {
    let parameters = this.props.location.search.split('=');
    let str = parameters[1];
    let id = str.substring(0, str.indexOf("&"));
    let json = { "id": id }

    HttpUtil.post(ApiUtil.API_PROJECT_SETTING, json)
      .then(
        datasetList => {
          this.mAllData = datasetList;
          this.setState({
            members: datasetList.members,
            datasets: datasetList.datasets,
            editor: datasetList.editor,
            role: datasetList.member.role,
            permission: datasetList.member.permission,
            setup:datasetList.member.permission.indexOf("1"),
            projectId: id,
            projectName: parameters[2].replace("%20", ' '),
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

  render() {
    return (
      <Layout>
        <Content style={{ background: '#fff' }}>
          <div style={{ height: "50px" }}>
            <Button style={{ display: "inline-block", margin: "20px" }} type="primary" ghost icon={<LeftOutlined />} onClick={() => this.return()}>BACK</Button>
            <Title level={4} style={{ display: "inline-block", margin: "20px" }}>{this.state.projectName}</Title>
          </div>
          <div style={{ background: '#fff', padding: 24, minHeight: 480 }}>

            <Tabs defaultActiveKey="1">
              <TabPane tab="MEMBERS" key="1">
                <p style={{ color: '#1890FF' }}>You can assign members to this project, and confirm their roles and permissions.</p>
                <Table
                  columns={this.memberColumns}
                  dataSource={this.state.members}
                  rowKey={item => item.id}
                  pagination={{ pageSize: 10 }}
                  scroll={{ y: 340 }} />
                <ProjectSettingRole
                  visible={this.state.roleSetting}
                  member={this.state.editingItem}
                  afterClose={() => {
                    this.setState({ roleSetting: false });
                    this.getData();
                  }}
                />
                <ProjectSettingPermission
                  visible={this.state.permissionSetting}
                  member={this.state.editingItem}
                  afterClose={() => {
                    this.setState({ permissionSetting: false });
                    this.getData();
                  }}
                />
              </TabPane>
              <TabPane tab="DATASETS" key="2">
              <p style={{color:'#1890FF'}}>You can attach multiple datasets, then labelers can lebel the images in the attached datasets.</p>
                <Table
                  columns={this.datasetColumns}
                  dataSource={this.state.datasets}
                  rowKey={item => item.id}
                  pagination={{ pageSize: 10 }}
                  scroll={{ y: 340 }} />
              </TabPane>
              <TabPane tab="EDITOR" key="3">
                <ProjectSettingEditor
                  editor={this.state.editor}
                  projectId={this.state.projectId}
                  setup={this.state.setup}
                />
              </TabPane>
            </Tabs>
          </div>
        </Content>
      </Layout>
    )
  }
}
export default Setting;