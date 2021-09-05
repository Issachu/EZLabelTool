/*
Date: 7 May 2021
Author：Yan Zhou a1807782
Description：front-end for change password
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

class FrameChangePassword extends React.Component {

    state = {
        visible: false,
        username: "",
    }

    //get value from parent
    UNSAFE_componentWillReceiveProps(parentProps) {
        if (this.state.visible !== parentProps.visible) {
            this.setState({
                visible: parentProps.visible,
                username: parentProps.username
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
        if (values.new_password === values.confirm_password) {
            HttpUtil.post(ApiUtil.API_USER_RESET, values)
                .then(
                    re => {
                        if (re.code === 0) {
                            message.info(re.message);
                            this.props.p_logout();
                            this.setState({
                                visible: false,
                            });
                        } else {
                            message.warning(re.message);
                        }
                    }
                )
                .catch(error => {
                    message.error(error.message);
                });
        } else {
            message.warning("Please confirm your new password!");
        }
    }

    // generate the error info if failed
    onFinishFailed = (errorInfo) => {
        console.log('Failed:', errorInfo);
    };

    render() {
        const { visible, username } = this.state;

        return (
            <Modal
                title="Change Password"
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
                        initialValues={{ name: username }}
                    >
                        <Form.Item
                            label="User Name"
                            name="name"
                        >
                            <Input disabled />
                        </Form.Item>
                        <Form.Item
                            label="Password"
                            name="current_password"
                            rules={[{ required: true, message: 'Please input your current password!' }]}
                        >
                            <Input.Password />
                        </Form.Item>
                        <Form.Item
                            label="New Password"
                            name="new_password"
                            rules={[{ required: true, message: 'Please input your new password!' }]}
                        >
                            <Input.Password />
                        </Form.Item>
                        <Form.Item
                            label="Confirm Password"
                            name="confirm_password"
                            rules={[{ required: true, message: 'Please confirm your new password!' }]}
                        >
                            <Input.Password />
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
export default FrameChangePassword;