
import React, { Component, Fragment } from "react";
import axios from "axios";

import { API_URL_TAG } from "../../constants";

class TagsView extends React.Component {
  deleteTag = pk => {
    axios.delete(API_URL_TAG + pk).then(() => {
      this.props.setData();
    });
  };

  editTag = (pk) => {
    this.props.editTag(pk);
  };
  
  render() {
    const tags = this.props.tags;
    for (let i = 0; i < tags.length; i++) {
      let tag = tags[i];
      let keyword_string = "";
      for (let j = 0; j < tag.keywords.length; j++) {
        let keyword = tag.keywords[j];
        if(j < tag.keywords.length - 1){
          keyword_string = keyword_string + keyword.name + ", ";
        } else {
          keyword_string = keyword_string + keyword.name;
        }
      }

      if (keyword_string.length > 200) {
        keyword_string = keyword_string.substring(0, 200) + "...";
      }
      tags[i]["keyword_string"] = keyword_string;
    }

    return (
      <div>
        <h2>Tags</h2>
        <div id="btnCreateNewTag"><button onClick={this.props.onClick} class="buttons btnGreen mbutton"> + Add New Tag </button></div>
        <table id="tblAssets">
          <thead>
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Keywords</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {!tags || tags.length <= 0 ? (
                  <tr>
                    <td colSpan="4" align="center">
                      <b>Ops, no tag yet</b>
                    </td>
                  </tr>
                ) : (
                  tags.map(tag => (
                    <tr>
                      <td>{tag.name}</td>
                      <td>{tag.description}</td>
                      <td>{tag.keyword_string}</td>
                      <td><button onClick={() => this.editTag(tag.pk)}>Edit</button> <button onClick={() => this.deleteTag(tag.pk)}>Delete</button></td>
                    </tr>
                ))
              )}
          </tbody>
        </table>
      </div>
    );
  }
}

export default TagsView;