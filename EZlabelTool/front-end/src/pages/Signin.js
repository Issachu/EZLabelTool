/*
Date: 07 April 2021
Author：Yan Zhou a1807782
Description：front-end for signin module
*/

import React from 'react';
import { Button, Input, message, Card, Form, Radio } from 'antd';

import HttpUtil from '../Utils/HttpUtil';
import ApiUtil from '../Utils/ApiUtil';

const layout = {
  labelCol: { span: 8 },
  wrapperCol: { span: 16 },
};
const tailLayout = {
  wrapperCol: { offset: 8, span: 16 },
};

const tabList = [
  {
    key: 'tab1',
    tab: 'LOG IN',
  },
  {
    key: 'tab2',
    tab: 'SIGN UP',
  },
]

class Signin extends React.Component {
  state = {
    key: 'tab1',
    radio: 'a',
    noTitleKey: 'app',
  }

  onTabChange = (key, type) => {
    this.setState({ [type]: key })
  }

  onRadioChange = (key, type) => {
    this.setState({ [type]: key })
  }

  login = (values) => {
    HttpUtil.post(ApiUtil.API_LOG_IN, values)
      .then(
        re => {
          if (re.code === 0) {
            sessionStorage.setItem("isLogged", true);
            this.props.history.push('/home/project')
          } else {
            message.warning(re.message);
          }
        }
      )
      .catch(error => {
        message.error(error.message);
      });
  };

  signup = (values) => {

    if (values.org_name === undefined)
      values.org_name = ""

    if (values.org_code === undefined)
      values.org_code = ""

    HttpUtil.post(ApiUtil.API_SIGN_UP, values)
      .then(
        re => {
          this.props.history.push('/signin')
          if (re.code === 0) {
            message.info(re.message);
            this.setState({
              key: 'tab1',
            });
          } else {
            message.warning(re.message);
          }
        }
      )
      .catch(error => {
        message.error(error.message);
      });
  };

  onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
  };

  handleRodio = e => {
    this.setState({
      radio: e.target.value,
    });
  };


  render() {
    return (
      <div>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}>
          <img width="40%" src="../logo.png" alt="" />
        </div>
        <div
          style={{
            width: '100%',
            height: '100%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >

          <Card
            style={{ width: '40%' }}
            title=""
            tabList={tabList}
            activeTabKey={this.state.key}
            onTabChange={(key) => {
              this.onTabChange(key, 'key')
            }}>
            {this.state.key === 'tab1' && (
              <Form {...layout}
                name="login"
                initialValues={{ remember: true }}
                onFinish={this.login}
                onFinishFailed={this.onFinishFailed}
              >
                <Form.Item
                  label="Username"
                  name="name"
                  rules={[{ required: true, message: 'Please input your username!' }]}
                >
                  <Input />
                </Form.Item>
                <Form.Item
                  label="Password"
                  name="password"
                  rules={[{ required: true, message: 'Please input your password!' }]}
                >
                  <Input.Password />
                </Form.Item>
                <Form.Item {...tailLayout}>
                  <Button type="primary" htmlType="submit">
                    LOG IN
                  </Button>
                </Form.Item>
              </Form>
            )}
            {this.state.key === 'tab2' && (
              <Form {...layout}
                name="signup"
                initialValues={{ remember: true }}
                onFinish={this.signup}
                onFinishFailed={this.onFinishFailed}
              >
                <Form.Item
                  label="Username"
                  name="name"
                  rules={[
                    { required: true, message: 'Please input your username!' },
                    { max: 20, message: 'No more than 20 characters!' },
                    { pattern: new RegExp('^[a-z][0-9a-z]{1,}$', 'g'), message: 'Start with alphabets, combination of numbers & lowcase alphabets!' }
                  ]}
                >
                  <Input />
                </Form.Item>
                <Form.Item
                  label="Password"
                  name="password"
                  rules={[
                    { required: true, message: 'Please input your password!' },
                    { max: 20, message: 'No more than 20 characters!' },
                    { min: 4, message: 'At least 4 characters!' },
                    { pattern: new RegExp('^[0-9a-zA-Z]{1,}$', 'g'), message: 'Should be combination of numbers & alphabets!' }
                  ]}
                >
                  <Input.Password />
                </Form.Item>
                <Form.Item
                  label="Do you want"
                  name="choose"
                  rules={[{ required: true, message: 'Please choose!' }]}

                >
                  <Radio.Group onChange={this.handleRodio}>
                    <Radio value="a">Create Orgnization</Radio>
                    <Radio value="b">Join Orgnization</Radio>
                  </Radio.Group>
                </Form.Item>

                {(() => {
                  if (this.state.radio === 'a') {
                    return <Form.Item
                      label="Organization Name"
                      name="org_name"
                      rules={[{ required: true, message: 'Please input your organization name!' }]}
                    >
                      <Input />
                    </Form.Item>;
                  } else {
                    return <Form.Item
                      label="Organization Code"
                      name="org_code"
                      rules={[{ required: true, message: 'Please input the organization code with 6 characters!' }]}
                    >
                      <Input />
                    </Form.Item>;
                  }
                })()}
                <Form.Item {...tailLayout}>
                  <Button type="primary" htmlType="submit">
                    SIGN UP
                  </Button>
                </Form.Item>
              </Form>
            )}
          </Card>
        </div>
      </div>
    )
  }
}
export default Signin;
