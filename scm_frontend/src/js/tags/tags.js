import TagsView from './tags_view';
import CreateTagView from './create_tag_view';
import { API_URL_TAGS } from "../../constants";

import * as React from "react";
import axios from "axios";

export default class Tags extends React.Component { 
  constructor(props) {
    super(props);
    this.handleCreateTagClick = this.handleCreateTagClick.bind(this);
    this.handleCloseCreateTagClick = this.handleCloseCreateTagClick.bind(this);
    this.setData = this.setData.bind(this);
    this.state = {isCreateTag: false, tags: []};

    this.setData();
  }

  handleCreateTagClick() {
    this.setState({isCreateTag: true});
  }

  handleCloseCreateTagClick() {
    this.setState({isCreateTag: false});
    this.setData();
  }

  setData = () => {
    axios.get(API_URL_TAGS).then(res => this.setState({ tags: res.data }));
  };

  editTag = (pk) => {
    this.setState({isCreateTag: true});
    this.state.pk = pk
  }

  render() {
    const isCreateTag = this.state.isCreateTag;
    let content;
    if(isCreateTag) {
      content = <CreateTagView pk={this.state.pk} onClick={this.handleCloseCreateTagClick}/>;
    } else {
      content = <TagsView tags={this.state.tags} setData={this.setData} editTag={this.editTag} onClick={this.handleCreateTagClick}/>;
    }

    return (<div>{content}</div>);
  }
}