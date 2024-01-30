import React, { Component, Fragment } from "react";
import axios from "axios";

import { API_URL_ASSET } from "../../constants";

class AssetsView extends React.Component {
  deleteAsset = pk => {
    axios.delete(API_URL_ASSET + pk).then(() => {
      this.props.resetState();
    });
  };

  editAsset = (pk) => {
    this.props.editAsset(pk)
  };

  render() {
    const assets = this.props.assets;
    return (
      <div>
        <h2>Assets</h2>
        <div id="btnCreateNewAsset"><button onClick={this.props.onClick} class="buttons btnGreen mbutton"> + Add New Asset </button></div>
        <table id="tblAssets">
          <thead>
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Associated Controls</th>
              <th>Categorie</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {!assets || assets.length <= 0 ? (
                <tr>
                  <td colSpan="4" align="center">
                    <b>Ops, no asset yet</b>
                  </td>
                </tr>
              ) : (
                assets.map(asset => (
                  <tr>
                    <td>{asset.name}</td>
                    <td>{`${asset.description.substring(0, 200)}...`}</td>
                    <td>{asset.control_associations + " Associated Controls"}</td>
                    <td>{asset.assettype.name}</td>
                    <td><button onClick={() => this.editAsset(asset.pk)}>Edit</button> <button onClick={() => this.deleteAsset(asset.pk)}>Delete</button></td>
                  </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    );
  }
}

export default AssetsView;