import AssetsView from './assets_view';
import CreateAssetView from './create_asset_view';
import { API_URL_ASSETS, API_URL_MATCHING_CONTROLS_WITH_ASSET } from "../../constants";


import * as React from "react";
import axios from "axios";

export default class Assets extends React.Component { 
  constructor(props) {
    super(props);
    this.handleCreateAssetClick = this.handleCreateAssetClick.bind(this);
    this.handleCloseCreateAssetClick = this.handleCloseCreateAssetClick.bind(this);
    this.state = {isCreateAsset: false, assets: [], pk: null};
  }

  componentDidMount() {
    this.resetState();
  }

  handleCreateAssetClick() {
    this.setState({isCreateAsset: true});
  }

  handleCloseCreateAssetClick() {
    this.setState({isCreateAsset: false});
    this.resetState()
  }

  getAssets = () => {
    axios.get(API_URL_ASSETS).then(res => {
      let asset_data = res.data
      console.log(asset_data);
      console.log(asset_data["pk"]);
      for(let asset_index=0; asset_index < asset_data.length; asset_index++) {
        asset_data[asset_index]["control_associations"] = 0;
        axios.get(API_URL_MATCHING_CONTROLS_WITH_ASSET + asset_data[asset_index].pk).then(res_control_matches => {
          let contorl_matches = res_control_matches.data
          let control_associations = 0
          for(let i=0; i < contorl_matches.length; i++) {
            control_associations += 1
            control_associations += contorl_matches[i]["child_controls"].length;
          }
          asset_data[asset_index]["control_associations"] = control_associations
          console.log(asset_data);
          this.setState({ assets: asset_data })
        });
      }
    });
  };

  resetState = () => {
    this.setState({isCreateAsset: false});
    this.setState({pk: null})
    this.getAssets();
  };

  editAsset = (pk) => {
    this.setState({isCreateAsset: true});
    this.state.pk = pk
  }

  render() {
    const isCreateAsset = this.state.isCreateAsset;
    let content;
    if(isCreateAsset) {
      content = <CreateAssetView pk={this.state.pk} resetState={this.resetState} onClick={this.handleCloseCreateAssetClick}/>;
    } else {
      content = <AssetsView assets={this.state.assets} resetState={this.resetState} editAsset={this.editAsset} onClick={this.handleCreateAssetClick}/>;
    }

    return (<div>{content}</div>);
  }
}