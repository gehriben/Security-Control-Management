import ConstraintView from './constraint_view';
import CreateConstraintView from './create_constraint_view';

import * as React from "react";

export default class Constraints extends React.Component { 
  constructor(props) {
    super(props);
    this.handleCreateConstraintClick = this.handleCreateConstraintClick.bind(this);
    this.handleCloseCreateConstraintClick = this.handleCloseCreateConstraintClick.bind(this);
    this.state = {isCreateConstraint: false};
  }

  handleCreateConstraintClick() {
    this.setState({isCreateConstraint: true});
  }

  handleCloseCreateConstraintClick() {
    this.setState({isCreateConstraint: false});
  }

  render() {
    const isCreateConstraint = this.state.isCreateConstraint;
    let content;
    if(isCreateConstraint) {
      content = <CreateConstraintView onClick={this.handleCloseCreateConstraintClick}/>;
    } else {
      content = <ConstraintView onClick={this.handleCreateConstraintClick}/>;
    }

    return (<div>{content}</div>);
  }
}