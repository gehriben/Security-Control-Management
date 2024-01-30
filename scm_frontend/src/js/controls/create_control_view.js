import React from "react";
import axios from "axios";

import 'bootstrap/dist/css/bootstrap.css';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Badge from 'react-bootstrap/Badge';
import ListGroup from 'react-bootstrap/ListGroup';
import Button from 'react-bootstrap/Button';

class CreateControlView extends React.Component {
    constructor(props) {
        super(props);
        this.state = { 
            control: {
                pk: 0,
                cn: "",
                name: "",
                description: "",
                parent_control: null,
                tags: []
            }
        };
      }
    
    render() {
        const properties = this.props.controls;
        return(
            <div>
                <h2>Add new Control</h2>
                <Container fluid>
                    <Row xs sm="2"><label for="txtControlCN">Control Number</label></Row>
                    <Row xs sm="2"><input type="text" id="txtControlCN" class="txt"></input></Row>
                    <Row xs sm="2"><label for="txtControlName">Control Name</label></Row>
                    <Row xs sm="2"><input type="text" id="txtControlName" class="txt"></input></Row>
                    <Row xs sm="2"><label for="selControlCategory">Control Category</label></Row>
                    <Row xs sm="2">
                        <select id="selControlCategory" class="txt">
                            <option value="directive">Directive</option>
                            <option value="deterrent">Deterrent</option>
                            <option value="preventive:">Preventive</option>
                            <option value="compensating">compensating</option>
                            <option value="detective">detective</option>
                            <option value="corrective">corrective</option>
                            <option value="recovery">recovery</option>
                        </select>
                    </Row>
                    <Row xs sm="2"><label for="selParentControl">Parent Control</label></Row>
                    <Row xs sm="2">
                        <select id="selParentControl" class="txt">
                            <option value="">None</option>
                            <option value="">Access Control</option>
                            <option value="">Account Management</option>
                            <option value="">Automated System Account Management</option>
                        </select>
                    </Row>
                    <Row xs sm="2"><label for="txtControlDescription">Description</label></Row>
                    <Row xs sm="2"><textarea  id="txtControlDescription" class="txt" rows="4"></textarea ></Row>
                    <Row xs sm="2"><label>Tags</label></Row>
                    <Row xs sm="4"><Button variant="secondary">Add Tag</Button>{' '}</Row>
                    <Row xs sm="2">
                        <ListGroup as="ol" numbered>
                            <ListGroup.Item as="li" className="d-flex justify-content-between align-items-start">
                                <div className="ms-2 me-auto">
                                <div className="fw-bold">Restricted Applications</div>
                                Assets of the type Software for which the access is restricted in any way.
                                </div>
                            </ListGroup.Item>
                            <ListGroup.Item as="li" className="d-flex justify-content-between align-items-start">
                                <div className="ms-2 me-auto">
                                <div className="fw-bold">Restricted Servers</div>
                                Assets of the type Hardware for which the access is restricted in any way.
                                </div>
                            </ListGroup.Item>
                            <ListGroup.Item as="li" className="d-flex justify-content-between align-items-start">
                                <div className="ms-2 me-auto">
                                <div className="fw-bold">User Account access</div>
                                Assets which just can be accessed with a user account.
                                </div>
                            </ListGroup.Item>
                        </ListGroup>
                    </Row>
                    <Row xs sm="4">
                        <Col><button class="buttons btnGreen">Save</button></Col>
                        <Col><button onClick={this.props.onClick} class="buttons btnRed">Cancel</button></Col>
                    </Row>
                </Container>


            </div>
        );
    }
}

export default CreateControlView;