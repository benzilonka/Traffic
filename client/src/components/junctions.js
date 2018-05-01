/*jshint esversion: 6 */
import React, { Component } from 'react';
import { withScriptjs, withGoogleMap, GoogleMap, Marker } from "react-google-maps";
import { compose, withProps } from "recompose";
import {
    Container, 
    Row, 
    Col,
    Button,
    FormGroup,
    Label,
    Input 
  } from 'reactstrap';
import '../styles/App.css';
import '../styles/Junctions.css';

const MAP_DEFAULT = {
    lat: 31.789523,
    lng: 34.640348,
    zoom: 11
};

var MyMapComponent;

class Junctions extends Component {
    constructor(props) {
        super(props);
        this.state = {
            show_create_junction_panel: false,
            show_add_dataset_panel: false
        };
        this.init_map();
    }

    init_map = () => {
        let self = this;
        let markers = this.props.junctions.map(function(junction) {
            return (
                <Marker 
                    position={{ lat: junction.lat, lng: junction.lon }} 
                    key={junction.id} 
                    onClick={() => self.handleMarkerClick(junction)} 
                />
            );
        });
        MyMapComponent = compose(
            withProps({
              googleMapURL: "https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places",
              loadingElement: <div style={{ height: `100%` }} />,
              containerElement: <div style={{ height: `380px` }} />,
              mapElement: <div style={{ height: `100%` }} />,
            }),
            withScriptjs,
            withGoogleMap
          )((props) =>
            <GoogleMap
                defaultZoom={MAP_DEFAULT.zoom}
                defaultCenter={{ lat: MAP_DEFAULT.lat, lng: MAP_DEFAULT.lng }}                
            >
              {markers}
            </GoogleMap>
        );
    }

    handleMarkerClick = junction => {
        this.props.selectJunction(junction);
    }
    getDatasetFiles = dataset_id => {
        this.props.getDatasetFiles(dataset_id);
    }
    toggleAddJunction = () => {
        this.setState({
            show_create_junction_panel: !this.state.show_create_junction_panel,
            new_junction: {
                name: '',
                lat: '',
                lon: ''
            }
        });
    }
    addJunction = () => {
        let self = this;
        this.props.addJunction(this.state.new_junction, function(response) {
            self.toggleAddJunction();
            self.init_map();            
        });
    }
    handleNewJunctionNameChange = e => {
        let new_junction = this.state.new_junction;
        new_junction.name = e.target.value;
        this.setState({
            new_junction: new_junction
        });
    }
    handleNewJunctionLongitudeChange = e => {
        let new_junction = this.state.new_junction;
        new_junction.lon = e.target.value;
        this.setState({
            new_junction: new_junction
        });
    }
    handleNewJunctionLatitudeChange = e => {
        let new_junction = this.state.new_junction;
        new_junction.lat = e.target.value;
        this.setState({
            new_junction: new_junction
        });
    }
    deleteJunction = () => {
        let self = this;
        this.props.deleteJunction(function(response) {
            self.init_map();
        });
    }
    toggleAddDataset = () => {
        this.setState({
            show_add_dataset_panel: !this.state.show_add_dataset_panel,
            new_dataset: {
                name: ''
            }
        });
    }    
    addDataset = () => {
        let self = this;
        this.props.addDataset(this.state.new_dataset, function(response) {
            self.toggleAddDataset();
        });
    }
    handleNewDatasetNameChange = e => {
        let new_dataset = this.state.new_dataset;
        new_dataset.name = e.target.value;
        this.setState({
            new_dataset: new_dataset
        });
    }

    render() {
        let self = this;
        let title;
        if(this.props.selectedJunction != null) {
            title = "Showing data for " + this.props.selectedJunction.name;
        } else {
            title = "Please select a junction from the map";
        }



        let add_dataset_panel = (<span></span>);
        if(this.state.show_add_dataset_panel) {
            add_dataset_panel = (
                <div className="input-panel">
                      <FormGroup>
                        <Label>Dataset Name:</Label>
                        <Input 
                            type="text" 
                            placeholder={`Dataset Name`}
                            value={this.state.new_dataset.name} 
                            onChange={(e) => this.handleNewDatasetNameChange(e)} 
                        />
                      </FormGroup>
                        <Button color="success" onClick={(e) => this.addDataset()}>Add</Button>
                  </div>
            );
        }



        let feeds = (<span></span>);
        if(this.props.selectedJunction != null && this.props.selectedJunction.datasets != null) {
            let _feeds = this.props.selectedJunction.datasets.map(function(entry) {
                return (
                    <li key={entry.id} onClick={() => self.getDatasetFiles(entry.id)}>
                        {entry.name}
                    </li>
                );
            });
            feeds = (
                <div>
                    <h5 key="feeds-list-h5">{_feeds.length > 0 ? 'Select a feed:' : 'No datasets available.'}</h5>
                    <ul key="feeds-list-ul">
                        {_feeds}
                    </ul>
                    <Button color="primary" onClick={(e) => this.toggleAddDataset()}>Add new dataset</Button>
                    <Button color="danger" onClick={(e) => this.deleteJunction()}>Delete junction</Button>
                    {add_dataset_panel}
                </div>
            );
        }


        
        let create_junction_panel = (<span></span>);
        if(this.state.show_create_junction_panel) {
            create_junction_panel = (
                <div className="input-panel">
                    <FormGroup>
                        <Label>Name:</Label>
                        <Input 
                            type="text" 
                            placeholder={`Junction Name`}
                            value={this.state.new_junction.name} 
                            onChange={(e) => this.handleNewJunctionNameChange(e)} 
                        />
                    </FormGroup>                    
                    <FormGroup>
                        <Label>Latitude:</Label>
                        <Input 
                            type="number" 
                            placeholder={`Junction Latitude`}
                            value={this.state.new_junction.lat} 
                            onChange={(e) => this.handleNewJunctionLatitudeChange(e)} 
                        />
                    </FormGroup>
                    <FormGroup>
                        <Label>Longitude:</Label>
                        <Input 
                            type="number" 
                            placeholder={`Junction Longitude`}
                            value={this.state.new_junction.lon}
                            onChange={(e) => this.handleNewJunctionLongitudeChange(e)} 
                        />
                    </FormGroup>
                    <Button color="success" onClick={(e) => this.addJunction(this.init_map)}>Create</Button>
                </div>
            );
        }



        return (
            <Container id="junctions">
                <Row>
                    <Col xs={12}>
                        <MyMapComponent isMarkerShown={true} id="google-map"/>
                        <h1>{title}</h1>
                        <div id="feeds-list">
                            {feeds}
                        </div>
                        <hr/>
                        <div>
                            <Button color="primary" onClick={(e) => this.toggleAddJunction()}>Create new junction</Button>
                            {create_junction_panel}
                        </div>
                    </Col>
                </Row>
            </Container>
        );
    }
}

export default Junctions;
