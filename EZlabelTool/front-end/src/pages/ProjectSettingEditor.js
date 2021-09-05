/*
Date: 24 April 2021
Author：Pingyi Hu a1805597
Description：front-end for editor setting in project module
*/

import React from 'react';
import { Table, Button, message } from 'antd';
import "antd/dist/antd.css";
import ProjectSettingEditorSetting from './ProjectSettingEditorSetting';
import HttpUtil from '../Utils/HttpUtil';
import ApiUtil from '../Utils/ApiUtil';

class ProjectSettingEditor extends React.Component {
  columns = [
    {
      title: 'EDITOR',
      dataIndex: 'name',
      width: "160px",
    },
    {
      title: 'DESCRIPTION',
      dataIndex: 'desc',
      width: "300px",
    },
    {
      title: 'OPERARIONS',
      key: 'action',
      align: 'center',
      render: (text, record) => {
        if(this.props.setup === -1){
          return (
            <span>
              <Button type="link" disabled>choose</Button>
            </span>
          );
        }else{
          return (
            <span>
              <Button type="link" onClick={() => this.getSettingData(record)}>choose</Button>
            </span>
          );
        }
        
      },
    }
  ];

  state = {
    editor_copy_id: "",
    editor_list: [],
    objects: [],
    classifications: [],
  }

  getSettingData = (editor) => {
    let id = { editor_id: editor.id, project_id: this.props.projectId };
    console.log(id);
    HttpUtil.post(ApiUtil.API_EDITOR_CHOOSE, id)
      .then(
        re => {
          if (re.code === -1){
            message.info(re.message);
          }else {
            let id = re.editor_copy_id;
            this.setState({
              editor_copy_id: id
            });
            message.info(re.message);
          }
        }
      ).catch(error => {
        message.error(error.message);
      });
  }

  // React life cycle
  componentDidMount() {
    this.getdata();
  }

  getdata = () => {
    if (JSON.stringify(this.props.editor) === '{}') {
      HttpUtil.post(ApiUtil.API_EDITOR_LIST)
        .then(
          editorList => {
            this.setState({
              editor_list: editorList,
            });
          }
        ).catch(error => {
          message.error(error.message);
        });
    } else {
      this.setState({
        editor_copy_id: this.props.editor.id
      });
    }
  }
  
  render() {
    if (this.state.editor_copy_id === "") {
      return (
        <div>
          <p style={{color:'#1890FF'}}>Please choose an editor template for labeling. You can also configure the template according to your own requirements.</p>
          <Table
            columns={this.columns}
            dataSource={this.state.editor_list}
            rowKey={item => item.id}
            pagination={{ pageSize: 10 }}
            scroll={{ y: 340 }}
          />
        </div>
      );
    }
    else {
      return (
        <div>
          <ProjectSettingEditorSetting
            editor_copy_id={this.state.editor_copy_id}
          />
        </div>
      );
    }
  }
}
export default ProjectSettingEditor;
