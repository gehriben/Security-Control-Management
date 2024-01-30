import React, { Component, Fragment } from "react";
import axios from "axios";

import { API_URL_PROPERTY } from "../../constants";

class PropertyView extends React.Component {
  deleteProperty = pk => {
    axios.delete(API_URL_PROPERTY + pk).then(() => {
      this.props.setData();
    });
  };

  render() {
    const properties = this.props.properties;
    return (
      <div>
        <h2>Properties</h2>
        <div id="btnCreateNewProperty"><button onClick={this.props.onClick} class="buttons btnGreen mbutton"> + Add New Property </button></div>
        <table id="tblAssets">
          <thead>
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Parent Property</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {!properties || properties.length <= 0 ? (
                  <tr>
                    <td colSpan="4" align="center">
                      <b>Ops, no property yet</b>
                    </td>
                  </tr>
                ) : (
                  properties.map(property => (
                    <tr>
                      <td>{property.name}</td>
                      <td>{property.description}</td>
                      {property.parent_property != null 
                        ? <td>{property.parent_property_name}</td>
                        : <td>None</td>
                      }
                      <td><button onClick={() => this.props.editProperty(property.pk)}>Edit</button> <button onClick={() => this.deleteProperty(property.pk)}>Delete</button></td>
                    </tr>
                ))
              )}
          </tbody>
        </table>
      </div>
    );
  }
}

export default PropertyView;