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
                duration: 60,
                cars_per_second: 1,
                vehicle_info: {"car": [70, 0.8, 2.6, 4.5, 2.5, 1, -1], "bus": [55, 0.2, 2.1, 4.3, 2.5, 1, -1]}
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
    handleNewSimulationCarsPerSecondChange = e => {
        let new_simulation = this.state.new_simulation;
        new_simulation.cars_per_second = e.target.value;
        this.setState({
            new_simulation: new_simulation
        });
    }
    handleNewSimulationVehicleInfoChange = (e, type, i) => {
        let new_simulation = this.state.new_simulation;
        new_simulation.vehicle_info[type][i] = e.target.value;
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
                                <Label>Cars per second:</Label>
                                <Input 
                                    type="number" 
                                    placeholder={`Cars per second`}
                                    value={this.state.new_simulation.cars_per_second} 
                                    onChange={(e) => this.handleNewSimulationCarsPerSecondChange(e)} 
                                />
                            </FormGroup>
                            
                            <h3>Car policy:</h3>
                            <FormGroup>
                                <Label>Max speed:</Label>
                                <Input 
                                    type="number" 
                                    placeholder={`Max speed`}
                                    value={this.state.new_simulation.vehicle_info['car'][0]} 
                                    onChange={(e) => this.handleNewSimulationVehicleInfoChange(e, 'car', 0)} 
                                />
                            </FormGroup>
                            <FormGroup>
                                <Label>Speed:</Label>
                                <Input 
                                    type="number" 
                                    placeholder={`Speed`}
                                    value={this.state.new_simulation.vehicle_info['car'][1]} 
                                    onChange={(e) => this.handleNewSimulationVehicleInfoChange(e, 'car', 1)} 
                                />
                            </FormGroup>
                            <FormGroup>
                                <Label>Acceleration:</Label>
                                <Input 
                                    type="number" 
                                    placeholder={`Acceleration`}
                                    value={this.state.new_simulation.vehicle_info['car'][2]} 
                                    onChange={(e) => this.handleNewSimulationVehicleInfoChange(e, 'car', 2)} 
                                />
                            </FormGroup>
                            <FormGroup>
                                <Label>Deceleration:</Label>
                                <Input 
                                    type="number" 
                                    placeholder={`Deceleration`}
                                    value={this.state.new_simulation.vehicle_info['car'][3]} 
                                    onChange={(e) => this.handleNewSimulationVehicleInfoChange(e, 'car', 3)} 
                                />
                            </FormGroup>
                            <FormGroup>
                                <Label>Minimum gap between cars:</Label>
                                <Input 
                                    type="number" 
                                    placeholder={`Minimum gap between cars`}
                                    value={this.state.new_simulation.vehicle_info['car'][4]} 
                                    onChange={(e) => this.handleNewSimulationVehicleInfoChange(e, 'car', 4)} 
                                />
                            </FormGroup>
                            <FormGroup>
                                <Label>Lane change policy (1-inf):</Label>
                                <Input 
                                    type="number" 
                                    placeholder={`Lane change policy (1-inf):`}
                                    value={this.state.new_simulation.vehicle_info['car'][5]} 
                                    onChange={(e) => this.handleNewSimulationVehicleInfoChange(e, 'car', 5)} 
                                />
                            </FormGroup>
                            <FormGroup>
                                <Label>Make red crossing optional (-1 to 0):</Label>
                                <Input 
                                    type="number" 
                                    placeholder={`Make red crossing optional (-1 to 0)`}
                                    value={this.state.new_simulation.vehicle_info['car'][6]} 
                                    onChange={(e) => this.handleNewSimulationVehicleInfoChange(e, 'car', 6)} 
                                />
                            </FormGroup>

                            <h3>Bus policy:</h3>
                            <FormGroup>
                                <Label>Max speed:</Label>
                                <Input 
                                    type="number" 
                                    placeholder={`Max speed`}
                                    value={this.state.new_simulation.vehicle_info['bus'][0]} 
                                    onChange={(e) => this.handleNewSimulationVehicleInfoChange(e, 'bus', 0)} 
                                />
                            </FormGroup>
                            <FormGroup>
                                <Label>Speed:</Label>
                                <Input 
                                    type="number" 
                                    placeholder={`Speed`}
                                    value={this.state.new_simulation.vehicle_info['bus'][1]} 
                                    onChange={(e) => this.handleNewSimulationVehicleInfoChange(e, 'bus', 1)} 
                                />
                            </FormGroup>
                            <FormGroup>
                                <Label>Acceleration:</Label>
                                <Input 
                                    type="number" 
                                    placeholder={`Acceleration`}
                                    value={this.state.new_simulation.vehicle_info['bus'][2]} 
                                    onChange={(e) => this.handleNewSimulationVehicleInfoChange(e, 'bus', 2)} 
                                />
                            </FormGroup>
                            <FormGroup>
                                <Label>Deceleration:</Label>
                                <Input 
                                    type="number" 
                                    placeholder={`Deceleration`}
                                    value={this.state.new_simulation.vehicle_info['bus'][3]} 
                                    onChange={(e) => this.handleNewSimulationVehicleInfoChange(e, 'bus', 3)} 
                                />
                            </FormGroup>
                            <FormGroup>
                                <Label>Minimum gap between cars:</Label>
                                <Input 
                                    type="number" 
                                    placeholder={`Minimum gap between cars`}
                                    value={this.state.new_simulation.vehicle_info['bus'][4]} 
                                    onChange={(e) => this.handleNewSimulationVehicleInfoChange(e, 'bus', 4)} 
                                />
                            </FormGroup>
                            <FormGroup>
                                <Label>Lane change policy (1-inf):</Label>
                                <Input 
                                    type="number" 
                                    placeholder={`Lane change policy (1-inf):`}
                                    value={this.state.new_simulation.vehicle_info['bus'][5]} 
                                    onChange={(e) => this.handleNewSimulationVehicleInfoChange(e, 'bus', 5)} 
                                />
                            </FormGroup>
                            <FormGroup>
                                <Label>Make red crossing optional (-1 to 0):</Label>
                                <Input 
                                    type="number" 
                                    placeholder={`Make red crossing optional (-1 to 0)`}
                                    value={this.state.new_simulation.vehicle_info['bus'][6]} 
                                    onChange={(e) => this.handleNewSimulationVehicleInfoChange(e, 'bus', 6)} 
                                />
                            </FormGroup>
                            <Button color="success" onClick={(e) => this.createSimulation()}>Create</Button>
                        </div>
                    </Col>
                </Row>
            </Container>
        );
    }
}//max speed, sigma, acceleration, deceleration, minimum gap between cars,# lane change policy (1-inf), make red crossing optional (-1 to 0)

export default Simulation;
