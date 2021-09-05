/*
Date: 12 April 2021
Author：Yan Zhou a1807782
Description：front-end for dataset module
*/

import React from 'react';
import { Layout, message, Button, Table, Image } from 'antd';
import { LeftOutlined } from '@ant-design/icons';

import HttpUtil from '../Utils/HttpUtil';
import ApiUtil from '../Utils/ApiUtil';

const { Content } = Layout;

class DatasetGetImages extends React.Component {
  my_columns = [
    {
      title: 'IMAGE',
      dataIndex: 'filename',
      width: "160px",
    },
    {
      title: 'URL',
      dataIndex: 'url',
      width: "300px",
      render: (text, record) => {
        return (
          <span>
            <Image
              width={80}
              src={record.url}
            />
          </span>
        );
      },
    },
    {
      title: 'CREATOR',
      dataIndex: 'creator',
      width: "160px",
    },
    {
      title: 'CREATE_DATE',
      dataIndex: 'create_date',
      width: "160px",
    }
  
  ];

  mAllData = [];
  state = {
    mData: [], // data in table
    my_columns: [], //colunms
  }

  // React life cycle
  componentDidMount() {
    this.getData();
  }

  // get all the data
  getData = () => {
    // let {location} = this.props.history;
    // this.project = location.state.project;

    let parameters = this.props.location.search.split('=');
    let id = parameters[1];
    let json = { "dataset_id": id }

    HttpUtil.post(ApiUtil.API_DATASET_IMAGE_LIST, json)
      .then(
        imagesList => {
          this.mAllData = imagesList;
          this.setState({
            mData: imagesList,
          });
        }
      ).catch(error => {
        message.error(error.message);
      });
  }
  // return back to the previous page
  return = () => {
    window.history.back(-1)
  }

  render() {
    return (
      <Layout>
        <Content >
          <div>
            <Button style={{ display: "inline-block", margin: "20px" }} type="primary" ghost icon={<LeftOutlined />} onClick={() => this.return()}>BACK</Button>
          </div>
          <div style={{ background: '#fff', padding: 24, minHeight: 480 }}>
            <Table
              columns={this.my_columns}
              dataSource={this.state.mData}
              rowKey={item => item.id}
              pagination={{ pageSize: 10 }}
              scroll={{ y: 420 }} />
          </div>
        </Content>
      </Layout>
    )
  }
}
export default DatasetGetImages;
