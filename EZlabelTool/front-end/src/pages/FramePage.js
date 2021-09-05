/*
Date: 14 April 2021
Author：Jingyi Cui
Description: framepage
*/

import React from 'react';
import { Link, Route, Switch } from 'react-router-dom';

import HttpUtil from '../Utils/HttpUtil';
import ApiUtil from '../Utils/ApiUtil';

import Project from './Project';
import Dataset from './Dataset';
import User from './User';
import Editor from './Editor';
import Guide from './Guide';

import 'antd/dist/antd.css';
import './css/FramePage.css'
import { Layout, Menu, message } from 'antd';
import { ExportOutlined, UserOutlined } from "@ant-design/icons";
import FrameChangePassword from './FrameChangePassword';

const { Header, Content, Footer } = Layout;

class FramePage extends React.Component {

  state = {
    org_name: null,
    org_code: null,
    user_name: null,
    user_id: null,
    collapsed: false,
    changePasswordDialog: false,
  };

  // React life cycle
  componentDidMount() {
    // initialize the data
    if (sessionStorage.getItem("user_name")=== null) {
      HttpUtil.post(ApiUtil.API_GET_CURRENT_USER)
      .then(
        currentUser => {
          sessionStorage.setItem("user_name", currentUser.name);
          sessionStorage.setItem("role", currentUser.role);
          sessionStorage.setItem("org_name", currentUser.org_name);
          sessionStorage.setItem("org_code", currentUser.org_code);

          this.setState({
            user_name: sessionStorage.getItem("user_name"),
            role: sessionStorage.getItem("role"),
            org_name: sessionStorage.getItem("org_name"),
            org_code: sessionStorage.getItem("org_code")
          });
        }
        
      ).catch(error => {
        message.error(error.message);
      });
    }else{
      this.setState({
        user_name: sessionStorage.getItem("user_name"),
        role: sessionStorage.getItem("role"),
        org_name: sessionStorage.getItem("org_name"),
        org_code: sessionStorage.getItem("org_code")
      });
    }
  }


  logout = () => {
    HttpUtil.post(ApiUtil.API_LOG_OUT, "")
      .then(
        re => {
          if (re.code === 0) {
            message.info(re.message);
            sessionStorage.clear();
            this.props.history.push('/signin');
          } else {
            message.warning(re.message);
          }
        }
      )
      .catch(error => {
        message.error(error.message);
      });
  };

  showDialog() {
    this.setState({
      changePasswordDialog: true,
    });
  }

  render() {
    const path = this.props.location.pathname;
    return (
      <Layout className="layout" style={{ overflow: "hidden" }} >
        <Header style={{ display: "flex", justifyContent: "space-between" }}>
          <Menu theme="dark" onClick={this.handleClick} mode="horizontal" selectedKeys={[path]}>
            <Menu.Item key="/home/project"><Link to={'/home/project'}>Project</Link></Menu.Item>
            <Menu.Item key="/home/dataset"><Link to={'/home/dataset'}>Dataset</Link></Menu.Item>
            <Menu.Item key="/home/member"><Link to={'/home/member'}>Member</Link></Menu.Item>
            <Menu.Item key="/home/editor"><Link to={'/home/editor'}>Template Editor</Link></Menu.Item>
            <Menu.Item key="/home/guide"><Link to={'/home/guide'}>Guide</Link></Menu.Item>
          </Menu>
          <span>
            <h4 style={{ display: "inline-block", marginRight: "20px", color: "white" }}>{this.state.user_name}  in  {this.state.org_name} || ORGCODE : {this.state.org_code}</h4>
            <UserOutlined style={{ display: "inline-block", marginRight: "20px", marginTop: "25px", color: "white" }} onClick={() => this.showDialog()} />
            <ExportOutlined style={{ display: "inline-block", marginRight: "0px", marginTop: "25px", color: "white" }} onClick={this.logout} />
          </span>
        </Header>
        <Content style={{ padding: '0 50px', minHeight: 550 }}>
          <div className="site-layout-content">
            <Switch>
              <Route path="/home/project" component={Project} />
              <Route path="/home/dataset" component={Dataset} />
              <Route path="/home/member" component={User} />
              <Route path="/home/editor" component={Editor} />
              <Route path="/home/guide" component={Guide} />
            </Switch>
            <FrameChangePassword
              visible={this.state.changePasswordDialog}
              username={this.state.user_name}
              p_logout={this.logout}
              afterClose={() => {
                this.setState({ changePasswordDialog: false });
              }}
            />
          </div>
        </Content>
        <Footer style={{ textAlign: 'center' }}>EZ Label</Footer>
      </Layout>
    );
  }
}

export default FramePage;