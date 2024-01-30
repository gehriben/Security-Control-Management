
import React, { Component, Fragment } from "react";
import axios from "axios";

import { API_URL_CONTROL } from "../../constants";

class Modal extends React.Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {

  }
  
  render() {
    return (
      <div id="modal" class="modal">
        <div class="modal-content">
          <button class="btn" onClick={this.props.closeModal}><span class="close">&times;</span></button>
          <div>{this.props.content}</div>
        </div>
      </div>
    );
  }
}

export default Modal;