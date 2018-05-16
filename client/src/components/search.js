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
import Select from 'react-select';
import '../styles/App.css';
import '../styles/Controls.css';
import {RadioGroup, Radio} from 'react-radio-group';


class Search extends Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedJunction: null,
            selectedDataset: null,
            selectedField: null,
            datasets: [],
            selectedValue: null,
            equalTo: 0,
            min: 0,
            max: 0
        };
    }

    handleJunctionSelectChange = (selectedOption) => {
        this.setState({
            selectedJunction: selectedOption.value
        }); 
        let self = this;
        this.props.getDatasets(selectedOption.value, function(response) {
            self.setState({
                datasets: response
            });
        });
    };
    handleDatasetSelectChange = (selectedOption) => {
        this.setState({ selectedDataset: selectedOption.value });
    };
    handleFieldSelectChange = (selectedOption) => {
        if(selectedOption.bool) {            
            this.setState({ selectedValue: 'bool' });
        } else {
            this.setState({ selectedValue: null });
        }
        this.setState({ selectedField: selectedOption.value });
    };
    handleValueChange = (selectedOption) => {
        this.setState({ selectedValue: selectedOption });
    };
    handleBoolChange = (selectedOption) => {
        this.setState({ equalTo: selectedOption });
    };
    handleEqualToChange = e => {
        this.setState({
            equalTo: e.target.value
        });
    };
    handleMinChange = e => {
        this.setState({
            min: e.target.value
        });
    };
    handleMaxChange = e => {
        this.setState({
            max: e.target.value
        });
    };

    getJunctionName = junction_id => {
        let j = null;
        this.props.junctions.map(function(junction) {
            if(j === null) {
                if(junction.id === junction_id) {
                    j = junction.name;
                }
            }
            return null;
        });
        return j;
    };

    selectSearchResult = data => {
        let self = this;
        this.props.highlightVehicle(data.vehicle_id);
        this.props.getDatasetFiles(data.dataset_id, function() {
            self.props.onSeekChange(data.frame_index / data.number_of_frames);
        });        
    };

    render() {
        let self = this;
        let junctions = [];
        this.props.junctions.map(function(junction) {
            junctions.push({
                value: junction.id,
                label: junction.name
            });
            return null;
        });
        let datasets = [{
            value: -1,
            label: 'All datasets'
        }];
        if(this.state.datasets != null) {
            this.state.datasets.map(function(dataset) {
                datasets.push({
                    value: dataset.id,
                    label: dataset.name
                });
                return null;
            });
        }

        let inputs = (<span></span>);
        switch(this.state.selectedValue) {
            case 'bool':
                inputs = (
                    <RadioGroup name="equalTo" onChange={this.handleBoolChange}>
                        <Radio value={1} /> True
                        <br/>
                        <Radio value={0} /> False
                    </RadioGroup>
                );
                break;
            case 'equal':
                inputs = (
                    <Input 
                        step="0.1"
                        type="number" 
                        placeholder={`Search datasets where value equals to`}
                        value={this.state.equalTo} 
                        onChange={(e) => this.handleEqualToChange(e)}
                    />
                );
                break;
            case 'minmax':
                inputs = (
                    <div>
                        <Label>Minimum:</Label>
                        <Input 
                            step="0.1"
                            type="number" 
                            placeholder={`Minimum`}
                            value={this.state.min} 
                            onChange={(e) => this.handleMinChange(e)}
                        />
                        <Label>Maximum:</Label>
                        <Input 
                            step="0.1"
                            type="number" 
                            placeholder={`Maximum`}
                            value={this.state.max} 
                            onChange={(e) => this.handleMaxChange(e)}
                        />
                    </div>
                );
                break;
            default:
                inputs = (<span></span>);
                break;
        }

        let i = 0;
        let results = (<span></span>);
        if(this.props.search_results != null) {
            //console.log(this.props.search_results);
            results = this.props.search_results.map(function(result) {
                i++;
                return (
                    <li key={i} className="search-result"
                        onClick={(e) => self.selectSearchResult(result)}>
                        Junction {self.getJunctionName(result.junction_id)} Dataset {result.dataset_id} Frame {result.frame_index} / {result.number_of_frames}
                    </li>
                );
            });
        }

        let results_wrap = (<ul>{results}</ul>);
        if(this.props.search_results.length === 0) {
            results_wrap = (<p>Nothing to show</p>);
        }

        let radios = (<span></span>);
        if(this.state.selectedValue != 'bool') {
            radios = (
                <RadioGroup name="values" selectedValue={this.state.selectedValue} onChange={this.handleValueChange}>
                    <Radio value="equal" /> Equal to
                    <br/>
                    <Radio value="minmax" /> Min-Max
                </RadioGroup>
            );
        }

        let search_body = (
            <div>
                <FormGroup>
                    <Label>Select junction:</Label>
                    <Select
                        name="form-junction"
                        value={this.state.selectedJunction}
                        onChange={this.handleJunctionSelectChange}
                        options={junctions}
                    />
                    <Label>Select dataset:</Label>
                    <Select
                        name="form-dataset"
                        value={this.state.selectedDataset}
                        onChange={this.handleDatasetSelectChange}
                        options={datasets}
                    />
                    <Label>Select field:</Label>
                    <Select
                        name="form-field-name"
                        value={this.state.selectedField}
                        onChange={this.handleFieldSelectChange}
                        options={[
                        { value: 'ttc', label: 'TTC' },
                        { value: 'speed', label: 'Speed' },
                        { value: 'against_direction_flag', label: 'Against Direction', bool: true },
                        { value: 'passed_in_red', label: 'Passed in Red', bool: true },
                        { value: 'change_lane_count', label: 'Change Lane Count' },
                        ]}
                    />
                    {radios}
                    {inputs}
                    <Button color="primary" onClick={(e) => this.props.search(this.state)}>Search</Button>
                    {results_wrap}
                </FormGroup>
            </div>
        );

        return (
            <Container fluid className="search">
                <Row>
                    <Col xs={12} lg={4}>
                        <h4>Search</h4>
                        {search_body}
                    </Col>
                </Row>
            </Container>
        );
    }
}

export default Search;




