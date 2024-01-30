import 'bootstrap/dist/css/bootstrap.css';
import React from "react";
import axios from "axios";

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Badge from 'react-bootstrap/Badge';
import ListGroup from 'react-bootstrap/ListGroup';
import Button from 'react-bootstrap/Button';

import Modal from '../_general/modal';
import { API_URL_PROPERTIES } from "../../constants";
import { API_URL_PROPERTY } from "../../constants";

class CreatePropertyView extends React.Component {
    constructor(props) {
        super(props);
        this.state = { 
          property: {
              pk: -1,
              name: "",
              description: "",
              parent_property: null,
              parent_property_name: ""
          },
          properties: []
        };
      }
    
    componentDidMount() {
      this.setData();
    }

    setData() {
        if (this.props.pk) {
            axios.get(API_URL_PROPERTY + this.props.pk).then(res => {
                const { pk, name, description, parent_property, parent_property_name }  = res.data;
                this.setState({property: { pk, name, description, parent_property, parent_property_name } });
            });
        }

        axios.get(API_URL_PROPERTIES).then(res => this.setState({ properties: res.data }));
    }
    
    onChange = e => {
        this.setState(prevState => {
            let property = Object.assign({}, prevState.property);
            property[e.target.name] = e.target.value;          
                                                
            return { property };                                 
          }); 
    };

    saveProperty = () => {
        if (!this.props.pk) {
            axios.post(API_URL_PROPERTIES, this.state.property).then(() => {
                this.props.onClick();
            });
        } else {
            axios.put(API_URL_PROPERTY + this.state.property.pk + "/", this.state.property).then(() => {
              this.props.onClick();
            });
        }
      };

    defaultIfEmpty = value => {
        return value === "" ? "" : value;
    };

    render() {
        return(
            <div>
                <h2>
                  {this.props.pk < 0 && <span>Edit Property</span>} 
                  {this.props.pk > 0 && <span>Add new Property</span>} 
                </h2>
                <Container fluid>
                  <Row xs sm="2"><label for="txtPropertyName">Property Name</label></Row>
                  <Row xs sm="2"><input type="text" name="name" id="txtPropertyName" class="txt" onChange={this.onChange} value={this.defaultIfEmpty(this.state.property.name)}></input></Row>
                  <Row xs sm="2"><label for="txtPropertyDescription">Description</label></Row>
                  <Row xs sm="2"><textarea  id="txtPropertyDescription" name="description" class="txt" rows="8" onChange={this.onChange} value={this.defaultIfEmpty(this.state.property.description)}></textarea ></Row>
                  <Row xs sm="2"><label for="selParentProperty">Parent Property</label></Row>
                  <Row xs sm="2">
                      <select id="selParentProperty" name="parent_property" class="txt" onChange={this.onChange} value={this.defaultIfEmpty(this.state.property.parent_property)}>
                        <option value={null}>None</option>
                        {this.state.properties.map(property => (
                            <option value={property.pk}>{property.name}</option>
                        ))}
                      </select>
                  </Row>
                  <Row xs sm="4">
                      <Col><button class="buttons btnGreen" onClick={() => this.saveProperty()}>Save</button></Col>
                      <Col><button onClick={this.props.onClick} class="buttons btnRed">Cancel</button></Col>
                  </Row>
                </Container>
            </div>
        );
    }
}

export default CreatePropertyView;