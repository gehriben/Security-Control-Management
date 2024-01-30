import PropertyView from './property_view';
import CreatePropertyView from './create_property_view';
import { API_URL_PROPERTIES } from "../../constants";
import { API_URL_PROPERTY } from "../../constants";

import * as React from "react";
import axios from "axios";


export default class Properties extends React.Component { 
  constructor(props) {
    super(props);

    this.handleCreatePropertyClick = this.handleCreatePropertyClick.bind(this);
    this.handleCloseCreatePropertyClick = this.handleCloseCreatePropertyClick.bind(this);
    this.setData = this.setData.bind(this);
    this.editProperty = this.editProperty.bind(this);

    this.state = {isCreateProperty: false, properties: [], pk: null};

    this.setData();
  }

  handleCreatePropertyClick() {
    this.setState({isCreateProperty: true});
  }

  handleCloseCreatePropertyClick() {
    this.setState({isCreateProperty: false});

    this.setData();
    this.setState({pk: null});
  }

  setData = () => {
    axios.get(API_URL_PROPERTIES).then(res => this.setState({ properties: res.data }));
  };

  getParentProperty = (pk) => {
    return axios.get(API_URL_PROPERTY + pk).then(res => {return res.data });
  };

  editProperty = (pk) => {
    this.setState({isCreateProperty: true, pk: pk});
  }

  render() {
    const isCreateProperty = this.state.isCreateProperty;
    let content;
    if(isCreateProperty) {
      content = <CreatePropertyView pk={this.state.pk} onClick={this.handleCloseCreatePropertyClick}/>;
    } else {
      content = <PropertyView properties={this.state.properties} setData={this.setData} editProperty={this.editProperty} onClick={this.handleCreatePropertyClick}/>;
    }

    return (<div>{content}</div>);
  }
}