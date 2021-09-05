/*
Date: 14 April 2021
Author：Jingyi Cui
Description：front-end for editor module
*/

import React from 'react';
import { Modal, Form, Input, Button, message } from 'antd';
import ApiUtil from '../Utils/ApiUtil';
import HttpUtil from '../Utils/HttpUtil';

// style for the form
const layout = {
    labelCol: { span: 8 },
    wrapperCol: { span: 16 },
};

// style for the submit in form
const tailLayout = {
    wrapperCol: { offset: 8, span: 16 },
};

class EditorInfoDialog extends React.Component {

    state = {
        visible: false,
        editor: {},
    }

    //get value from parent
    UNSAFE_componentWillReceiveProps(parentProps) {
        if (this.state.visible !== parentProps.visible) {
            this.setState({
                visible: parentProps.visible
            });
        }
    }

    // if cancel, then close the dialog
    handleCancel = () => {
        this.setState({
            visible: false,
        });
    }

    // post request to the backend if submit
    handleSubmit = (values) => {
        HttpUtil.post(ApiUtil.API_EDITOR_ADD, values)
            .then(
                re => {
                    message.info(re.message);
                }
            )
            .catch(error => {
                message.error(error.message);
            });

        this.setState({
            visible: false,
        });
    }

    // generate the error info if failed
    onFinishFailed = (errorInfo) => {
        console.log('Failed:', errorInfo);
    };

    render() {
        const { visible } = this.state;

        return (
            <Modal
                title="Add Editor Template"

                style={{ top: 20 }}
                width={500}
                afterClose={this.props.afterClose}
                onCancel={this.handleCancel}
                visible={visible}
                footer={null}
                destroyOnClose={true}
            >
                <div>
                    <Form {...layout}
                        name="form_in_modal"
                        onFinish={this.handleSubmit}
                        onFinishFailed={this.onFinishFailed}
                    >
                        <Form.Item
                            label="Editor Name"
                            name="name"
                            rules={[{ required: true, message: 'Please input your editor name!' }]}
                        >
                            <Input />
                        </Form.Item>
                        <Form.Item
                            label="Description"
                            name="desc"
                            initialValue=""
                        >
                            <Input.TextArea />
                        </Form.Item>
                        <Form.Item {...tailLayout}>
                            <Button type="primary" htmlType="submit">Confirm</Button>
                        </Form.Item>
                    </Form>
                </div>
            </Modal>
        );
    }
}
export default EditorInfoDialog;