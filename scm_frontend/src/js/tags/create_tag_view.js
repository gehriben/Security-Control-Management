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
import { API_URL_TAGS } from "../../constants";
import { API_URL_TAG } from "../../constants";
import { API_URL_KEYWORD } from "../../constants";
import { API_URL_KEYWORDS } from "../../constants";

class CreateTagView extends React.Component {
    constructor(props) {
        super(props);
        this.setData = this.setData.bind(this);
        this.addKeyword = this.addKeyword.bind(this);
        this.removeKeyword = this.removeKeyword.bind(this);
        this.editKeyword = this.editKeyword.bind(this);
        this.closeModal = this.closeModal.bind(this);
        this.state = { 
            tag: {
                pk: null,
                name: "",
                description: "",
                keywords: []
            },
            show_modal: false,
        };
      }
    
    componentDidMount() {
        this.setData();
    }

    setData() {
        if (this.props.pk != null) {
            axios.get(API_URL_TAG + this.props.pk).then(res => {
                const { pk, name, description, keywords } = res.data;
                this.setState({tag: { pk, name, description, keywords } });
            });
        }
    }
    
    onChange = e => {
        this.setState(prevState => {
            let tag = Object.assign({}, prevState.tag);
            tag[e.target.name] = e.target.value;
                                                        
            return { tag };                                 
          }); 
    };
    
    saveTag = e => {
        if (this.props.pk != null) { 
            axios.put(API_URL_TAG + this.state.tag.pk + "/", this.state.tag).then(() => {
                this.props.onClick();
            });
        } else {
            axios.post(API_URL_TAGS, this.state.tag).then(() => {
                this.props.onClick();
            });
        }

    }

    addKeyword = (keyword_pk) => {
        axios.get(API_URL_KEYWORD + keyword_pk).then(res => {
            let tag_data = this.state.tag;
            tag_data.keywords.push(res.data);

            this.setState({ tag: tag_data })
        });
    }

    removeKeyword = async (keyword_pk) => {
        let tag_data = this.state.tag;
        for(let i=0; i < tag_data.keywords.length; i++){
            if (keyword_pk == tag_data.keywords[i].pk) {
                tag_data.keywords.splice(i, 1);
            }
        }
        await this.setState({ tag: tag_data })
    }  

    editKeyword = (keyword_pk, new_keyword_name) => {
        console.log(keyword_pk)
        let tag_data = this.state.tag;
        for(let i=0; i < tag_data.keywords.length; i++){
            if (keyword_pk == tag_data.keywords[i].id) {
                tag_data.keywords[i].name = new_keyword_name 
                console.log(tag_data)
            }
        }
        this.setState({ tag: tag_data })
    }
    
    openModal() {
        this.setState({show_modal: true})
    }

    closeModal() {
        this.setState({show_modal: false})
    }

    defaultIfEmpty = value => {
        return value === "" ? "" : value;
    };

    render() {
        let modal = "";
        if (this.state.show_modal) {
            modal = <Modal closeModal={this.closeModal} content={<ModalContent addKeyword={this.addKeyword} closeModal={this.closeModal}  />} />
        } 

        return(
            <div>
                {modal}
                <h2>Add new Tag</h2>
                <Container fluid>
                    <Row xs sm="2"><label for="txtTagName">Tag Name</label></Row>
                    <Row xs sm="2"><input type="text" name="name" id="txtTagName" class="txt" onChange={this.onChange} value={this.defaultIfEmpty(this.state.tag.name)}></input></Row>
                    <Row xs sm="2"><label for="txtTagDescription">Description</label></Row>
                    <Row xs sm="2"><textarea  id="txtTagDescription" name="description" class="txt" rows="4" onChange={this.onChange} value={this.defaultIfEmpty(this.state.tag.description)}></textarea ></Row>
                    <Row xs sm="2"><label>Keywords</label></Row>
                    <Row xs sm="4"><Button variant="secondary" onClick={() => this.openModal()}>Add Keyword</Button>{' '}</Row>
                    <Row xs sm="2">
                        <ListGroup as="ol" numbered>
                        {!this.state.tag.keywords || this.state.tag.keywords.length <= 0 ? (
                            <div className="ms-2 me-auto">
                                <div className="fw-bold">No properties assigned</div>
                            </div>
                            ) : (
                                this.state.tag.keywords.map(keyword => ( 
                                <ListGroup.Item as="li" className="d-flex justify-content-between align-items-start">
                                    <KeywordElement keyword={keyword} setData={this.setData} removeKeyword={this.removeKeyword} editKeyword={this.editKeyword} />
                                </ListGroup.Item>
                                    ))
                            )}
                        </ListGroup>
                    </Row>
                    <Row xs sm="4">
                        <Col><button class="buttons btnGreen" onClick={() => this.saveTag()}>Save</button></Col>
                        <Col><button onClick={this.props.onClick} class="buttons btnRed">Cancel</button></Col>
                    </Row>
                </Container>
            </div>
        );
  }
}

class KeywordElement extends React.Component {
    constructor(props) {
        super(props);
        this.state = { 
            keyword: {
                pk: 0,
                name: ""
            },
            is_editedable: false
        };
      }

    toggleEditField() {
        this.setState({is_editedable: !this.state.is_editedable});
    }

    onChange = e => {
        console.log(e.target.value);
        this.props.editKeyword(this.props.keyword.pk, e.target.value);                                          
    };

    render() {
        return(
            <div className="ms-2 me-auto">
                <table>
                    <tbody>
                        
                            {this.state.is_editedable ? (
                                <tr>
                                    <td><input ref="txtKeywordName" type="text" name="name" id="txtKeywordName" class="txt" onChange={this.onChange} value={this.props.keyword.name}></input></td>
                                    <td><button class="btn" onClick={() => this.toggleEditField()}><i class="fa fa-floppy-o" aria-hidden="true"></i></button></td>
                                </tr>
                                ) : (
                                <tr>
                                    <td className="fw-bold">{this.props.keyword.name}</td>
                                    <td><button class="btn" onClick={() => this.toggleEditField()}><i class="fa fa-pencil" aria-hidden="true"></i></button></td>
                                    <td><button class="btn" onClick={() => this.props.removeKeyword(this.props.keyword.pk)}><i class="fa fa-trash" aria-hidden="true"></i></button></td>
                                </tr>
                                )
                            }
                        
                    </tbody>
                </table>
            </div>
        );
    }

}

class ModalContent extends React.Component {
    constructor(props) {
        super(props);
        this.state = { keywords: [], keyword_pk: 0 };
        
      }
    
    componentDidMount() {
        this.getKeywords();
    }

    getKeywords() {
        axios.get(API_URL_KEYWORDS).then(res => this.setState({ keywords: res.data }));
    }

    onChange = (e) => {
        this.setState({keyword_pk: e.target.value}); 
    };

    confirmKeyword() {
        this.props.addKeyword(this.state.keyword_pk);
        this.props.closeModal();
    }

    render() {
        const keywords = this.state.keywords;
        return(
            <>
                <h2>Add Keyword</h2>
                <Container fluid>
                    <Row xs sm="1">
                        <select id="selTagKeywords" name="keyword" class="txt" onChange={this.onChange}>
                            {keywords.map(keyword => (
                                <option value={keyword.pk}>{keyword.name}</option>
                            ))}
                        </select>
                    </Row>
                    <Row xs sm="1">
                        <Col><button class="buttons btnGreen" onClick={() => this.confirmKeyword()}>Confirm</button></Col>
                    </Row>
                </Container>
            </>
        );
    }

}


export default CreateTagView;