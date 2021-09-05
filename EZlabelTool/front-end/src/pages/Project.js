/*
Date: 11 April 2021
Author：Yan Zhou a1807782
Description：front-end for project module
*/

import React from 'react';
import { Layout, Table, Button, Modal, message, Input, Tag } from 'antd';

import ProjectInfoDialog from './ProjectInfoDialog'

import HttpUtil from '../Utils/HttpUtil';
import ApiUtil from '../Utils/ApiUtil';

const { Content } = Layout;
const { Search } = Input;

class Project extends React.Component {
    columns = [
        {
            title: 'NO.',
            width: "60px",
            render: (text, record, index) => `${this.state.current - 1}` * `${this.state.pageSize}` + index + 1,

        },
        {
            title: 'PROJECT',
            dataIndex: 'name',
            width: "160px",
            align: 'center',
            render: (text, record) => {
                if (record.status === '0') {
                    return (
                        <span>
                            <Button type="link" onClick={() => this.getSettingData(record)}>{record.name}</Button>
                        </span>
                    );
                } else {
                    return (
                        <span>
                            <Button type="link" onClick={() => this.getDetailData(record)}>{record.name}</Button>
                        </span>
                    );
                }
            },
        },
        {
            title: 'STATUS',
            dataIndex: 'status',
            width: "120px",
            align: 'center',
            render: (status) => {
                let color = '';
                let tag = '';
                if (status === "0") {
                    color = 'default';
                    tag = 'SETTING';
                } else if (status === "1") {
                    color = 'blue';
                    tag = 'PROCESSING';
                } else if (status === "2") {
                    color = 'volcano';
                    tag = 'COMPLETED';
                } else {
                    color = 'default';
                    tag = 'UNKNOWN';
                }
                return (
                    <Tag color={color} key={tag}>
                        {tag.toUpperCase()}
                    </Tag>
                );
            },
        },
        {
            title: 'CREATOR',
            dataIndex: 'creator',
            width: "160px",
            align: 'center',
        },
        {
            title: 'LABELLS',
            dataIndex: 'labells',
            width: "160px",
            align: 'center',
        },
        {
            title: 'CREATE DATE',
            dataIndex: 'create_date',
            width: "160px",
            align: 'center',
        },
    ];

    mAllData = [];

    state = {
        addProjectDialog: false,
        editingItem: null,
        mData: [], // data in table
        current: 1, // current page
        pageSize: 10,
    }

    // React life cycle
    componentDidMount() {
        // initialize the data
        this.getData();
    }

    // get all the data
    getData = () => {
        HttpUtil.post(ApiUtil.API_PROJECT_LIST)
            .then(
                projectList => {
                    this.mAllData = projectList;
                    this.setState({
                        mData: projectList,
                    });
                }
            ).catch(error => {
                message.error(error.message);
            });
    }

    // show the modal for add a new project
    showAddDialog() {
        this.setState({
            addProjectDialog: true,
        });
    }

    // search function
    onSearch = value => {
        let query = {
            "name": value
        }

        HttpUtil.post(ApiUtil.API_PROJECT_SEARCH, query)
            .then(
                projectSearchList => {
                    this.mAllData = projectSearchList;
                    this.setState({
                        mData: projectSearchList,
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
                    this.getData();
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

    // open a new page and get detail data
    getDetailData = (project) => {
        // post, cannot resolve the refresh problem
        // this.props.history.push({
        //     pathname: '/detail',
        //     state: {project: project},
        // });

        this.props.history.push('/detail/?id=' + project.id);

    }

    render() {
        return (
            <Layout>
                <Content>
                    <div className="box" style={{ lineHeight: '64px', display: "flex", alignItems: "center" }}>
                        <Button style={{ display: "inline-block", margin: "10px" }} type="primary" onClick={() => this.showAddDialog()}>ADD PROJECT</Button>
                        <Search style={{ width: 400, display: "inline-block", position: "absolute", right: "20px", verticalAlign: "middle" }} allowClear placeholder="search the name of project" onSearch={this.onSearch} enterButton />
                    </div>
                    <div style={{ background: '#fff', padding: 24, minHeight: 480, width: "96%" }}>
                        <Table
                            columns={this.columns}
                            dataSource={this.state.mData}
                            rowKey={item => item.id}
                            pagination={{
                                pageSize: this.state.pageSize,
                                current: this.state.current,
                                onChange: (page) => {
                                    this.setState({
                                        current: page,
                                    });
                                }
                            }}
                            scroll={{ y: 340 }} />
                        <ProjectInfoDialog
                            visible={this.state.addProjectDialog}
                            project={this.state.editingItem}
                            getSettingData={this.getSettingData}
                            afterClose={() => {
                                this.setState({ addProjectDialog: false });
                                this.getData();
                            }}
                        />
                    </div>
                </Content>
            </Layout>
        )
    }
}

export default Project;
