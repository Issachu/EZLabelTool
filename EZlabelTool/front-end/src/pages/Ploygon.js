/*
Date: 23 April 2021
Author：Pingyi Hu a1805597
Description：The function of polygon annotation
*/

import React, { useState, Component } from "react";
import Konva from "konva";
import { render } from "react-dom";
import { Stage, Layer, Group, Line, Rect } from "react-konva";

// const Ploygon = ({shapeProps, isSelected, onSelect}) => {
//   const shapeRef = React.useRef();
//   const [points, setPoints] = useState(shapeProps)
//   const [isMouseOverStartPoint, setIsMouseOverStartPoint] = useState(false);

//   handleMouseOverStartPoint = event => {
//     event.target.scale({ x: 2, y: 2 });
//     setIsMouseOverStartPoint(true);
//   };

//   handleMouseOutStartPoint = event => {
//     event.target.scale({ x: 1, y: 1 });
//     setIsMouseOverStartPoint(false);
//   };

//   return (
//     <React.Fragment>
//       <Line
//         {...shapeProps}
//         stroke="black"
//         strokeWidth={5}
//         draggable
//         closed={isFinished}
//       />
//       {points.map((point, index) => {
//         const width = 6;
//         const x = point[0] - width / 2;
//         const y = point[1] - width / 2;
//         const startPointAttr =
//           index === 0
//             ? {
//                 hitStrokeWidth: 12,
//                 onMouseOver: handleMouseOverStartPoint,
//                 onMouseOut: handleMouseOutStartPoint
//               }
//             : null;
//         return (
//           <Rect
//             key={index}
//             x={x}
//             y={y}
//             width={width}
//             height={width}
//             fill="white"
//             stroke="black"
//             strokeWidth={3}
//             // onDragStart={handleDragStartPoint}
//             // onDragMove={handleDragMovePoint}
//             // onDragEnd={handleDragEndPoint}
//             // draggable
//             {...startPointAttr}
//           />
//         );
//       })}
//     </React.Fragment>
//   );
// };

class Ploygon extends Component {
  state = {
    points: [],
    curMousePos: [0, 0],
    isMouseOverStartPoint: false,
    isFinished: false
  };

  componentDidMount() {
    console.log(window.innerHeight);
  }

  getMousePos = stage => {
    return [stage.getPointerPosition().x, stage.getPointerPosition().y];
  };
  handleClick = event => {
    const {
      state: { points, isMouseOverStartPoint, isFinished },
      getMousePos
    } = this;
    const stage = event.target.getStage();
    const mousePos = getMousePos(stage);

    if (isFinished) {
      return;
    }
    if (isMouseOverStartPoint && points.length >= 3) {
      this.setState({
        isFinished: true
      });
    } else {
      this.setState({
        points: [...points, mousePos]
      });
    }
  };
  handleMouseMove = event => {
    const { getMousePos } = this;
    const stage = event.target.getStage();
    const mousePos = getMousePos(stage);

    this.setState({
      curMousePos: mousePos
    });
  };
  handleMouseOverStartPoint = event => {
    if (this.state.isFinished || this.state.points.length < 3) return;
    event.target.scale({ x: 2, y: 2 });
    this.setState({
      isMouseOverStartPoint: true
    });
  };
  handleMouseOutStartPoint = event => {
    event.target.scale({ x: 1, y: 1 });
    this.setState({
      isMouseOverStartPoint: false
    });
  };
  handleDragStartPoint = event => {
    console.log("start", event);
  };
  handleDragMovePoint = event => {
    const points = this.state.points;
    const index = event.target.index - 1;
    console.log(event.target);
    const pos = [event.target.attrs.x, event.target.attrs.y];
    console.log("move", event);
    console.log(pos);
    this.setState({
      points: [...points.slice(0, index), pos, ...points.slice(index + 1)]
    });
  };
  handleDragOutPoint = event => {
    console.log("end", event);
  };

  render() {
    console.log(this.state);
    const {
      state: { points, isFinished, curMousePos },
      handleClick,
      handleMouseMove,
      handleMouseOverStartPoint,
      handleMouseOutStartPoint,
      handleDragStartPoint,
      handleDragMovePoint,
      handleDragEndPoint
    } = this;
    // [ [a, b], [c, d], ... ] to [ a, b, c, d, ...]
    const flattenedPoints = points
      .concat(isFinished ? [] : curMousePos)
      .reduce((a, b) => a.concat(b), []);
    return (
      <Stage
        width={window.innerWidth}
        height={window.innerHeight}
        onMouseDown={handleClick}
        onMouseMove={handleMouseMove}
      >
        <Layer>
          <Line
            points={flattenedPoints}
            stroke="black"
            strokeWidth={5}
            draggable="true"
            closed={isFinished}
          />
          {points.map((point, index) => {
            const width = 6;
            const x = point[0] - width / 2;
            const y = point[1] - width / 2;
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
                onDragStart={handleDragStartPoint}
                onDragMove={handleDragMovePoint}
                onDragEnd={handleDragEndPoint}
                draggable
                {...startPointAttr}
              />
            );
          })}
        </Layer>
      </Stage>
    );
  }
}

export default Ploygon;