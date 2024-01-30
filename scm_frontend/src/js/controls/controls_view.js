import React, { Component, Fragment } from "react";
import axios from "axios";

import { API_URL_CONTROL } from "../../constants";

class ControlsView extends React.Component {
  deleteControl = pk => {
    axios.delete(API_URL_CONTROL + pk).then(() => {
      this.props.resetState();
    });
  };

  editControl = (pk) => {
    this.props.editAsset(pk)
  };

  render() {
    const controls = this.props.controls;
    
    return (
      <div>
        <h2>Controls</h2>
        <div id="btnCreateNewControl"><button onClick={this.props.onClick} class="buttons btnGreen mbutton"> + Add New Control </button></div>
        <table id="tblAssets">
          <thead>
            <tr>
              <th>CN</th>
              <th>Name</th>
              <th>Description</th>
              <th>Parent Control</th>
              <th>Tags</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {!controls || controls.length <= 0 ? (
                  <tr>
                    <td colSpan="6" align="center">
                      <b>Ops, no controls yet</b>
                    </td>
                  </tr>
                ) : (
                  controls.map(control => (
                    <tr>
                      <td>{control.cn}</td>
                      <td>{control.name}</td>
                      <td>{`${control.description.substring(0, 200)}...`}</td>
                      {control.parent_control != null 
                        ? <td>{control.parent_control_name}</td>
                        : <td>None</td>
                      }  
                      <td>
                        {!control.tags || control.tags.length <= 0 ? (
                          <p>No tags assigned</p>
                        ) : (
                          control.tags.map(tag => ( 
                            <span>{tag.name}, </span> ))
                        )}
                      </td>
                      <td><button onClick={() => this.editControl(control.pk)}>Edit</button> <button onClick={() => this.deleteControl(control.pk)}>Delete</button></td>
                    </tr>
                ))
              )}
          </tbody>
        </table>
      </div>
    );
  }
}

export default ControlsView;