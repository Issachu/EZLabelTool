/*
Date: 11 April 2021
Author：Yan Zhou a1807782
Description：front-end for project module
*/

import React from 'react';
import { Modal, Form, Checkbox,Button, message} from 'antd';
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
    { label: 'Delete', value: '0' },
    { label: 'Setup', value: '1' },
    { label: 'Export', value: '2' },
];

class ProjectSettingPermission extends React.Component {
    
    state = {
        visible: false,
        member: null,
        value: '2',
    }

    //get value from parent
    UNSAFE_componentWillReceiveProps(parentProps) {
        if (this.state.visible !== parentProps.visible) {
            this.setState({
                visible: parentProps.visible,
                member:parentProps.member,
                value:parentProps.member.permission,
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
        let permission="";
        let arrary = values.permission
        
        if (arrary !== undefined) {
            for(let i=0;i < arrary.length;i++){
                permission = permission + arrary[i] + ','
            }
        }

        let request={
            "id":this.state.member.id,
            // new role
            "role":this.state.member.role,
            "permission":permission,
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
                title="Change Permission"
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
                            label="Permission"
                            name="permission"
                        >
                            <Checkbox.Group options={options}/>
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
export default ProjectSettingPermission;