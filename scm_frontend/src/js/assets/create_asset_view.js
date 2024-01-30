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
import { API_URL_ASSETS, API_URL_ASSET, API_URL_ASSETTYPES, API_URL_TAGS, API_URL_TAG, 
    API_URL_PROPERTIES, API_URL_PROPERTY, API_URL_CONSTRAINT_FOR_ASSET, API_URL_CONSTRAINTS, 
    API_URL_CONSTRAINT, API_URL_CONSTRAINT_ASSOCIATION, API_URL_MATCHING_CONTROLS_WITH_ASSET } from "../../constants";

class CreateAssetView extends React.Component {
    constructor(props) {
        super(props);
        this.closeModal = this.closeModal.bind(this);
        this.addTag = this.addTag.bind(this);
        this.removeTag = this.removeTag.bind(this);
        this.addProperty = this.addProperty.bind(this);
        this.removeProperty = this.removeProperty.bind(this);
        this.addConstraint = this.addConstraint.bind(this);
        this.removeConstraint = this.removeConstraint.bind(this);

        this.state = { 
            asset: {
                pk: null,
                name: "",
                description: "",
                assettype: {
                    pk: "",
                    name: ""
                },
                tags: [],
                properties: []
            },
            assettypes: [],
            constraintAssociations: [],
            control_matches: [],
            modal: ""
        };
      }
    
    componentDidMount() {
        this.setData();
        this.getAssettypes();
    }

    setData() {
        if (this.props.pk != null) {
            this.setAssetData(this.props.pk);
            this.setConstraintData(this.props.pk);
            this.setControlMatchData(this.props.pk);
        }
    }

    setAssetData(pk) {      
        axios.get(API_URL_ASSET + pk).then(res => {
            const { pk, name, description, assettype, tags, properties }  = res.data;
            this.setState({asset: { pk, name, description, assettype, tags, properties } });
        });
    }

    setConstraintData(pk) {
        axios.get(API_URL_CONSTRAINT_FOR_ASSET + pk).then(res => {
            this.setState({constraintAssociations: res.data});
        });
    }

    setControlMatchData(pk) {
        axios.get(API_URL_MATCHING_CONTROLS_WITH_ASSET + pk).then(res => {
            this.setState({control_matches: res.data});
        });
    }

    getAssettypes = () => {
        axios.get(API_URL_ASSETTYPES).then(res => {
            this.setState({ assettypes: res.data });
            if (this.props.pk == null) {
                let asset = this.state.asset;
                asset.assettype.pk = res.data[0]["pk"];
                asset.assettype.name = res.data[0]["name"];

                this.setState({ asset: asset });
            }  
        } );
    };
    
    onChange = e => {
        this.setState(prevState => {
            let asset = Object.assign({}, prevState.asset);
            if(e.target.name == "assettype") {
                asset.assettype.pk = e.target.value;
                asset.assettype.name = "None";
            } else {
                asset[e.target.name] = e.target.value;
            }                   
                                                
            return { asset };                                 
          }); 
    };

    saveAsset = () => {
        if (this.props.pk == null) {
            axios.post(API_URL_ASSETS, this.state.asset).then(() => {
                this.props.resetState();
            });
        } else {
            axios.put(API_URL_ASSET + this.state.asset.pk + "/", this.state.asset).then(() => {
                this.props.resetState();
            });
        }
      };

    addTag = (pk) => {
        axios.get(API_URL_TAG + pk).then(res => {
            let asset_data = this.state.asset;
            asset_data.tags.push(res.data);

            this.setState({ asset: asset_data })
        });
    }

    removeTag = async (pk) => {
        let asset_data = this.state.asset;
        for(let i=0; i < asset_data.tags.length; i++){
            if (pk == asset_data.tags[i].pk) {
                asset_data.tags.splice(i, 1);
            }
        }
        await this.setState({ asset: asset_data })
    }

