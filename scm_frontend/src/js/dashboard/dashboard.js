import * as React from "react";
import axios from "axios";

import 'bootstrap/dist/css/bootstrap.css';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';

import { API_URL_IMPORT_CONTROLS, API_URL_ANALYSE_CONTROLS, API_URL_MATCH_CONTROLS, 
  API_URL_TAGS, API_URL_KEYWORDS, API_URL_PROPERTY_TAGS, API_URL_METRICS, API_URL_CONTROLS, 
  API_URL_ASSETS, API_URL_IMPORT_ASSETS, API_URL_ASSET_CONTROL_MATCHES, API_URL_PROPERTIES, 
  API_URL_MATCHING_CONTROLS_WITH_ASSETS, API_URL_CREATE_GRAPHS, API_URL_TFIDF_MATCHING } from "../../constants";

export default class Dashboard extends React.Component { 
  constructor(props) {
    super(props);
    this.state = {controls: []};
  }

  componentDidMount() {
    this.get_matching_results();
  }

  get_matching_results() {
    axios.get(API_URL_MATCHING_CONTROLS_WITH_ASSETS).then(res => this.setState({ controls: res.data }) );
  }

  importControls() {
    axios.post(API_URL_IMPORT_CONTROLS).then( alert("Controls imported!") );
  }

  importAssets() {
    axios.post(API_URL_IMPORT_ASSETS).then( alert("Assets imported!") );
  }

  analyseControls() {
    axios.post(API_URL_ANALYSE_CONTROLS).then( alert("Controls analysis started!") );
  }

  matchControls() {
    axios.post(API_URL_MATCH_CONTROLS).then( () => {
      alert("Controls matched!");
      this.get_matching_results();
    });
  }

  tfidfMatching() {
    axios.post(API_URL_TFIDF_MATCHING).then( () => {
      alert("TFIDF Matching done!");
      this.get_matching_results();
    });
  }

  createGraphs() {
    axios.post(API_URL_CREATE_GRAPHS).then( () => {
      alert("Graphs created!");
    });
  }

  deleteAnalyticData() {
    axios.delete(API_URL_TAGS)
    axios.delete(API_URL_KEYWORDS)
    axios.delete(API_URL_PROPERTY_TAGS)
    axios.delete(API_URL_METRICS)
    
    alert("Analytic data deleted!");
  }

  deleteControls() {
    axios.delete(API_URL_CONTROLS).then(alert("Controls deleted!"));
  }

  deleteAssets() {
    axios.delete(API_URL_ASSETS);
    axios.delete(API_URL_PROPERTIES);

    alert("Assets deleted!")
  }

  deleteMatchingResults() {
    axios.delete(API_URL_ASSET_CONTROL_MATCHES).then(() => {
      alert("Matching results deleted!");
      this.get_matching_results();
    });
  }


  render() {
      return (
        <div>
          <h2>Dashboard</h2>
          <Container fluid>
            <Row xs sm="4"><button class="buttons btnGreen" onClick={() => this.importControls()}>Import Controls</button></Row>
            <Row xs sm="4"><p></p></Row>
            <Row xs sm="4"><button class="buttons btnGreen" onClick={() => this.importAssets()}>Import Assets</button></Row>
            <Row xs sm="4"><p></p></Row>
            <Row xs sm="4"><button class="buttons btnGreen" onClick={() => this.analyseControls()}>Analyse Assets & Controls</button></Row>
            <Row xs sm="4"><p></p></Row>
            <Row xs sm="4"><button class="buttons btnGreen" onClick={() => this.matchControls()}>Match controls</button></Row>
            <Row xs sm="4"><p></p></Row>
            <Row xs sm="4"><button class="buttons btnGreen" onClick={() => this.tfidfMatching()}>TFIDF Matching</button></Row>
            <Row xs sm="4"><p></p></Row>
            <Row xs sm="4"><button class="buttons btnGreen" onClick={() => this.createGraphs()}>Create graphs</button></Row>
            <Row xs sm="4"><p></p></Row>
            <Row xs sm="4"><button class="buttons btnRed" onClick={() => this.deleteControls()}>Delete Controls</button></Row>
            <Row xs sm="4"><p></p></Row>
            <Row xs sm="4"><button class="buttons btnRed" onClick={() => this.deleteAssets()}>Delete Assets</button></Row>
            <Row xs sm="4"><p></p></Row>
            <Row xs sm="4"><button class="buttons btnRed" onClick={() => this.deleteAnalyticData()}>Delete analytic data</button></Row>
            <Row xs sm="4"><p></p></Row>
            <Row xs sm="4"><button class="buttons btnRed" onClick={() => this.deleteMatchingResults()}>Delete Matching Results</button></Row>
            <Row xs sm="4"><p></p></Row>
          </Container>
          <h3>Recommended Controls</h3>
            {this.state.controls.length > 0 && 
              <>
                <span>Count: {this.state.controls[0].control_count}</span>
                <br />
              </>
            }
            {!this.state.controls || this.state.controls.length <= 0 ? (
                  <tr>
                    <td colSpan="6" align="center">
                      <b>Ops, no controls yet</b>
                    </td>
                  </tr>
                ) : (
                  this.state.controls.map(control => (
                    <>
                      <br />
                      <h4>{control.name}</h4>
                      <table id="tblAssets">
                      <thead>
                        <tr>
                          <th>CN</th>
                          <th>Name</th>
                          <th>Description</th>
                          <th>Assets concerned</th>
                        </tr>
                      </thead>
                      <tbody class="highlightedRow">
                        <tr>
                          <td>{control.cn}</td>
                          <td>{control.name}</td>
                          <td>{`${control.description.substring(0, 200)}...`}</td>
                          <td>
                            {control.concerend_assets.map(concerend_asset => (<span>{concerend_asset.name}, </span> ))}
                          </td> 
                        </tr>
                        {control.child_controls.map(child_control => (
                          <tr>
                           <td>{child_control.cn}</td>
                           <td>{child_control.name}</td>
                           <td>{`${child_control.description.substring(0, 200)}...`}</td>
                           <td>
                            {control.concerend_assets.map(concerend_asset => (<span>{concerend_asset.name}, </span> ))}
                          </td>  
                         </tr>
                        ))
                        }
                      </tbody>
                    </table>
                  </>
                ))
              )}
        </div>
      );
    }
  } 