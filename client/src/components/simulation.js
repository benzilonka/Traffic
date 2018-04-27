/*jshint esversion: 6 */
import React, { Component } from 'react';
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

class Simulation extends Component {
    constructor(props) {
        super(props);
        this.state = {
            new_simulation: {
                name: '',
                duration: 0,
                cars_per_second: 0,
                max_speed: 0
            }
        };
        this.props.getSimulations();
        this.props.selectJunction({ id: 0 });
    }

    handleNewSimulationNameChange = e => {
        let new_simulation = this.state.new_simulation;
        new_simulation.name = e.target.value;
        this.setState({
            new_simulation: new_simulation
        });
    }
    handleNewSimulationDurationChange = e => {
        let new_simulation = this.state.new_simulation;
        new_simulation.duration = e.target.value;
        this.setState({
            new_simulation: new_simulation
        });
    }
    handleNewSimulationcars_per_secondChange = e => {
        let new_simulation = this.state.new_simulation;
        new_simulation.cars_per_second = e.target.value;
        this.setState({
            new_simulation: new_simulation
        });
    }

    createSimulation = e => {
        this.props.createSimulation(this.state.new_simulation);
    }
    
    getSimulation = id => {
        this.props.getDatasetFiles(id);
    }

    render() {
        let self = this;
        let simulations = (<span></span>);
        if(this.props.simulations) {
            simulations = this.props.simulations.map(function(simulation) {
                return (
                    <li key={simulation.id} onClick={(e) => self.getSimulation(simulation.id)}>
                        {simulation.name}
                    </li>
                );
            });
        }
        return (
            <Container id="simulation">
                <Row>
                    <Col xs={6}>
                        <h2>Simulations</h2>
                    </Col>
                </Row>
                <Row>
                    <Col xs={6}>
                        <ul className="simulationsList">{simulations}</ul>                        
                    </Col>
                </Row>
                <hr/>
                <Row>
                    <Col xs={6}>
                        <h4>Create a simulation</h4>
                    </Col>
                </Row>
                <Row>
                    <Col xs={6}>
                        <div className="input-panel">
                            <FormGroup>
                                <Label>Simulation Name:</Label>
                                <Input 
                                    type="text" 
                                    placeholder={`Simulation Name`}
                                    value={this.state.new_simulation.name} 
                                    onChange={(e) => this.handleNewSimulationNameChange(e)} 
                                />
                            </FormGroup>
                            <FormGroup>
                                <Label>Duration (in seconds):</Label>
                                <Input 
                                    type="number" 
                                    placeholder={`Duration`}
                                    value={this.state.new_simulation.duration} 
                                    onChange={(e) => this.handleNewSimulationDurationChange(e)} 
                                />
                            </FormGroup>
                            <FormGroup>
                                <Label>Number of vehicles per second:</Label>
                                <Input 
                                    type="text" 
                                    placeholder={`Vehicles per second`}
                                    value={this.state.new_simulation.cars_per_second} 
                                    onChange={(e) => this.handleNewSimulationcars_per_secondChange(e)} 
                                />
                            </FormGroup>
                            <Button color="success" onClick={(e) => this.createSimulation()}>Create</Button>
                        </div>
                    </Col>
                </Row>
            </Container>
        );
    }
}

export default Simulation;
