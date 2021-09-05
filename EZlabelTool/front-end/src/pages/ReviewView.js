/*
Date: 23 April 2021
Author：Pingyi Hu a1805597
Description：The review module
*/

import React, { useState, useEffect } from "react";
import { Stage, Layer, Line, Rect } from "react-konva";
import 'antd/dist/antd.css';
import { Layout, List, Menu, Button, message, Select, Modal, Typography } from 'antd';
import { LeftOutlined, AimOutlined, HomeOutlined, BorderOutlined, StarOutlined} from '@ant-design/icons';
import uuid from "uuid/v1";
import ImageFromUrl from "./ImageFromUrl";
import Annotation from "./Annotation";
import HttpUtil from '../Utils/HttpUtil';
import ApiUtil from '../Utils/ApiUtil';

const { Header, Footer, Sider, Content } = Layout;
const { Option } = Select;
const { Title } = Typography;

const reviewOption = [
  { label: "Not reviewed", value: "0" },
  { label: "Bad", value: "1" },
  { label: "Unsure", value: "2" },
  { label: "Good", value: "3" },
];

export default function App(props) {
  const [measure, setMeasure] = useState(1);
  const [previousStatus, setPreviousStatus] = useState("");
  const [project_id, setProject_id] = useState("");
  const [image_id, setImage_id] = useState("");
  const [url, setUrl] = useState("");
  const [objects, setObjects] = useState([]);
  const [classifications, setClassifications] = useState([]);
  const [classificationResults, setClassificationResults] = useState([]);
  const [review, setReview] = useState("");
  const [annotations, setAnnotations] = useState([]);
  const [polygons, setPolygons] = useState([]);
  const [newAnnotation, setNewAnnotation] = useState([]);
  const [newPolygon, setNewPolygon] = useState([]);
  const [isStarted, setIsStarted] = useState(false);
  const [points, setPoints] = useState([]);
  const [coord, setCoord] = useState([]);
  const [polygonIsMouseOverStartPoint, setPolygonIsMouseOverStartPoint] = useState(false);
  const [polygonIsFinished, setPolygonIsFinished] = useState(false);
  const [selectedId, selectAnnotation] = useState(null);
  const [selectedPolygonId, selectPolygon] = useState(null);
  const [selectedName, setSelectedName] = useState(null);
  const [selectedShape, setSelectedShape] = useState(null);
  const [selectedColor, setSelectedColor] = useState("blue");
  const [canvasMeasures, setCanvasMeasures] = useState({
    width: window.innerWidth * 0.7,
    height: window.innerHeight * 0.8
  });
  const [stageScale, setStageScale] = useState({
    scale: 1,
    stageX: 0,
    stageY: 0
  });
  const [isDrawing, setIsDrawing] = useState(false);
  const [changed, setChanged] = useState(false);
  const [imageName, setImageName] = useState("");

  // return back to the previous page
  const returnBack = () => {
    if (changed) {
      const modal = Modal.confirm({
        title: 'Confirm',
        content: 'Are you sure you want to leave this page without saving?',
        okText: 'Yes',
        cancelText: 'Cancel',
        onOk() {
          handleBack();
          modal.destroy();
        },
        onCancel() { },
      });
    }
    else {
      handleBack();
    }
  };

  const handleBack = () => {
    let values = {
      image_id: image_id,
      project_id: project_id,
      status: previousStatus,
    };
    HttpUtil.post(ApiUtil.API_LABEL_BACK, values)
      .then(
        re => {
          // console.log(re.message);
        }
      )
      .catch(error => {
        message.error(error.message);
      });
    window.history.back(-1);
  };

  useEffect(() => {
    let parameters = props.location.search.split('=');
    let str = parameters[1];
    let id = str.substring(0, str.indexOf("&"));
    let image_id = parameters[2];
    setProject_id(id);
    window.localStorage["project_id"] = id;
    window.localStorage["image_id"] = image_id;
    window.localStorage["previous_status"] = "0";
    let json = { id: id };
    HttpUtil.post(ApiUtil.API_PROJECT_EDITOR_COPY_SETTING, json)
      .then((datasetList) => {
        datasetList.classifications.forEach((v, i) => {
          const classesArray = datasetList.classifications[i].classes.split(',');
          datasetList.classifications[i].classes = [].concat(classesArray);
        });
        setObjects(datasetList.objects);
        setClassifications(datasetList.classifications);
        setCanvasMeasures({
          width: window.innerWidth * 0.7,
          height: window.innerHeight * 0.8
        });
      })
      .catch((error) => {
        message.error(error.message);
      });
    handleChooseImage();
  }, []);

  const getWindowSize = () => (
    {
      width: window.innerWidth * 0.7,
      height: window.innerHeight * 0.8
    }
  );
  const handleResize = () => {
    setCanvasMeasures(getWindowSize());
  }

  useEffect(() => {
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const handleLeaveBack = () => {
    let values = {
      image_id: window.localStorage.image_id,
      project_id: window.localStorage.project_id,
      status: window.localStorage.previous_status,
    };
    HttpUtil.post(ApiUtil.API_LABEL_BACK, values)
      .then(
        re => {
        }
      )
      .catch(error => {
        message.error(error.message);
      });
  };

  // return back to the home page
  const returnHome = () => {
    if (changed) {
      const modal = Modal.confirm({
        title: 'Confirm',
        content: 'Are you sure you want to leave this page without saving?',
        okText: 'Yes',
        cancelText: 'Cancel',
        onOk() {
          handleHome();
          modal.destroy();
        },
        onCancel() { },
      });
    }
    else {
      handleHome();
    }
  };

  const handleHome = () => {
    let values = {
      image_id: image_id,
      project_id: project_id,
      status: previousStatus,
    };
    HttpUtil.post(ApiUtil.API_LABEL_BACK, values)
      .then(
        re => {
          // console.log(re.message);
        }
      )
      .catch(error => {
        message.error(error.message);
      });
    props.history.push('/home/project');
  };

  useEffect(() => {
    const listener = ev => {
      ev.preventDefault();
      ev.returnValue = 'Please save your changes before leaving';
      handleLeaveBack();
    };
    window.addEventListener('beforeunload', listener);
    return () => {
      window.removeEventListener('beforeunload', listener)
    }
  }, []);

  useEffect(() => {
    const listener = () => {
      handleLeaveBack();
    };
    window.addEventListener('popstate', listener);
    return () => {
      window.removeEventListener('popstate', listener)
    }
  }, []);

  const handleChooseImage = () => {
    let parameters = props.location.search.split('=');
    let str = parameters[1];
    let id = str.substring(0, str.indexOf("&"));
    let image_id = parameters[2];
    let json_info = { project_id: id, image_id: image_id };
    HttpUtil.post(ApiUtil.API_REVIEW_VIEW_CHOOSE, json_info)
      .then((result) => {
        if (result.code === 0) {
          setImage_id(result.id);
          setImageName(result.filename);
          window.localStorage.image_id = result.id;
          setUrl(result.url);
          setAnnotations(result.bbox);
          setPolygons(result.polygon);
          setClassificationResults(result.classes);
          window.localStorage.previous_status = result.status;
          setReview(result.review);
          setPreviousStatus(result.status);
          setCanvasMeasures({
            width: window.innerWidth * 0.7,
            height: window.innerHeight * 0.8
          });
          setStageScale({
            scale: 1,
            stageX: 0,
            stageY: 0
          });
          setIsDrawing(false);
          setChanged(false);
        } else if (result.code === 1) {
          message.info(result.message);
          window.history.back(-1);
        }

      }).catch((error) => {
        message.error(error.message);
      });
  };

  const createMenuList = (list) => {
    return list.map((item) => {
      return (
        <Menu.Item key={[item.name, item.shape, item.color]}>
          <span>
            {objectIcon(item.shape, item.color)}
            {item.name}
          </span>
        </Menu.Item>
      );
    }
    );
  };

  const objectIcon=(type,color)=>{
    if (type === "Bounding Box") return(<BorderOutlined style={{color:color}}/>);
    else if (type === "Polygon") return(<StarOutlined style={{color:color}}/>);
  };


  const handleChooseClass = (value, option) => {
    setChanged(true);
    let result = {
      name: option.title,
      class: value,
    };
    if (classificationResults.length === 0) {
      classificationResults.push(result);
      setClassificationResults(classificationResults);
    } else {
      let changed = true;
      for (let i = 0; i < classificationResults.length; ++i) {
        if (classificationResults[i].name === option.title) {
          classificationResults[i].class = value;
          setClassificationResults(classificationResults);
          changed = false;
        }
      }
      if (changed) {
        classificationResults.push(result);
        setClassificationResults(classificationResults);
      }
    }
  }

  const handleChooseClassM = (value, option) => {
    setChanged(true);
    if (option.length > 0) {
      let result = {
        name: option[0].title,
        class: value,
      };
      if (classificationResults.length === 0) {
        classificationResults.push(result);
        setClassificationResults(classificationResults);
      } else {
        let changed = true;
        for (let i = 0; i < classificationResults.length; ++i) {
          if (classificationResults[i].name === option[0].title) {
            classificationResults[i].class = value;
            setClassificationResults(classificationResults);
            changed = false;
          }
        }
        if (changed) {
          classificationResults.push(result);
          setClassificationResults(classificationResults);
        }
      }
    }
  }

  function getClass(name) {
    for (let i = 0; i < classificationResults.length; ++i) {
      if (classificationResults[i].name === name) {
        return (classificationResults[i].class);
      }
    }
  }

  function getDefaultValue() {
    return (review);
  }

  const createClassficationList = (list) => {
    return list.map((item) => {
      if (item.type === "Radio") {
        return (
          <div key={item.name}>
            <div style={{ width: 200, height: 36, marginLeft: 10, marginTop: 15 }}>{item.name}</div>
            <Select
              style={{ width: 150, marginLeft: 10 }}
              placeholder="One choice"
              key={getClass(item.name)}
              defaultValue={getClass(item.name)}
              onChange={handleChooseClass}
            >
              {item.classes.map(d => (<Option key={d} title={item.name}>{d}</Option>))}
            </Select>
          </div>
        );
      } else {
        return (
          <div key={item.name}>
            <div style={{ width: 200, height: 36, marginLeft: 10, marginTop: 15 }}>{item.name}</div>
            <Select
              mode="multiple"
              style={{ width: 150, marginLeft: 10 }}
              placeholder="Multiple choices"
              key={getClass(item.name)}
              defaultValue={getClass(item.name)}
              onChange={handleChooseClassM}
            >
              {item.classes.map(d => (<Option key={d} title={item.name}>{d}</Option>))}
            </Select>
          </div>
        );
      }
    });
  };

  const handleReview = (value) => {
    setChanged(true);
    setReview(value);
  };

  const handleMenuClick = e => {
    const name = e.key.split(',')[0];
    const shape = e.key.split(',')[1];
    const color = e.key.split(',')[2];
    setSelectedName(name);
    setSelectedShape(shape);
    setSelectedColor(color);
    setPolygonIsFinished(false);
    setPolygonIsMouseOverStartPoint(false);
    setIsStarted(false);
    setNewPolygon([]);
    setNewAnnotation([]);
    setPoints([]);
    setCoord([]);
    setIsDrawing(true);
  };

  const handleMouseDown = event => {
    var { x, y } = event.target.getStage().getPointerPosition();
    if (selectedName !== null && selectedId === null && newAnnotation.length === 0 && selectedShape === "Bounding Box") {
      setChanged(true);
      x = (x - stageScale.stageX) / stageScale.scale;
      y = (y - stageScale.stageY) / stageScale.scale;
      const label_id = uuid();
      const name = selectedName;
      const shape = selectedShape;
      const color = selectedColor;
      setNewAnnotation([{ x: x / measure, y: y / measure, width: 0, height: 0, label_id, name: name, shape: shape, color: color }]);
    }
    else if (selectedId === null && newAnnotation.length === 1 && selectedName !== null && selectedShape === "Bounding Box"){
      annotations.push(...newAnnotation);
      setAnnotations(annotations);
      setIsDrawing(false);
      setNewAnnotation([]);
      setSelectedName(null);
      setSelectedShape(null);
    }
    else if (selectedName !== null && selectedId === null && newAnnotation.length === 0 && selectedShape === "Polygon") {
      x = (x - stageScale.stageX) / stageScale.scale;
      y = (y - stageScale.stageY) / stageScale.scale;
      const curMouse = [x / measure, y / measure];
      const label_id = uuid();
      const name = selectedName;
      const shape = selectedShape;
      const color = selectedColor;
      if (polygonIsFinished && isStarted) {
        return;
      }
      if (polygonIsMouseOverStartPoint && isStarted) {
        setChanged(true);
        setPolygonIsFinished(true);
        // console.log("finished");
        newPolygon[0].closed = true;
        setNewPolygon(newPolygon);
        polygons.push(...newPolygon);
        setIsDrawing(false);
        setPolygons(polygons);
        setPoints([]);
        setCoord([]);
        setNewPolygon([]);
      }
      else {
        setIsStarted(true);
        points.push(x / measure);
        points.push(y / measure);
        coord.push(curMouse);
        setNewPolygon([{
          points: points,
          coord: coord,
          name: name,
          shape: shape,
          color: color,
          label_id: label_id,
          closed: false
        }])
      }
    }
  };

  const handleMouseMove = event => {
    if (selectedName !== null && selectedId === null && newAnnotation.length === 1 && selectedShape === "Bounding Box") {
      const sx = newAnnotation[0].x;
      const sy = newAnnotation[0].y;
      var { x, y } = event.target.getStage().getPointerPosition();
      x = (x - stageScale.stageX) / stageScale.scale;
      y = (y - stageScale.stageY) / stageScale.scale;
      const label_id = uuid();
      const name = selectedName;
      const shape = selectedShape;
      const color = selectedColor;
      setNewAnnotation([
        {
          x: sx,
          y: sy,
          width: x / measure - sx,
          height: y / measure - sy,
          label_id,
          name: name,
          color: color,
          shape: shape
        }
      ]);
    }
  };

  const handleMouseUp = () => {
    // if (selectedId === null && newAnnotation.length === 1) {
    //   annotations.push(...newAnnotation);
    //   setAnnotations(annotations);
    //   // console.log(annotations)
    //   setIsDrawing(false);
    //   setNewAnnotation([]);
    //   setSelectedName(null);
    //   setSelectedShape(null);
    // }
  };

  const handleMouseOverStartPoint = event => {
    if (polygonIsFinished || points.length < 6) return;
    event.target.scale({ x: 2, y: 2 });
    setPolygonIsMouseOverStartPoint(true);
  };
  const handleMouseOutStartPoint = event => {
    event.target.scale({ x: 1, y: 1 });
    setPolygonIsMouseOverStartPoint(false);
  };

  const handleMouseEnter = event => {
    event.target.getStage().container().style.cursor = "crosshair";
  };

  const handleKeyDown = event => {
    if (event.keyCode === 8 || event.keyCode === 46) {
      if (selectedId !== null) {
        const newAnnotations = annotations.filter(
          annotation => annotation.label_id !== selectedId
        );
        setAnnotations(newAnnotations);
      }
      else if (selectedPolygonId !== null) {
        const newPolygons = polygons.filter(
          polygon => polygon.label_id !== selectedPolygonId
        );
        setPolygons(newPolygons);
      }
    }
  };

  const handleWheel = e => {
    e.evt.preventDefault();
    const scaleBy = 1.01;
    const stage = e.target.getStage();
    const oldScale = stage.scaleX();
    const mousePointTo = {
      x: stage.getPointerPosition().x / oldScale - stage.x() / oldScale,
      y: stage.getPointerPosition().y / oldScale - stage.y() / oldScale
    };

    const newScale = e.evt.deltaY > 0 ? oldScale * scaleBy : oldScale / scaleBy;

    stage.scale({ x: newScale, y: newScale });

    setStageScale({
      scale: newScale,
      stageX:
        -(mousePointTo.x - stage.getPointerPosition().x / newScale) * newScale,
      stageY:
        -(mousePointTo.y - stage.getPointerPosition().y / newScale) * newScale
    });
    // console.log(stageScale);
  };

  const resetScale = () => {
    setStageScale({
      scale: 1,
      stageX: 0,
      stageY: 0
    });
  };

  const handleSubmit = () => {
    if (review === "0") {
      message.info("you need to review this image!");
    }
    else {
      let values = {
        image_id: image_id,
        project_id: project_id,
        bbox: annotations,
        polygons: polygons,
        classResult: classificationResults,
        review: review,
        measure: measure
      };
      // console.log(values);
      HttpUtil.post(ApiUtil.API_REVIEW_SUBMIT, values)
        .then(
          re => {
            window.localStorage.previous_status = re.status;
          }
        )
        .then(() => { window.history.back(-1); })
        .catch(error => {
          message.error(error.message);
        });
    }
  };

  const annotationsToDraw = [...annotations, ...newAnnotation];
  const polygonsToDraw = [...polygons, ...newPolygon];
  return (
    <Layout>
      <Header style={{ display: "flex", justifyContent: "space-between", paddingLeft: "0px", paddingRight: "0px"}}>
        <div style={{ lineHeight: '64px', fontSize: "20px", color: "white"}}>
          <HomeOutlined style={{ display: "inline-block", marginLeft: "10px" }} type="primary" onClick={() => returnHome()} />
          <Button style={{ display: "inline-block", margin: "20px" }}  ghost icon={<LeftOutlined />} onClick={() => returnBack()}>BACK</Button>
          <span style={{ marginLeft: "300px"}}>
            {imageName}
            <Title level={4} style={{ display: "inline-block", margin: "10px" }}></Title>
            <AimOutlined style={{ display: "inline-block", margin: "20px" }} type="dashed" shape="circle" onClick={() => resetScale()} />
          </span>
        </div>
        <span>
          <Button style={{ display: "inline-block", marginRight: "20px" }} type="primary" onClick={handleSubmit}>SUBMIT</Button>
        </span>
      </Header>
      <Layout>
      <Sider theme="light">
          <div style={{ width: 200, height: 36, background: "#F5F5F5", textAlign: "center", lineHeight: '36px', fontSize: "16px" }}>Objects</div>
          <Menu
            onClick={handleMenuClick}
            selectable={false}
            mode="inline"
            style={{ width: 200 }}
          >
            {createMenuList(objects)}
          </Menu>
          <div style={{ width: 200, height: 36, background: "#F5F5F5", textAlign: "center", lineHeight: '36px', fontSize: "16px" }}>Classifications</div>
          <div>
            {createClassficationList(classifications)}
          </div>
          <div style={{ width: 200, height: 36, marginTop: 10, background: "#F5F5F5", textAlign: "center", lineHeight: '36px', fontSize: "16px" }}>Review</div>
          <div>
            <Select
              key={getDefaultValue()}
              defaultValue={getDefaultValue()}
              style={{ width: 150, marginLeft: 10, marginTop: 10 }}
              onChange={handleReview}
              options={reviewOption}
            >
            </Select>
          </div>
        </Sider>
        <Content style={{ padding: '5 5px', minHeight: 800 }}>
          <div tabIndex={1} onKeyDown={handleKeyDown}>
            <Stage
              width={canvasMeasures.width}
              height={canvasMeasures.height}
              onWheel={handleWheel}
              scaleX={stageScale.scale}
              scaleY={stageScale.scale}
              x={stageScale.stageX}
              y={stageScale.stageY}
            >
              <Layer
                onMouseEnter={handleMouseEnter}
                onMouseDown={handleMouseDown}
                onMouseMove={handleMouseMove}
                onMouseUp={handleMouseUp}
              >
                <ImageFromUrl
                  canvasMeasures={canvasMeasures}
                  setMeasure={setMeasure}
                  imageUrl={url}
                  onMouseDown={() => {
                    // deselect when clicked on empty area
                    selectAnnotation(null);
                    selectPolygon(null);
                  }}
                />
              </Layer>
              <Layer
                onMouseEnter={handleMouseEnter}
                onMouseDown={handleMouseDown}
                onMouseMove={handleMouseMove}
                onMouseUp={handleMouseUp}
              >
                {annotationsToDraw.map((annotation, i) => {
                  return (
                    <Annotation
                      key={i}
                      isDrawing={isDrawing}
                      measure={measure}
                      shapeProps={annotation}
                      isSelected={annotation.label_id === selectedId}
                      onSelect={() => {
                        if (!isDrawing) {
                          selectAnnotation(annotation.label_id);
                          selectPolygon(null);
                        }
                      }}
                      onChange={newAttrs => {
                        const rects = annotations.slice();
                        rects[i] = newAttrs;
                        setAnnotations(rects);
                      }}
                    />
                  );
                })}
              </Layer>
              <Layer
                onMouseEnter={handleMouseEnter}
                onMouseDown={handleMouseDown}
                onMouseMove={handleMouseMove}
              >
                {polygonsToDraw.map((polygon, i) => {
                  if (polygon.closed === undefined) {
                    polygon.closed = true;
                  }
                  const isSelected = polygon.label_id === selectedPolygonId;
                  const points = polygon.points.map(function (item) {
                    return item * measure;
                  });
                  return (
                    <Line
                      key={i}
                      points={points}
                      onMouseDown={() => {
                        if (!isDrawing) {
                          selectPolygon(polygon.label_id);
                          selectAnnotation(null);
                        }
                      }}
                      stroke={polygon.color}
                      fill={polygon.color}
                      opacity={isSelected ? 0.8 : 0.4}
                      strokeWidth={5}
                      closed={polygon.closed}
                    />
                  );
                })}
                {polygonsToDraw.map((polygon, i) => {
                  if (polygon.closed === undefined) {
                    polygon.closed = true;
                  }
                  const points = polygon.points.map(function (item) {
                    return item * measure;
                  });
                  return (
                    <Line
                      key={i}
                      points={points}
                      onMouseDown={() => {
                        if (!isDrawing) {
                          selectPolygon(polygon.label_id);
                          selectAnnotation(null);
                        }
                      }}
                      stroke={polygon.color}
                      strokeWidth={2}
                      closed={polygon.closed}
                    />
                  );
                })}
                {coord.map((point, index) => {
                  const width = 6;
                  const x = point[0] * measure - width / 2;
                  const y = point[1] * measure - width / 2;
                  const startPointAttr =
                    index === 0
                      ? {
                        hitStrokeWidth: 12,
                        onMouseOver: handleMouseOverStartPoint,
                        onMouseOut: handleMouseOutStartPoint
                      }
                      : null;
                  return (
                    <Rect
                      key={index}
                      x={x}
                      y={y}
                      width={width}
                      height={width}
                      fill="white"
                      stroke="black"
                      strokeWidth={3}
                      {...startPointAttr}
                    />
                  );
                })}
              </Layer>
            </Stage>
          </div>
        </Content>
        <Sider theme="light">
        <div style={{ width: 200, height: 36, background: "#F5F5F5", textAlign: "center", lineHeight: '36px', fontSize: "16px" }}>Bounding Box</div>
          <List
            itemLayout="horizontal"
            dataSource={annotations}
            renderItem={item => (
              <List.Item>
                <List.Item.Meta
                  title={<div style={{ width: 200, height: 36, marginLeft: 15, marginTop: 5 }}>{item.name}</div>}
                />
              </List.Item>
            )}
          />
          <br />
          <div style={{ width: 200, height: 36, background: "#F5F5F5", textAlign: "center", lineHeight: '36px', fontSize: "16px" }}>Polygon</div>
          <List
            itemLayout="horizontal"
            dataSource={polygons}
            renderItem={item => (
              <List.Item>
                <List.Item.Meta
                  title={<div style={{ width: 200, height: 36, marginLeft: 15, marginTop: 5 }}>{item.name}</div>}
                />
              </List.Item>
            )}
          />
        </Sider>
      </Layout>
      <Footer theme="dark">EZ Label</Footer>
    </Layout>
  );
}