    addProperty = (pk) => {
        axios.get(API_URL_PROPERTY + pk).then(res => {
            let asset_data = this.state.asset;
            console.log(asset_data);
            asset_data.properties.push(res.data);

            this.setState({ asset: asset_data })
        });
    }

    removeProperty = async (pk) => {
        let asset_data = this.state.asset;
        for(let i=0; i < asset_data.properties.length; i++){
            if (pk == asset_data.properties[i].pk) {
                asset_data.properties.splice(i, 1);
            }
        }
        await this.setState({ asset: asset_data })
    }

    addConstraint = (pk, value) => {
        axios.get(API_URL_CONSTRAINT + pk).then(res => {
            let constraintAssociation = {
                name: res.data["name"] + "_" + value + "_" + this.state.asset.name,
                constraint: res.data,
                selected_value: {"value": value},
                asset: this.state.asset,
                control: null
            }
            
            this.saveConstraint(constraintAssociation);
        });
    }

    saveConstraint = (constraintAssociation) => {
        axios.post(API_URL_CONSTRAINT_FOR_ASSET + this.props.pk + "/", constraintAssociation).then(() => { this.setConstraintData(this.props.pk); }); 
    };

    removeConstraint = async (pk) => {
        axios.delete(API_URL_CONSTRAINT_ASSOCIATION + pk).then(() => {
            this.setConstraintData(this.props.pk);
        });
    }

    defaultIfEmpty = value => {
        return value === "" ? "" : value;
    };

    openTagModal() {
        axios.get(API_URL_TAGS).then(res => {
            this.setState({modal: <Modal closeModal={this.closeModal} content={<ModalContent type="Tag" data={res.data} add={this.addTag} closeModal={this.closeModal}  />} />})
        });
    }

    openPropertyModal() {
        axios.get(API_URL_PROPERTIES).then(res => {
            this.setState({modal: <Modal closeModal={this.closeModal} content={<ModalContent type="Property" data={res.data} add={this.addProperty} closeModal={this.closeModal}  />} />})
        });
    }

    openConstraintModal() {
        axios.get(API_URL_CONSTRAINTS).then(res => {
            this.setState({modal: <Modal closeModal={this.closeModal} content={<ConstraintModalContent type="Constraint" data={res.data} add={this.addConstraint} closeModal={this.closeModal}  />} />})
        });
    }

    closeModal() {
        this.setState({modal: ""})
    }

