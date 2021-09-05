/*
Date: 12 April 2021
Author：Yan Zhou a1807782
Description：front-end for dataset module
*/

import React from 'react';
import { Layout, Table, Button, Modal, message, Input, Popover } from 'antd';

import DatasetInfoDialog from './DatasetInfoDialog'
import DatasetUploadDialog from './DatasetUploadDialog'

import HttpUtil from '../Utils/HttpUtil';
import ApiUtil from '../Utils/ApiUtil';

const { Content } = Layout;
const { Search } = Input;

class Dataset extends React.Component {
    columns = [
        {
            title: 'NO.',
            width: "60px",
            render: (text, record, index) => `${this.state.current - 1}` * `${this.state.pageSize}` + index + 1,
        },
        {
            title: 'DATASET',
            dataIndex: 'name',
            width: "160px",
            align: 'center',
            render: (text, record) => {
                return (
                    <span>
                        <Button type="link" onClick={() => this.getDetailData(record)}>{record.name}</Button>
                    </span>
                );
            },
        },
        {
            title: 'ROWS',
            dataIndex: 'rows',
            width: "100px",
            align: 'center',
        },
        {
            title: 'PROJECTS',
            dataIndex: 'project',
            width: "100px",
            align: 'center',
            render: (text, record) => {
                if (record.project !== 0) {
                    return (
                        <span>
                            <Popover content={record.detail} title="Projects in use" trigger="hover">
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
            title: 'CREATOR',
            dataIndex: 'creator',
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
            title: 'OPERARIONS',
            key: 'action',
            align: 'center',
            render: (text, record) => {
                if (record.flag === "0") {
                    return (
                        <span>
                            <Button type="link" onClick={() => this.deleteConfirm(record)}>delete</Button>
                            <Button type="link" onClick={() => this.showUploadDialog(record)}>upload</Button>
                            <Button type="link" onClick={() => this.activeConfirm(record)}>activate</Button>
                        </span>
                    );
                } else {
                    return (
                        <span>
                            <Button type="link" onClick={() => this.deleteConfirm(record)}>delete</Button>
                        </span>
                    );
                }
            },
        },
    ];

    mAllData = [];
    state = {
        addDatasetDialog: false,
        uploadDialog: false,
        editingItem: null,
        mData: [], // data in table
        current: 1, // current page
        pageSize: 10,
    }

    // React life cycle
    componentDidMount() {
        this.getData();
    }

    // get all the data
    getData = () => {
        HttpUtil.post(ApiUtil.API_DATASET_LIST)
            .then(
                datasetList => {
                    this.mAllData = datasetList;
                    this.setState({
                        mData: datasetList,
                    });
                }
            ).catch(error => {
                message.error(error.message);
            });
    }

    // show the modal for add a new dataset
    showAddDialog() {
        this.setState({
            addDatasetDialog: true,
        });
    }

    showUploadDialog(item) {
        this.setState({
            uploadDialog: true,
            editingItem: item,
        });
    }

    // search function
    onSearch = value => {
        let query = {
            "name": value
        }

        HttpUtil.post(ApiUtil.API_DATASET_SEARCH, query)
            .then(
                datasetSearchList => {
                    this.mAllData = datasetSearchList;
                    this.setState({
                        mData: datasetSearchList,
                    });
                }
            ).catch(error => {
                message.error(error.message);
            });
    }

    //delete comfirm information
    deleteConfirm = (dataset) => {
        if (dataset.project === 0) {
            var that = this;
            const modal = Modal.confirm({
                title: 'Confirm',
                content: 'Do you want to delete the dataset?',
                okText: 'Yes',
                cancelText: 'Cancel',
                onOk() {
                    that.removeData(dataset);
                    modal.destroy();
                },
                onCancel() { },
            });
        } else {
            Modal.warning({
                title: 'This dataset is in use.',
                content: 'Please delete the associated projects first.',
            });
        }

    }

    //delete the dataset
    removeData = (dataset) => {
        HttpUtil.post(ApiUtil.API_DATASET_DELETE, dataset)
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

    //active comfirm information
    activeConfirm = (dataset) => {
        var that = this;
        if (dataset.rows === '0') {
            message.warn("There is no image in the dataset, upload images before activating it.");
        } else {
            const modal = Modal.confirm({
                title: 'Confirm',
                content: 'Do you want to active the dataset? You cannot upload images after activating it.',
                okText: 'Yes',
                cancelText: 'Cancel',
                onOk() {
                    that.activeData(dataset);
                    modal.destroy();
                },
                onCancel() { },
            });
        }
    }

    //active the dataset
    activeData = (dataset) => {
        HttpUtil.post(ApiUtil.API_DATASET_ACTIVE, dataset)
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

    // open a new page and get detail images
    getDetailData = (dataset) => {
        this.props.history.push('/images/?id=' + dataset.id);
    }

    render() {
        return (
            <Layout>
                <Content >
                    <div class="box" style={{ lineHeight: '64px', display: "flex", alignItems: "center" }}>
                        <Button style={{ display: "inline-block", margin: "10px" }} type="primary" onClick={() => this.showAddDialog()}>ADD DATASET</Button>
                        <Search style={{ width: 400, display: "inline-block", position: "absolute", right: "20px", verticalAlign: "middle" }} allowClear placeholder="search the name of dataset" onSearch={this.onSearch} enterButton />
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

                        <DatasetInfoDialog
                            visible={this.state.addDatasetDialog}
                            dataset={this.state.editingItem}
                            afterClose={() => {
                                this.setState({ addDatasetDialog: false });
                                this.getData();
                            }}
                        />

                        <DatasetUploadDialog
                            visible={this.state.uploadDialog}
                            dataset={this.state.editingItem}
                            afterClose={() => {
                                this.setState({ uploadDialog: false });
                                this.getData();
                            }}
                        />
                    </div>
                </Content>
            </Layout>
        )
    }
}

export default Dataset;
