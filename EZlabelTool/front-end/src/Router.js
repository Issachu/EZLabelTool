import React from 'react';
import { HashRouter, Route, Switch} from 'react-router-dom';

import Signin from './pages/Signin';
import ProjectSetting from './pages/ProjectSetting';
import ProjectDetail from './pages/ProjectDetail';
import DatasetGetImages from './pages/DatasetGetImages';
import EditorSetting from './pages/EditorSetting';
import FramePage from './pages/FramePage';
import Label from './pages/Label';
import Review from './pages/Review';
import LabelView from './pages/LabelView';
import ReviewView from './pages/ReviewView';
import PrivateRoute from "./privateRoute";

const SimpleRoute = () => (
    <HashRouter>
        <Switch>
            <Route  path="/signin" component={Signin}/>           
            <PrivateRoute  path="/home" component={FramePage}/>
            <PrivateRoute  path="/editorSetting" component={EditorSetting}/>
            <PrivateRoute  path="/label" component={Label}/>
            <PrivateRoute  path="/review" component={Review}/>
            <PrivateRoute  path="/labelView" component={LabelView}/>
            <PrivateRoute  path="/reviewView" component={ReviewView}/>
            <PrivateRoute  path="/setting" component={ProjectSetting}/>
            <PrivateRoute  path="/detail" component={ProjectDetail}/> 
            <PrivateRoute  path="/images" component={DatasetGetImages}/>
        </Switch>
    </HashRouter>
);
export default SimpleRoute;