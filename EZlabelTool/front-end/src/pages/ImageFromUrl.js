/*
Date: 23 April 2021
Author：Pingyi Hu a1805597
Description：The function of put image from url on canvas
*/
import React, { useState, useEffect } from "react";
import { Image } from "react-konva";

const ImageFromUrl = ({
  imageUrl,
  canvasMeasures,
  setMeasure,
  onMouseDown,
  onMouseUp,
  onMouseMove
}) => {
  const [image, setImage] = useState(null);
  const [imageMeasures, setImageMeasures] = useState({
    width: 0,
    height: 0
  });

  useEffect(() => {
    const imageToLoad = new window.Image();
    imageToLoad.src = imageUrl;
    imageToLoad.addEventListener("load", () => {
      setImage(imageToLoad);
      if (imageToLoad.width/imageToLoad.height > canvasMeasures.width/canvasMeasures.height){
        setMeasure(canvasMeasures.width/imageToLoad.width)
        setImageMeasures({
          width: canvasMeasures.width,
          height: imageToLoad.height*(canvasMeasures.width/imageToLoad.width)
        });
      } else {
        setMeasure(canvasMeasures.height/imageToLoad.height)
        setImageMeasures({
          width: imageToLoad.width*(canvasMeasures.height/imageToLoad.height),
          height: canvasMeasures.height,
        });
      }
      
    });

    return () => imageToLoad.removeEventListener("load",[]);
  }, [imageUrl, setImage, canvasMeasures, setMeasure]);

  return (
    <Image
      image={image}
      onMouseDown={onMouseDown}
      onMouseMove={onMouseMove}
      onMouseUp={onMouseUp}
      height={imageMeasures.height}
      width={imageMeasures.width}
    />
  );
};

export default ImageFromUrl;