    render() {
        const assettypes = this.state.assettypes;
        const asset = this.state.asset;

        return(
            <div>
                {this.state.modal}
                <h2>Add new Asset</h2>
                <Container fluid>
                    <Row xs sm="2"><label for="txtAssetName">Asset Name</label></Row>
                    <Row xs sm="2"><input type="text" name="name" id="txtAssetName" class="txt" onChange={this.onChange} value={this.defaultIfEmpty(this.state.asset.name)}></input></Row>
                    <Row xs sm="2"><label for="selAssetCategory">Asset Category</label></Row>
                    <Row xs sm="2">
                        <select id="selAssetCategory" name="assettype" class="txt" onChange={this.onChange} value={this.defaultIfEmpty(this.state.asset.assettype.pk)}>
                            {assettypes.map(assettype => (
                                <option value={assettype.pk}>{assettype.name}</option>
                            ))}
                        </select>
                    </Row>
                    <Row xs sm="2"><label for="txtAssetDescription">Description</label></Row>
                    <Row xs sm="2"><textarea  id="txtAssetDescription" name="description" class="txt" rows="4" onChange={this.onChange} value={this.defaultIfEmpty(this.state.asset.description)}></textarea ></Row>
                    { this.props.pk != null &&
                    <>
                        <Row xs sm="2"><label>Constraints</label></Row>
                        <Row xs sm="4"><Button variant="secondary" id="btnAddConstraint" onClick={() => this.openConstraintModal()}>Add Constraint</Button>{' '}</Row>
                        <Row xs sm="2">
                            <ListGroup as="ol" numbered>
                                {!this.state.constraintAssociations || this.state.constraintAssociations.length <= 0 ? (
                                    <div className="ms-2 me-auto">
                                        <div className="fw-bold">No constraints assigned</div>
                                    </div>
                                    ) : (
                                        this.state.constraintAssociations.map(constraintAssociation => ( 
                                        <ListGroup.Item as="li" className="d-flex justify-content-between align-items-start">
                                            <ListElement type="Tag" titel={constraintAssociation.constraint.name+" | "+constraintAssociation.selected_value["value"]} pk={constraintAssociation.pk} remove={this.removeConstraint}/>
                                        </ListGroup.Item>
                                            ))
                                    )}
                            </ListGroup>
                        </Row>
                    </> 
                    }
                    <Row xs sm="2"><br /></Row>
                    <Row xs sm="2"><label>Tags</label></Row>
                    <Row xs sm="4"><Button variant="secondary" id="btnAddTag" onClick={() => this.openTagModal()}>Add Tag</Button>{' '}</Row>
                    <Row xs sm="2">
                        <ListGroup as="ol" numbered>
                            {!this.state.asset.tags || this.state.asset.tags.length <= 0 ? (
                                <div className="ms-2 me-auto">
                                    <div className="fw-bold">No tags assigned</div>
                                </div>
                                ) : (
                                    asset.tags.map(tag => ( 
                                    <ListGroup.Item as="li" className="d-flex justify-content-between align-items-start">
                                        <ListElement type="Tag" titel={tag.name} pk={tag.pk} remove={this.removeTag}/>
                                    </ListGroup.Item>
                                        ))
                                )}
                        </ListGroup>
                    </Row>
                    <Row xs sm="2"><br /></Row>
                    <Row xs sm="2"><label>Properties</label></Row>
                    <Row xs sm="4"><Button variant="secondary" id="btnAddProperty" onClick={() => this.openPropertyModal()}>Add Property</Button>{' '}</Row>
                    <Row xs sm="2">
                        <ListGroup as="ol" numbered>
                            {!this.state.asset.properties || this.state.asset.properties.length <= 0 ? (
                                <div className="ms-2 me-auto">
                                    <div className="fw-bold">No properties assigned</div>
                                </div>
                                ) : (
                                    asset.properties.map(property => ( 
                                    <ListGroup.Item as="li" className="d-flex justify-content-between align-items-start">
                                        <ListElement type="Property" titel={property.name} pk={property.pk} remove={this.removeProperty}/>
                                    </ListGroup.Item>
                                        ))
                                )}
                        </ListGroup>
                    </Row>
                    <Row xs sm="2"><br /></Row>
                    <Row xs sm="2"><label>Associated Controls</label></Row>
                    <Row xs sm="2">
                        <ListGroup as="ol" numbered>
                            {!this.state.control_matches || this.state.control_matches.length <= 0 ? (
                                <div className="ms-2 me-auto">
                                    <div className="fw-bold">No controls matched</div>
                                </div>
                                ) : (
                                    this.state.control_matches.map(control_match => ( 
                                    <ListGroup.Item as="li" className="d-flex justify-content-between align-items-start">
                                        <div className="ms-2 me-auto">
                                            <span className="fw-bold">{control_match.name}</span>
                                            { control_match.child_controls.map(child_control => (
                                                <ListGroup.Item as="li" className="d-flex justify-content-between align-items-start">
                                                    <div className="ms-2 me-auto">{child_control.name}</div>
                                                </ListGroup.Item>
                                            )) }
                                        </div>
                                    </ListGroup.Item>
                                        ))
                                )}
                        </ListGroup>
                    </Row>
                    <Row xs sm="4">
                        <Col><button class="buttons btnGreen" onClick={() => this.saveAsset()}>Save</button></Col>
                        <Col><button onClick={this.props.onClick} class="buttons btnRed">Cancel</button></Col>
                    </Row>
                </Container>
            </div>
        );
    }
}

