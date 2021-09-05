/*
Date: 11 April 2021
Author：Yan Zhou a1807782
Description：front-end for project module
*/

import React from 'react';
import { Layout, Typography, Space } from 'antd';


const { Content } = Layout;
const { Title,Text} = Typography;

class Guide extends React.Component {
    

    render() {
        return (
            <Layout>
                <Content>
                    <div className="box" style={{ lineHeight: '64px',  display: "flex", alignItems: "center" }} >
                    </div>
                    <div style={{ background: '#fff', padding: 24, height: 530, width: "96%",overflow:"auto", }}>
                    <Title level={4}>1. How to organize my team?</Title>
                    <Space direction="vertical">
                    <Text>If you created an organization when signing up, now you are the team administrator.</Text>
                    <Text>Provide your team members with the ORGCODE at the upper right corner to enable them to join in.</Text>
                    </Space>

                    <Title level={4}>2.Introduction of the menu</Title>
                    <Space direction="vertical">
                    <Text mark>Project</Text>
                    <Text>You’d better create something in Dataset and Editor before moving here. There are four main processes here:</Text>
                    <Text type="success">Setup</Text>
                    <Text>You should setup the project after creating it. Setting stage includes: select members, attach datasets and choose an editor template. </Text>
                    <Text>These data should be prepared under the following three menus.</Text>
                    <Text type="success">Label</Text>
                    <Text>The members who are labelers can label the images.</Text>
                    <Text type="success">Review</Text>
                    <Text>The members who are reviewers can review the labeled images and comment them.</Text>
                    <Text type="success">Export</Text>
                    <Text>User can export the data when the whole project has been completed.</Text>

                    <Text mark>Dataset</Text>
                    <Text>This is a place to store datasets, so you can attach these datasets to different projects for labelers to annotate.</Text>
                    <Text>Main process: Create dataset - Upload images - Activate the dataset when the dataset is prepared.</Text>

                    <Text mark>Member</Text>
                    <Text>You can find all the members in the organization here. </Text>
                    <Text>If you are the administrator, you can remove any members or help them reset their password.</Text>

                    <Text mark>Editor</Text>
                    <Text>You can configure editor templates here. A project can use one of these editor to label the images.</Text>
                    <Text>You can modify the template at any time. However, the editor  bound to a project will not be affected.</Text>
                    <Text>Main process: Create editor - Setup it!</Text>

                    <Text mark>Guide</Text>
                    <Text>Yeah, you are here now, this is a user guide for you.</Text>
                    </Space>
                    </div>
                </Content>
            </Layout>
        )
    }
}

export default Guide;
