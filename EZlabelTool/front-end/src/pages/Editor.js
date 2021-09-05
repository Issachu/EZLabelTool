/*
Date: 14 April 2021
Author：Jingyi Cui
Description：front-end for editor module
*/
import React from 'react';
import { Layout, Table, Button, Modal, message } from 'antd';
import EditorInfoDialog from './EditorInfoDialog'

import HttpUtil from '../Utils/HttpUtil';
import ApiUtil from '../Utils/ApiUtil';

const { Content } = Layout;

class Editor extends React.Component {
    columns = [
        {
            title: 'NO.',
            width: "60px",
            render: (text, record, index) => `${this.state.current - 1}` * `${this.state.pageSize}` + index + 1,
        },
        {
            title: 'EDITOR',
            dataIndex: 'name',
            width: "200px",
            align: 'center',
        },
        {
            title: 'DESCRIPTION',
            dataIndex: 'desc',
            width: "400px",
        },
        {
            title: 'PROJECTS',
            dataIndex: 'project',
            width: "160px",
            align: 'center',
        },
        {
            title: 'OPERATIONS',
            key: 'action',
            align: 'center',
            render: (text, record) => {
                return (
                    <span>
                        <Button type="link" onClick={() => this.getSettingData(record)}>setup</Button>
                    </span>
                );
            },
        }
    ];
    mAllData = [];
    state = {
        addEditorDialog: false,
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
        HttpUtil.post(ApiUtil.API_EDITOR_LIST)
            .then(
                editorList => {
                    this.mAllData = editorList;
                    this.setState({
                        mData: editorList,
                    });
                }
            ).catch(error => {
                message.error(error.message);
            });
    }

    // show the modal for add a new editor
    showAddDialog() {
        this.setState({
            addEditorDialog: true,
        });
    }

    // search function
    onSearch = value => {
        let query = {
            "name": value
        }

        HttpUtil.post(ApiUtil.API_EDITOR_SEARCH, query)
            .then(
                editorSearchList => {
                    this.mAllData = editorSearchList;
                    this.setState({
                        mData: editorSearchList,
                    });
                }
            ).catch(error => {
                message.error(error.message);
            });

    }

    //delete comfirm information
    deleteConfirm = (editor) => {
        var that = this;
        const modal = Modal.confirm({
            title: 'Confirm',
            content: 'Do you want to delete the editor?',
            okText: 'Yes',
            cancelText: 'Cancel',
            onOk() {
                that.removeData(editor);
                modal.destroy();
            },
            onCancel() { },
        });
    }

    //delete the editor
    removeData = (editor) => {
        HttpUtil.post(ApiUtil.API_EDITOR_DELETE, editor)
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

    // open a new page and get detail data
    getSettingData = (editor) => {
        this.props.history.push('/editorSetting/?id=' + editor.id);
    }

    render() {
        return (
            <Layout>
                <Content >
                    <div className="box" style={{ lineHeight: '64px', display: "flex", alignItems: "center" }}>
                        <Button style={{ display: "inline-block", margin: "10px" }} type="primary" onClick={() => this.showAddDialog()}>ADD EDITOR TEMPLATE</Button>
                        {/* <Search style={{width: 400, display:"inline-block",position:"absolute",right:"20px" ,verticalAlign:"middle"}} placeholder="search the name of editor" onSearch={this.onSearch} enterButton /> */}
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

                        <EditorInfoDialog
                            visible={this.state.addEditorDialog}
                            editor={this.state.editingItem}
                            afterClose={() => {
                                this.setState({ addEditorDialog: false });
                                this.getData();
                            }}
                        />
                    </div>
                </Content>
            </Layout>
        )
    }
}

export default Editor;
