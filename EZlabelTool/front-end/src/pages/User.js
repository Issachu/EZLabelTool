/*
Date: 10 April 2021
Author：Yan Zhou a1807782
Description：front-end for user module
*/


import React from 'react';
import { Layout, Table, Modal, Button, message, Input, Popover } from 'antd';

import HttpUtil from '../Utils/HttpUtil';
import ApiUtil from '../Utils/ApiUtil';

const { Content } = Layout;
const { Search } = Input;

class User extends React.Component {
    columns = [
        {
            title: 'NO.',
            width: "60px",
            render: (text, record, index) => `${this.state.current - 1}` * `${this.state.pageSize}` + index + 1,
        },
        {
            title: 'USER',
            dataIndex: 'name',
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
            title: 'PROJECTS',
            dataIndex: 'project',
            width: "160px",
            align: 'center',
            render: (text, record) => {
                if (record.project !== 0) {
                    return (
                        <span>
                            <Popover content={record.detail} title="Projects in charge" trigger="hover">
                                <Button type="link">{record.project}</Button>
                            </Popover>
                        </span>
                    );
                }else{
                    return (
                        <span>
                            {record.project}
                        </span>
                    );
                }
            },
        },
        {
            title: 'OPERARIONS',
            key: 'action',
            align: 'center',
            render: (text, record) => {
                if (sessionStorage.getItem("role")==='0')
                    if (record.name === sessionStorage.getItem("user_name")) {
                        return (
                            <span>
                                <Button type="link" style={{ marginLeft: 12 }} disabled>remove from organization</Button>
                                <Button type="link" style={{ marginLeft: 12 }} disabled>reset password</Button>
                            </span>
                        );
                    }else{
                        return (
                            <span>
                                <Button type="link" style={{ marginLeft: 12 }} onClick={() => this.deleteConfirm(record)}>remove from organization</Button>
                                <Button type="link" style={{ marginLeft: 12 }} onClick={() => this.resetPasswordConfirm(record)}>reset password</Button>
                            </span>
                        );
                    } 
                else{
                    return (
                        <span>
                            <Button type="link" style={{ marginLeft: 12 }} disabled>remove from organization</Button>
                            <Button type="link" style={{ marginLeft: 12 }} disabled>reset password</Button>
                        </span>
                    );
                }
            },
        },
    ];

    mAllData = [];
    state = {
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
        HttpUtil.post(ApiUtil.API_USER_LIST)
            .then(
                userList => {
                    this.mAllData = userList;
                    this.setState({
                        mData: userList,
                    });
                }
            ).catch(error => {
                message.error(error.message);
            });
    }

    // search function
    onSearch = value => {
        let query = {
            "name": value
        }

        HttpUtil.post(ApiUtil.API_USER_SEARCH, query)
            .then(
                userSearchList => {
                    this.mAllData = userSearchList;
                    this.setState({
                        mData: userSearchList,
                    });
                }
            ).catch(error => {
                message.error(error.message);
            });

    }

    //delete comfirm information
    deleteConfirm = (user) => {
        var that = this;
        const modal = Modal.confirm({
            title: 'Confirm',
            content: 'Do you want to delete the user?',
            okText: 'Yes',
            cancelText: 'Cancel',
            onOk() {
                that.removeData(user);
                modal.destroy();
            },
            onCancel() { },
        });
    }

    //delete the user
    removeData = (user) => {
        HttpUtil.post(ApiUtil.API_USER_DELETE, user)
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

    //reset password comfirm information
    resetPasswordConfirm = (user) => {
        var that = this;
        const modal = Modal.confirm({
            title: 'Confirm',
            content: 'Do you want to reset the password to 666666',
            okText: 'Yes',
            cancelText: 'Cancel',
            onOk() {
                that.resertPassword(user);
                modal.destroy();
            },
            onCancel() { },
        });
    }

    //reset the password
    resertPassword = (user) => {
        HttpUtil.post(ApiUtil.API_USER_RESET, user)
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

    render() {
        return (
            <Layout>
                <Content >
                    <div class="box" style={{ lineHeight: '64px', display: "flex", alignItems: "center" }}>
                        <Button style={{ display: "inline-block", margin: "10px" }} type="primary" disabled>ADD MEMBER</Button>
                        <Search style={{ width: 400, display: "inline-block", position: "absolute", right: "20px", verticalAlign: "middle" }} allowClear placeholder="search the name of user" onSearch={this.onSearch} enterButton />
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
                    </div>
                </Content>
            </Layout>
        )
    }
}
export default User;
