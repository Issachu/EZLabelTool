/*
Date: 12 April 2021
Author：Yan Zhou a1807782
Description：front-end for dataset module
*/

import React from 'react';
import { Modal, Upload, Button, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';

import ApiUtil from '../Utils/ApiUtil';
import HttpUtil from '../Utils/HttpUtil';

const UPLOAD_URL = ApiUtil.API_DATASET_UPLOAD
const fileList = [];

class DatasetUploadDialog extends React.Component {

    state = {
        visible: false,
        dataset: null,
        fileList: [],
        uploading: false,
        previewVisible: false,
        previewImage: '',
        previewImageName: ''
    }

    //get value from parent
    UNSAFE_componentWillReceiveProps(parentProps) {
        if (this.state.visible !== parentProps.visible) {
            this.setState({
                visible: parentProps.visible,
                dataset: parentProps.dataset
            });
        }
    }

    // if cancel, then close the dialog
    handleCancel = () => {
        this.setState({
            visible: false,
        });
    }

    // show pic preview
    showPreview = file => {
        this.setState({
            previewVisible: true,
            previewImage: file.url || file.thumbUrl,
            previewImageName: file.name
        })
    }

    // hide pic preview
    hidePreview = () => {
        this.setState({
            previewVisible: false
        })
    }

    // get the state while updating
    handleChange = ({ file, fileList }) => {
        const { status, response } = file
        if (status === 'done') {
            const { ok, message: msg } = response
            if (ok) {
                message.success(msg)
                file.url = response.url
            } else {
                message.error(msg)
            }
        }
        this.setState({ fileList })
    }

    handleRemove = fileList => {
        let request = {
            "alias": fileList.response.alias,
        };
        HttpUtil.post(ApiUtil.API_DATASET_IMG_DELETE, request)
            .then(
                re => {
                    message.info(re.message);
                }
            ).catch(error => {
                message.error(error.message);
            });
    }

    render() {
        const { previewVisible, previewImage, previewImageName } = this.state
        const { visible } = this.state;
        return (
            <Modal
                title="Upload Image Data"
                style={{ top: 20, width: '100%' }}
                fullScreen="true"
                afterClose={this.props.afterClose}
                onCancel={this.handleCancel}
                visible={visible}
                footer={null}
                destroyOnClose={true}
            >
                <p>Please upload png, jpg or jpeg images.</p>
                <br/>
                <Upload multiple
                    action={UPLOAD_URL}
                    listType="picture"
                    data={this.state.dataset}
                    defaultFileList={[...fileList]}
                    onPreview={this.showPreview}
                    onChange={this.handleChange}
                    onRemove={this.handleRemove}
                >
                    <Button icon={<UploadOutlined />}>Upload</Button>
                </Upload>
                <Modal
                    visible={previewVisible}
                    footer={null}
                    onCancel={this.hidePreview}
                >
                    <img
                        src={previewImage}
                        alt={previewImageName}
                        style={{ width: '100%' }}
                    />
                </Modal>
            </Modal>
        );
    }
}
export default DatasetUploadDialog;