/*
Date: 11 April 2021
Author：Yan Zhou a1807782
Description：front-end for project module
*/

import React from 'react';
import { Modal, Form, Radio,Button, message} from 'antd';
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

const options = [
    { label: 'Labeller', value: '1' },
    { label: 'Reviewer', value: '2' },
    { label: 'None', value: '4' },
];

class ProjectSettingRole extends React.Component {
    
    state = {
        visible: false,
        member: null,
        value: '',
    }

    //get value from parent
    UNSAFE_componentWillReceiveProps(parentProps) {
        if (this.state.visible !== parentProps.visible) {
            this.setState({
                visible: parentProps.visible,
                member:parentProps.member,
                value:parentProps.member.role,
            });
        }
    }

    // if cancel, then close the dialog
    handleCancel = ()=>{
        this.setState({
            visible: false,
        });
    }

    // post request to the backend if submit
    handleSubmit = (values) => {
        let request={
            "id":this.state.member.id,
            // new role
            "role":values.role,
            "permission":this.state.member.permission,
        }

        HttpUtil.post(ApiUtil.API_PROJECT_ROLE_PERMISSION, request)
            .then(
                re=>{
                    message.info(re.message);
                }
            )
            .catch(error=>{
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
    
    render(){
        const {visible } = this.state;
        // const {value } = this.state;
        return(
            <Modal 
                title="Change Role"
                style={{top:20}}
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
                            label="Role"
                            name="role"
                            rules={[{ required: true, message: 'Please select the role!' }]}
                        >
                            <Radio.Group
                                options={options}
                                // value={value}
                                optionType="button"
                            />
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
export default ProjectSettingRole;