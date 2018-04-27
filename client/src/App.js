/*jshint esversion: 6 */
import React, { Component } from 'react';
import { CSSTransitionGroup } from 'react-transition-group';

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
import Simulation from './components/simulation';
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

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      frames: [null, null, null, null],
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
      isMenuOpen: false
    };

    this.getJunctions(function() {});
  }

  resetPlayback = () => {
    this.setState({
      playing: false,
      played: 0,
      currentFrame: 0
    });
  };

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

  playPause = () => {
    if(this.state.currentFrame == null || (false && this.state.urls.filter(url => url != null).length === 0)) {
      return false;
    }
    if(!this.state.playing) {
      var timeout = FRAME_TIME * this.state.playbackRate;
      let self = this;
      var playFrame = function() {
        if(self.state.playing) {
          let played = self.state.currentFrame + 1;
          played /= self.state.numOfFrames;
          self.setState({
            currentFrame: self.state.currentFrame + 1,
            played: played
          });
          timeout = FRAME_TIME / self.state.playbackRate;
          setTimeout(playFrame, timeout * SECOND);
        }
      };
      setTimeout(playFrame, timeout);
    }
    this.setState({ playing: !this.state.playing });
    return false;
  }
  onEnded = () => {
    this.setState({ 
      playing: false,
      currentFrame: 0
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
    if (!this.state.seeking) {
      this.setState(state);
    }
  };
  
  readVideoFile = (i, event) => {
    const input = event.target;
    const url = URL.createObjectURL(input.files[0]);
    let urls = this.state.urls;
    urls[i] = url;
    this.setState({
      urls: urls
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
        //console.log(JSON.stringify(response.data));
        _frames[i] = self.parseFrames(response.data, i);        
        let size = 0;
        _frames.map(function(frames_for_direction) {
          if(frames_for_direction && frames_for_direction.length > size) {
            size = frames_for_direction.length;
          }
          return null;
        });
        self.setState({
          frames: _frames,
          numOfFrames: size,
          loading: false
        });
        self.resetPlayback();
      }
      catch(e) {
        console.log(e);
      }
    });
  };

  parseFrames = (json, direction) => {
    let i = 0;
    let frames = [];
    json.map(function(frame) {
      let cars = [];
      frame.objects.map(function(car) {
        cars.push({
          y: Math.floor(car.bounding_box[1] / 2),
          x: Math.floor(car.bounding_box[0] / 2),
          type: car.type,
          direction: direction,
          tracking_id: car.tracking_id,
          speed: car.speed,
          ttc: car.ttc,
          distance: car.distance,
          key: i
        });
        i++;
        return null;
      });
      frames.push(cars);
      return null;
    });
    return frames;
  };

  getJunctions = callback => {
    let self = this;
    axios.post(SERVER_URL, {
      route: 'getJunctions'
    })
    .then(function (response) {
      try {
        response.data.map(function(junc) {
          junc.lat = parseFloat(junc.lat);
          junc.lon = parseFloat(junc.lon);
          return null;
        });
        self.setState({
          junctions: response.data
        });
        callback(response.data);
      }
      catch(e) {
        console.log(e);
        callback(e);
      }
    });
  };

  getDatasets = (junction_id, callback) => {
    let self = this;
    axios.post(SERVER_URL, {
      route: 'getDatasets',
      junction_id: junction_id
    })
    .then(function (response) {        
      try {
        let selectedJunction = self.state.selectedJunction;
        selectedJunction.datasets = response.data;
        self.setState({
          selectedJunction: selectedJunction
        });
        callback(response.data);
      }
      catch(e) {
        console.log(e);
        callback(e);
      }
    });
  };

  getDatasetFiles = dataset_id => {
    let self = this;
    axios.post(SERVER_URL, {
      route: 'getDatasetFiles',
      dataset_id: dataset_id,
      junction_id: self.state.selectedJunction ? self.state.selectedJunction.id : 0
    })
    .then(function (response) {
      console.log(response.data);
      try {
        let _frames = [];
        let i = 0;
        response.data.map(function(frames_for_direction) {
          _frames[i] = self.parseFrames(frames_for_direction, i);
          i++;
          return null;
        });
        let size = 0;
        _frames.map(function(frames_for_direction) {
          if(frames_for_direction.length > size) {
            size = frames_for_direction.length;
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
        self.resetPlayback();
        self.goToTab(TABS.main);
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
    let self = this;
    axios.post(SERVER_URL, {
      route: 'deleteJunction',
      junction_id: self.state.selectedJunction.id
    })
    .then(function (response) {        
      try {
        self.setState({
          selectedJunction: null
        });
        self.getJunctions(callback);
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

  createSimulation = (simulation) => {
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
          selectedJunction: simulation
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
    this.setState({
      tab: tab_index,
      isMenuOpen: false
    });
  };
  toggleMenu = () => {
    this.setState({
      isMenuOpen: !this.state.isMenuOpen
    });
  };
  selectJunction = junction => {
    if(junction) {
      junction.datasets = [];
      this.setState({
        selectedJunction: junction
      });
      this.getDatasets(junction.id, function() {});
    } else {
      this.setState({
        selectedJunction: null
      });
    }   
  };

  render() {
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
                      currentFrame={this.state.currentFrame}
                      playing={this.state.playing}
                      played ={this.state.played}
                      playbackRate={this.state.playbackRate} 
                      setPlaybackRate={this.setPlaybackRate.bind(this)}
                      loading={this.state.loading}
                      showSpeed={this.state.showSpeed}
                      showTTC={this.state.showTTC}
                      showDistance={this.state.showDistance}>
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
                              toggleShowDistance={this.toggleShowDistance.bind(this)}>
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
      </div>
    );
  }
}

export default App;
