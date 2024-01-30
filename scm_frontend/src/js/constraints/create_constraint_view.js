import 'bootstrap/dist/css/bootstrap.css';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Badge from 'react-bootstrap/Badge';
import ListGroup from 'react-bootstrap/ListGroup';
import Button from 'react-bootstrap/Button';

function CreateConstraintView(props) {
    return(
        <div>
            <h2>Add new Tag</h2>
            <Container fluid>
                <Row xs sm="2"><label for="txtConstraintName">Constraint Name</label></Row>
                <Row xs sm="2"><input type="text" id="txtConstraintName" class="txt"></input></Row>
                <Row xs sm="2"><label for="txtConstraintDescription">Description</label></Row>
                <Row xs sm="2"><textarea  id="txtConstraintDescription" class="txt" rows="4"></textarea ></Row>
                <Row xs sm="2"><label for="selConstraintCategory">Constraint Type</label></Row>
                <Row xs sm="2">
                    <select id="selConstraintCategory" class="txt">
                        <option value="string">String</option>
                        <option value="integer">Integer</option>
                    </select>
                </Row>
                <Row xs sm="2"><label>Value</label></Row>
                <Row xs sm="4"><Button variant="secondary">Add Value</Button>{' '}</Row>
                <Row xs sm="2">
                    <ListGroup as="ol" numbered>
                        <ListGroup.Item as="li" className="d-flex justify-content-between align-items-start">
                            <div className="ms-2 me-auto">
                            <div className="fw-bold">Low</div>
                            </div>
                        </ListGroup.Item>
                        <ListGroup.Item as="li" className="d-flex justify-content-between align-items-start">
                            <div className="ms-2 me-auto">
                            <div className="fw-bold">Medium</div>
                            </div>
                        </ListGroup.Item>
                        <ListGroup.Item as="li" className="d-flex justify-content-between align-items-start">
                            <div className="ms-2 me-auto">
                            <div className="fw-bold">High</div>
                            </div>
                        </ListGroup.Item>
                    </ListGroup>
                </Row>
            </Container>


        </div>
    );
  }

export default CreateConstraintView;