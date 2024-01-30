import ControlsView from './controls_view';
import CreateControlView from './create_control_view';
import { API_URL_CONTROLS } from "../../constants";
import { API_URL_CONTROL } from "../../constants";

import * as React from "react";
import axios from "axios";

export default class Control extends React.Component { 
  constructor(props) {
    super(props);
    this.handleCreateControlClick = this.handleCreateControlClick.bind(this);
    this.handleCloseCreateControlClick = this.handleCloseCreateControlClick.bind(this);
    this.state = {isCreateControl: false, controls: []};
  }

  componentDidMount() {
    this.getControls();
  }

  handleCreateControlClick() {
    this.setState({isCreateControl: true});
  }

  handleCloseCreateControlClick() {
    this.setState({isCreateControl: false});
    this.getControls();
  }

  getControls = async () => {   
    let res = await axios.get(API_URL_CONTROLS);
    let control_data = res.data;

    /* for (let i = 0; i < control_data.length; i++) {
      if(control_data[i]["parent_control"] != null) {     
        let parent_control = await this.getParentControl(parseInt(control_data[i]["parent_control"]));
        control_data[i]["parent_control"] = {'pk': parent_control['pk'], 'name': parent_control['name']}

      }
    }*/
    this.setState({ controls: control_data });
  }

  getParentControl = async (pk) => {
    let res = await axios.get(API_URL_CONTROL + pk);
    return res.data
  };

  render() {
    const isCreateControl = this.state.isCreateControl;
    let content;
    if(isCreateControl) {
      content = <CreateControlView onClick={this.handleCloseCreateControlClick}/>;
    } else {
      content = <ControlsView controls={this.state.controls} onClick={this.handleCreateControlClick}/>;
    }

    return (<div>{content}</div>);
  }
}