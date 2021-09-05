/*
Date: 23 April 2021
Author：Pingyi Hu a1805597
Description：The function of bounding box annotation
*/

import React, { useEffect } from "react";
import { Rect, Transformer } from "react-konva";


const Annotation = ({ shapeProps, measure, isDrawing, isSelected, onSelect, onChange }) => {
  const shapeRef = React.useRef();
  const transformRef = React.useRef();

  useEffect(() => {
    if (isSelected) {
      // we need to attach transformer manually
      transformRef.current.setNode(shapeRef.current);
      transformRef.current.getLayer().batchDraw();
    }
  }, [isSelected]);

  const onMouseEnter = event => {
    event.target.getStage().container().style.cursor = "move";
  };

  const onMouseLeave = event => {
    event.target.getStage().container().style.cursor = "crosshair";
  };

  const ColorChanger =(color)=>{
    if (color === "green"){return("rgba(155, 205, 155, 0.5)");}
    else if (color === "red"){return("rgba(255, 0, 0, 0.5)");}
    else if (color === "blue"){return("rgba(0, 0, 255, 0.5)");}
    else if (color === "gray"){return("rgba(156, 156, 156, 0.5)");}
    else if (color === "pink"){return("rgba(255, 192, 203, 0.5)");}
    else if (color === "yellow"){return("rgba(255, 255, 0, 0.5)");}
    else if (color === "purple"){return("rgba(160, 32, 240, 0.5)");}
  };

  return (
    <React.Fragment>

      <Rect
        fill={ColorChanger(shapeProps.color)}
        stroke={shapeProps.color}
        onMouseDown={onSelect}
        ref={shapeRef}
        x={shapeProps.x*measure}
        y={shapeProps.y*measure}
        height={shapeProps.height*measure}
        width={shapeProps.width*measure} 
        draggable={!isDrawing}
        onMouseEnter={onMouseEnter}
        onMouseLeave={onMouseLeave}
        onDragEnd={event => {
          onChange({
            ...shapeProps,
            x: event.target.x()/measure,
            y: event.target.y()/measure
          });
        }}
        onTransformEnd={event => {
          // transformer is changing scale of the node
          // and NOT its width or height
          // but in the store we have only width and height
          // to match the data better we will reset scale on transform end
          const node = shapeRef.current;
          const scaleX = node.scaleX();
          const scaleY = node.scaleY();

          // we will reset it back
          node.scaleX(1);
          node.scaleY(1);
          onChange({
            ...shapeProps,
            x: node.x()/measure,
            y: node.y()/measure,
            // set minimal value
            width: Math.max(5, node.width() * scaleX)/measure,
            height: Math.max(node.height() * scaleY)/measure
          });
        }}
      />

      {isSelected && <Transformer ref={transformRef} />}
      
      

    </React.Fragment>
    
  );
};



export default Annotation;
