/*jshint esversion: 6 */
import React, { Component } from 'react';
import { CSSTransitionGroup } from 'react-transition-group';
import loading_gif from './images/loading.gif';

import {
  Container, 
  Row, 
  Col,
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink 
} from 'reactstrap';
import axios from 'axios';
import Videos from './components/videos.js';
import Map from './components/map.js';
import Controls from './components/controls.js';
import Junctions from './components/junctions.js';
import Simulation from './components/simulation.js';
import Search from './components/search.js';
import './styles/App.css';

const FRAME_TIME = 0.066666666666;
const SECOND = 1000;
const SERVER_URL = 'http://localhost:8080/';
const TABS = {
  main: 0,
  junctions: 1,
  simulation: 2
};
const FADE_IN_TIME = 300;
const loadingStyle = {      
  backgroundImage: `url(${loading_gif})`
};


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      frames: [null, null, null, null],
      statistics: [null, null, null, null],
      urls: [null, null, null, null],
      playing: false,
      played: 0,
      playbackRate: 1.0,
      currentFrame: null,
      numOfFrames: 0,
      seeking: false,
      loading: false,
      showSpeed: false,
      showTTC: false,
      showDistance: false,
      tab: TABS.main,
      junctions: [],
      selectedJunction: null,
      isMenuOpen: false,
      search_results: []
    };
    let self = this;
    setTimeout(function() {
      self.getJunctions(function() {});
    }, 100);
  }
  toggleShowSpeed = () => {
    this.setState({
      showSpeed: !this.state.showSpeed
    });
  };
  toggleShowTTC = () => {
    this.setState({
      showTTC: !this.state.showTTC
    });
  };
  toggleShowDistance = () => {
    this.setState({
      showDistance: !this.state.showDistance
    });
  };

  resetSelection = () => {
    this.onEnded();
    this.setState({
      frames: [null, null, null, null],
      urls: [null, null, null, null],
      statistics: [null, null, null, null],
      selectedJunction: null
    });
  };

  playPause = () => {
    if(this.state.frames.filter(frames => frames != null).length === 0 || (false && this.state.urls.filter(url => url != null).length === 0)) {
      return false;
    }
    if(!this.state.playing) {
      var timeout = FRAME_TIME * this.state.playbackRate;
      let self = this;
      var playFrame = function() {
        if(self.state.playing && self.state.currentFrame < self.state.numOfFrames) {
          let played = self.state.currentFrame + 1;
          played /= self.state.numOfFrames;
          timeout = FRAME_TIME / self.state.playbackRate;
          self.setState({
            currentFrame: self.state.currentFrame + 1,
            played: played
          }, function() { setTimeout(playFrame, timeout * SECOND); });
        } else {
          if(self.state.currentFrame >= self.state.numOfFrames) {
            self.onEnded();
          }
        }
      };
      setTimeout(playFrame, timeout);
    }
    this.setState({ playing: !this.state.playing });
    return false;
  };
  onEnded = () => {
    this.setState({ 
      playing: false,
      played: 0,
      currentFrame: null
    });    
  };
  setPlaybackRate = rate => {
    this.setState({ playbackRate: rate });
  };
  onSeekMouseDown = e => {
  };
  onSeekChange = seekTo => {
    this.setState({ 
      played: seekTo,
      currentFrame: Math.floor(this.state.numOfFrames * seekTo)
    });
    if(this.refs.videos) {
      this.refs.videos.seekTo(seekTo);
    }
  };
  onSeekMouseUp = e => {
  };
  onProgress = state => {
  };
  
  readVideoFile = (i, event) => {
    let self = this;
    const input = event.target;
    const url = URL.createObjectURL(input.files[0]);
    let urls = this.state.urls;
    urls[i] = url;
    this.setState({
      urls: urls
    }, function() {
      if(this.refs.videos) {
        setTimeout(function() {
          self.refs.videos.seekTo(self.state.played);
        }, SECOND * FRAME_TIME);
      }
    });
  };

  loadFiles = (json, meta, i) => {
    this.setState({
      loading: true
    });
    let self = this;
    let junction_id = -1;
    let dataset_id = -1;
    let route = 'getFrames';
    if(this.state.selectedJunction && this.state.selectedJunction.currentDataset) {
      junction_id = this.state.selectedJunction.id;
      dataset_id = this.state.selectedJunction.currentDataset;
      route = 'addDatasetFile';
    }
    axios.post(SERVER_URL, {
      route: route,
      json: json,
      meta: meta,
      index: i,
      junction_id: junction_id,
      dataset_id: dataset_id
    })
    .then(function (response) {        
      try {
        let _frames = self.state.frames;        
        if(response.data.hasOwnProperty('statistics')){
          self.storeStatistics(response.data.statistics, i);
          response.data = response.data.frames;
        }
        _frames[i] = self.parseFrames(response.data, i);        
        let size = 0;
        _frames.map(function(frames_for_direction) {
          if(frames_for_direction && frames_for_direction.cars && frames_for_direction.cars.length > size) {
            size = frames_for_direction.cars.length;
          }
          return null;
        });
        self.setState({
          frames: _frames,
          numOfFrames: size,
          loading: false
        });
        self.onEnded();
      }
      catch(e) {
        console.log(e);
      }
    });
  };

  parseFrames = (json, direction) => {
    //console.log(json);
    let i = 0;
    let frames = {
      cars: [],
      traffic_lights: []
    };
    json.map(function(frame) {
      let cars = [];
      //console.log(frame);
      frame.objects.map(function(car) {
        let c = {
          y: Math.floor(car.bounding_box[1] / 2),
          x: Math.floor(car.bounding_box[0] / 2),
          type: car.type,
          direction: direction,
          tracking_id: car.tracking_id,
          speed: car.speed,
          ttc: car.ttc,
          distance: car.distance,
          key: i
        };
        if(car.hasOwnProperty('passed_in_red')){
          c.passed_in_red = car.passed_in_red;
        }
        cars.push(c);
        i++;
        return null;
      });
      frames.cars.push(cars);
      frames.traffic_lights.push(frame.light_status);
      return null;
    });
    return frames;
  };

  getJunctions = callback => {
    this.setState({
      loading: true
    });
    let self = this;
    axios.post(SERVER_URL, {
      route: 'getJunctions'
    })
    .then(function (response) {
      try {
        //console.log(response.data);
        response.data.map(function(junc) {
          junc.lat = parseFloat(junc.lat);
          junc.lng = parseFloat(junc.lng);
          return null;
        });
        self.setState({
          junctions: response.data,
          loading: false
        }, function() { callback(response.data); });
      }
      catch(e) {
        console.log(e);
        callback(e);
      }
    });
  };

  getDatasets = (junction_id, callback) => {
    this.setState({
      loading: true
    });
    let self = this;
    axios.post(SERVER_URL, {
      route: 'getDatasets',
      junction_id: junction_id
    })
    .then(function (response) {        
      try {
        let selectedJunction = self.state.selectedJunction;
        if(selectedJunction == null) {
          selectedJunction = self.getJunction(junction_id);
          if(selectedJunction !== null) {
            selectedJunction.datasets = response.data;
          } else {
            selectedJunction = {
              datasets: response.data
            };
          }
        } else {
          selectedJunction.datasets = response.data;
        }
        self.setState({
          selectedJunction: selectedJunction,
          loading: false
        });
        callback(response.data);
      }
      catch(e) {
        console.log(e);
        callback(e);
      }
    });
  };

  getDatasetFiles = (dataset_id, callback = null) => {
    this.setState({
      frames: [null, null, null, null],
      urls: [null, null, null, null],
      statistics: [null, null, null, null],
      loading: true
    });
    let self = this;
    axios.post(SERVER_URL, {
      route: 'getDatasetFiles',
      dataset_id: dataset_id,
      junction_id: self.state.selectedJunction ? self.state.selectedJunction.id : 0
    })
    .then(function (response) {
      try {
        let _frames = [];
        let i = 0;
        response.data.map(function(data_for_direction) {                
          if(data_for_direction.hasOwnProperty('statistics')){
            self.storeStatistics(data_for_direction.statistics, i);
            data_for_direction = data_for_direction.frames;
          }
          _frames[i] = self.parseFrames(data_for_direction, i);
          i++;
          return null;
        });
        let size = 0;
        _frames.map(function(frames_for_direction) {
          //console.log(frames_for_direction);
          if(frames_for_direction.cars.length > size) {
            size = frames_for_direction.cars.length;
          }
          return null;
        });
        let selectedJunction = self.state.selectedJunction;
        if(selectedJunction == null) {
          selectedJunction = { id: 0 };
        }
        selectedJunction.currentDataset = dataset_id;
        self.setState({
          frames: _frames,
          numOfFrames: size,
          loading: false,
          selectedJunction: selectedJunction
        });
        self.onEnded();
        self.goToTab(TABS.main);
        if(typeof callback === 'function') {
          callback();
        }
      }
      catch(e) {
        console.log(e);
      }
    });
  };

  addJunction = (junction, callback) => {
    let self = this;
    axios.post(SERVER_URL, {
      route: 'addJunction',
      junction: junction
    })
    .then(function (response) {        
      try {
        self.getJunctions(callback);
      }
      catch(e) {
        console.log(e);
      }
    });
  };

  deleteJunction = (callback) => {
    this.setState({
      loading: true
    });
    let self = this;
    axios.post(SERVER_URL, {
      route: 'deleteJunction',
      junction_id: self.state.selectedJunction.id
    })
    .then(function (response) {        
      try {
        self.setState({
          selectedJunction: null,
          loading: false
        }, function() { self.getJunctions(callback); });        
      }
      catch(e) {
        console.log(e);
      }
    });
  };

  addDataset = (dataset, callback) => {
    let self = this;
    axios.post(SERVER_URL, {
      route: 'addDataset',
      junction_id: self.state.selectedJunction.id,
      dataset: dataset
    })
    .then(function (response) {      
      try {
        self.getDatasets(self.state.selectedJunction.id, callback);
      }
      catch(e) {
        console.log(e);
      }
    });
  };

  createSimulation = simulation => {
    this.setState({
      loading: true
    });
    let self = this;
    axios.post(SERVER_URL, {
      route: 'createSimulation',
      simulation: simulation,
      junction_id: 0
    })
    .then(function (response) {      
      try {
        simulation.id = 0;
        self.setState({
          selectedJunction: simulation,
          loading: false
        });
        self.getDatasetFiles(response.data);
      }
      catch(e) {
        console.log(e);
      }
    });
  };

  getSimulations = () => {
    let self = this;
    axios.post(SERVER_URL, {
      route: 'getSimulations'
    })
    .then(function (response) {      
      try {
        self.setState({
          simulations: response.data
        });
      }
      catch(e) {
        console.log(e);
      }
    });
  };

  goToTab = tab_index => {
    let selectedJunction = this.state.selectedJunction;
    if(tab_index === TABS.junctions) {
      selectedJunction = null;
    }
    this.onEnded();
    this.setState({
      tab: tab_index,
      isMenuOpen: false,
      search_results: [],
      selectedJunction: selectedJunction
    });
    window.scrollTo(0,0);
  };
  toggleMenu = () => {
    this.setState({
      isMenuOpen: !this.state.isMenuOpen
    });
  };
  selectJunction = junction => {
    //console.log(junction);
    if(junction) {
      junction.datasets = [];
      this.setState({
        selectedJunction: junction
      });
      if(junction.datasets == null || junction.datasets.length === 0) {
        this.getDatasets(junction.id, function() {});
      }
    } else {
      this.setState({
        selectedJunction: null
      });
    }   
  };
  getJunction = junction_id => {
    let ret = null;
    if(this.state.junctions != null) {
      this.state.junctions.map(function(junction) {
        if(junction.id === junction_id) {
          ret = junction;
        }
        return null;
      });
    }
    return ret;
  };
  search = params => {
    //console.log(params);
    if(params.selectedJunction == null || params.selectedValue == null || ((params.selectedValue === 'equal' || params.selectedValue === 'bool') && params.equalTo == null) || (params.selectedValue === 'minmax' && (params.min == null || params.max == null))) {
      return;
    }
    let data = {
      route: 'searchData',
      junction_id: params.selectedJunction,
      meta_key: params.selectedField,
    };
    if(params.selectedDataset > 0) {
      data.dataset_id = params.selectedDataset;
    }
    switch(params.selectedValue) {
      case 'equal':
      case 'bool':
        data.meta_value = params.equalTo;
        break;
      case 'minmax':
        data.min_meta_value = params.min;
        data.max_meta_value = params.max;
        break;
      default:
        break;
    }
    //console.log(data);
    let self = this;
    axios.post(SERVER_URL, data)
    .then(function (response) {
      try {
        self.setState({
          search_results: response.data
        });
      }
      catch(e) {
        console.log(e);
      }
    });
  };
  highlightVehicle = vehicle_id => {
    this.setState({
      highlightVehicle: vehicle_id
    });
  };

  storeStatistics = (statistics, i) => {
    let curr_stats = this.state.statistics;
    curr_stats[i] = statistics;
    this.setState({
      statistics: curr_stats
    });
  };

  render = () => {
    let curr_tab;
    switch(this.state.tab) {
      case TABS.main:
        curr_tab = (
          <CSSTransitionGroup transitionName="fade-in" transitionLeave={false} transitionEnterTimeout={FADE_IN_TIME}>
            <Container fluid key="main-tab">
              <Row>              
                <Col xs={7}>
                  <Map ref="map"
                      frames={this.state.frames}
                      statistics={this.state.statistics}
                      currentFrame={this.state.currentFrame}
                      playing={this.state.playing}
                      played ={this.state.played}
                      playbackRate={this.state.playbackRate} 
                      setPlaybackRate={this.setPlaybackRate.bind(this)}
                      loading={this.state.loading}
                      showSpeed={this.state.showSpeed}
                      showTTC={this.state.showTTC}
                      showDistance={this.state.showDistance}
                      highlightVehicleFunc={this.highlightVehicle.bind(this)}
                      highlightVehicle={this.state.highlightVehicle}>
                  </Map>
                </Col>
                <Col xs={5}>
                  <Row>
                    <Col xs={12}>
                      <Videos ref="videos"
                              readVideoFile={this.readVideoFile.bind(this)} 
                              loadFiles={this.loadFiles.bind(this)} 
                              onProgress={this.onProgress.bind(this)}
                              onEnded={this.onEnded.bind(this)}
                              playing={this.state.playing}
                              playbackRate={this.state.playbackRate} 
                              setPlaybackRate={this.setPlaybackRate.bind(this)} 
                              urls={this.state.urls}>
                      </Videos> 
                    </Col>
                  </Row>
                  <Row>
                    <Col xs={12}>
                      <Controls ref="controls"
                              playing={this.state.playing}
                              played={this.state.played} 
                              playPause={this.playPause.bind(this)}
                              playbackRate={this.state.playbackRate} 
                              setPlaybackRate={this.setPlaybackRate.bind(this)} 
                              onSeekMouseDown={this.onSeekMouseDown.bind(this)}
                              onSeekChange={this.onSeekChange.bind(this)}
                              onSeekMouseUp={this.onSeekMouseUp.bind(this)}
                              toggleShowSpeed={this.toggleShowSpeed.bind(this)}
                              toggleShowTTC={this.toggleShowTTC.bind(this)}
                              toggleShowDistance={this.toggleShowDistance.bind(this)}
                              selectedJunction={this.state.selectedJunction}
                              resetSelection={this.resetSelection.bind(this)}
                              junctions={this.state.junctions}
                              getDatasets={this.getDatasets.bind(this)}>
                      </Controls>
                    </Col>
                  </Row>
                </Col>
              </Row>
            </Container>
          </CSSTransitionGroup>
        );
        break;
      case TABS.junctions:
        curr_tab = (
          <CSSTransitionGroup transitionName="fade-in" transitionLeave={false} transitionEnterTimeout={FADE_IN_TIME}>
            <Container fluid key="junctions-tab">
              <Row>
                <Col xs={12}>
                    <Junctions junctions={this.state.junctions} 
                               selectedJunction={this.state.selectedJunction} 
                               selectJunction={this.selectJunction.bind(this)}
                               getDatasetFiles={this.getDatasetFiles.bind(this)}
                               addJunction={this.addJunction.bind(this)}
                               deleteJunction={this.deleteJunction.bind(this)}
                               addDataset={this.addDataset.bind(this)}>
                    </Junctions>
                </Col>
              </Row>          
            </Container>
          </CSSTransitionGroup>
        );
        break;
      case TABS.simulation:
        curr_tab = (
          <CSSTransitionGroup transitionName="fade-in" transitionLeave={false} transitionEnterTimeout={FADE_IN_TIME}>
            <Container fluid key="simulation-tab">
              <Row>
                <Col xs={12}>
                    <Simulation createSimulation={this.createSimulation.bind(this)}
                                simulations={this.state.simulations}
                                selectJunction={this.selectJunction.bind(this)}
                                getSimulations={this.getSimulations.bind(this)}
                                getDatasetFiles={this.getDatasetFiles.bind(this)}>
                    </Simulation>
                </Col>
              </Row>          
            </Container>
          </CSSTransitionGroup>
        );
        break;
      default:
        curr_tab = (
          <h1>Page not found</h1>
        );
        break;
    }

    let loading = '';
    if(this.state.loading) {
      loading = (
        <div className="Loading" style={loadingStyle}></div>
      );
    }

    return (
      <div className="App">
          <Navbar color="light" light expand="md">
            <NavbarBrand onClick={(e) => this.goToTab(TABS.main)}>NoTraffic</NavbarBrand>
            <NavbarToggler onClick={this.toggleMenu} />
            <Collapse isOpen={this.state.isMenuOpen} navbar>
              <Nav className="ml-auto" navbar>
                <NavItem>
                  <NavLink onClick={(e) => this.goToTab(TABS.main)}>Main</NavLink>
                </NavItem>
                <NavItem>
                  <NavLink onClick={(e) => this.goToTab(TABS.junctions)}>Junctions</NavLink>
                </NavItem>
                <NavItem>
                  <NavLink onClick={(e) => this.goToTab(TABS.simulation)}>Simulation</NavLink>
                </NavItem>
              </Nav>
            </Collapse>
          </Navbar>
          {curr_tab}
          <hr/>
          <Search selectedJunction={this.state.selectedJunction}
                  junctions={this.state.junctions}
                  getDatasets={this.getDatasets.bind(this)}
                  search={this.search.bind(this)}
                  search_results={this.state.search_results}
                  getDatasetFiles={this.getDatasetFiles.bind(this)}
                  onSeekChange={this.onSeekChange.bind(this)}
                  highlightVehicle={this.highlightVehicle.bind(this)}
          ></Search>
          {loading}
      </div>
    );
  }
}

export default App;
