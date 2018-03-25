import React, { Component } from 'react';
import { Container, Row, Col } from 'reactstrap';
import axios from 'axios';
import logo from './images/logo.svg';
import Videos from './components/videos.js';
import Map from './components/map.js';
import Controls from './components/controls.js';
import './styles/App.css';

const FRAME_TIME = 0.066666666666;
const SECOND = 1000;

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
      showDistance: false
    }
  }

  toggleShowSpeed = () => {
    this.setState({
      showSpeed: !this.state.showSpeed
    });
  }
  toggleShowTTC = () => {
    this.setState({
      showTTC: !this.state.showTTC
    });
  }
  toggleShowDistance = () => {
    this.setState({
      showDistance: !this.state.showDistance
    });
  }

  playPause = () => {
    if(this.state.currentFrame == null || this.state.urls.filter(url => url != null).length === 0) {
      return false;
    }
    if(!this.state.playing) {
      var timeout = FRAME_TIME * this.state.playbackRate;
      let self = this;
      var playFrame = function() {
        if(self.state.playing) {
          self.setState({
            currentFrame: self.state.currentFrame + 1
          });
          timeout = FRAME_TIME / self.state.playbackRate;
          setTimeout(playFrame, timeout * SECOND);
        }
      }
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
  }
  setPlaybackRate = rate => {
    this.setState({ playbackRate: rate });
  }
  onSeekMouseDown = e => {
  }
  onSeekChange = seekTo => {
    this.setState({ 
      played: seekTo,
      currentFrame: Math.floor(this.state.numOfFrames * seekTo)
    });
    this.refs.videos.seekTo(seekTo);
  }
  onSeekMouseUp = e => {
  }
  onProgress = state => {
    if (!this.state.seeking) {
      this.setState(state);
    }
  }
  
  readVideoFile = (i, event) => {
    const input = event.target;
    const url = URL.createObjectURL(input.files[0]);
    let urls = this.state.urls;
    urls[i] = url;
    this.setState({
      urls: urls
    });
  }

  loadFiles = (json, meta, i) => {
    this.setState({
      loading: true
    });
    let self = this;
    axios.post('http://localhost:8080/', {
      route: 'getFrames',
      json: json,
      meta: meta
    })
    .then(function (response) {        
      try {
        let _frames = self.state.frames;
        _frames[i] = self.parseFrames(response.data, i);
        self.setState({
          frames: _frames,
          currentFrame: 0,
          numOfFrames: _frames[i].length,
          loading: false
        });
      }
      catch(e) {
        console.log(e);
      }
    });
  }

  parseFrames = (json, direction) => {
    let i = 0;
    let frames = [];
    json.map(function(frame) {
      let cars = [];
      frame['objects'].map(function(car) {
        cars.push({
          y: Math.floor(car.bounding_box[1] / 2),
          x: Math.floor(car.bounding_box[0]),
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
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">NoTraffic</h1>
        </header>
        <Container fluid>
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
      </div>
    );
  }
}

export default App;