class ListElement extends React.Component {
    constructor(props) {
        super(props);
      }

    render() {
        return(
            <div className="ms-2 me-auto">
                <table>
                    <tbody>
                        <tr>
                            <td className="fw-bold">{this.props.titel}</td>
                            <td><button class="btn" onClick={() => this.props.remove(this.props.pk)}><i class="fa fa-trash" aria-hidden="true"></i></button></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        );
    }

}

class ModalContent extends React.Component {
    constructor(props) {
        super(props);
        this.state = { data: [], pk: 0 };
        
      }
    
    componentDidMount() {
        this.setData();
    }

    setData() {
        this.setState({ data: this.props.data });
    }

    onChange = (e) => {
        this.setState({pk: e.target.value}); 
    };

    confirm() {
        this.props.add(this.state.pk);
        this.props.closeModal();
    }

    render() {
        return(
            <>
                <h2>Add {this.props.type}</h2>
                <Container fluid>
                    <Row xs sm="1">
                        <select id="selElement" name="selElement" class="txt" onChange={this.onChange}>
                            {this.state.data.map(element => (
                                <option value={element.pk}>{element.name}</option>
                            ))}
                        </select>
                    </Row>
                    <Row xs sm="1">
                        <Col><button class="buttons btnGreen" onClick={() => this.confirm()}>Confirm</button></Col>
                    </Row>
                </Container>
            </>
        );
    }

}

class ConstraintModalContent extends React.Component {
    constructor(props) {
        super(props);
        this.state = { data: [], values: [], selected_value: [], pk: 0 };
        
      }
    
    componentDidMount() {
        this.setData();
    }

    async setData() {
        await this.setState({ data: this.props.data });
        await this.setValueField(this.props.data[0]["pk"]);
        await this.setState({pk: this.props.data[0]["pk"]})
    }

    onChangeElement = (e) => {
        this.setValueField(e.target.value);
        this.setState({pk: e.target.value})
    };

    onChangeValue = (e) => {
        this.setState({selected_value: e.target.value})

    };

    setValueField = (pk) => {
        for(let i=0; i<this.state.data.length; i++) {
            if(this.state.data[i]["pk"] == pk) {
                if(this.state.data[i]["constraint_type"]["name"] == "String") {
                    this.setState({values: { "type":"String", "values": this.state.data[i]["values"]["values"] } });
                    this.setState({selected_value: this.state.data[i]["values"]["values"][0]});
                }
                else if(this.state.data[i]["constraint_type"]["name"] == "Integer") {
                    this.setState({values: { "type":"Integer", "values": this.state.data[i]["values"] } });
                    this.setState({selected_value: 0})
                }
            }
        }
    }

    confirm() {
        this.props.add(this.state.pk, this.state.selected_value);
        this.props.closeModal();
    }

    render() {
        let value_field = ""
        if (this.state.values.type == "String") {
            value_field = (
                <select id="selValue" name="selValue" class="txt" onChange={this.onChangeValue}>
                    {this.state.values.values.map(value => (
                        <option value={value}>{value}</option>
                    ))}
                </select>
            );
        } else if (this.state.values.type == "Integer") {
            value_field = (<input type="number" id="selValue" name="selValue" min={this.state.values["min"]} max={this.state.values["max"]} onChange={this.onChangeValue}></input>)
        }

        return(
            <>
                <h2>Add {this.props.type}</h2>
                <Container fluid>
                    <Row xs sm="1">
                        <select id="selElement" name="selElement" class="txt" onChange={this.onChangeElement}>
                            {this.state.data.map(element => (
                                <option value={element.pk}>{element.name}</option>
                            ))}
                        </select>
                    </Row>
                    <Row xs sm="1">
                        {value_field}
                    </Row>
                    <Row xs sm="1">
                        <Col><button class="buttons btnGreen" onClick={() => this.confirm()}>Confirm</button></Col>
                    </Row>
                </Container>
            </>
        );
    }

}

export default CreateAssetView;

