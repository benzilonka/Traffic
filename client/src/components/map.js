import React, { Component } from 'react';
import Vehicle from './vehicle.js';
import '../styles/Map.css';
import loading_gif from '../images/loading.gif';

const MAP_HEIGHT = 735;
const MAP_WIDTH = 735;
const LANE_WIDTH = 70;
const DIRECTIONS = {
  TOP_TO_DOWN: 0,
  RIGHT_TO_LEFT: 1,
  DOWN_TO_UP: 2,
  LEFT_TO_RIGHT: 3
}

class Map extends Component { 
  
  render() {
    let mapStyle = {      
      height: MAP_HEIGHT + 'px',
      width: MAP_WIDTH + 'px'
    };
    let vehicles = [[], [], [], []];
    try {
      if(this.props.currentFrame != null) {
        let self = this;
        this.props.frames.map(function(directionFrames, index) {
          if(directionFrames != null) {
            if(directionFrames[self.props.currentFrame] != null) {
              let _vehicles = directionFrames[self.props.currentFrame].map(function(vehicle) {
                let x = vehicle.x;
                let y = vehicle.y;
                if(y > MAP_HEIGHT / 2 - LANE_WIDTH / 2 - 10) {
                  return null;
                }
                return (
                    <Vehicle key={vehicle.key} 
                             x={x}
                             y={y} 
                             type={vehicle.type}
                             speed={vehicle.speed}
                             ttc={vehicle.ttc}
                             distance={vehicle.distance}
                             showSpeed={self.props.showSpeed}
                             showTTC={self.props.showTTC}
                             showDistance={self.props.showDistance}
                             >
                    </Vehicle>
                );
              });
              vehicles[index] = _vehicles;
            }
          }
          return null;
        });  
      }       
    }
    catch(e) {
      console.log(e);
    }   
    //console.log(vehicles);
    let lane0Style = {
      top: 0,
      left: MAP_HEIGHT / 2 - LANE_WIDTH / 2,
      width: LANE_WIDTH,
      height: MAP_HEIGHT / 2 - LANE_WIDTH / 2,
    };
    let lane1Style = {
      top: MAP_HEIGHT / 4 + LANE_WIDTH / 4,
      left: LANE_WIDTH * 2 - 10,
      width: LANE_WIDTH,
      height: MAP_HEIGHT / 2 - LANE_WIDTH / 2,
      transform: 'rotate(270deg)'
    };
    let lane2Style = {
      top: MAP_HEIGHT / 2 + LANE_WIDTH / 2,
      left: MAP_HEIGHT / 2 - LANE_WIDTH / 2,
      width: LANE_WIDTH,
      height: MAP_HEIGHT / 2 - LANE_WIDTH / 2,
      transform: 'rotate(180deg)'
    };
    let lane3Style = {
      top: MAP_HEIGHT / 4 + LANE_WIDTH / 4,
      left: MAP_HEIGHT / 2 + LANE_WIDTH * 2.4,
      width: LANE_WIDTH,
      height: MAP_HEIGHT / 2 - LANE_WIDTH / 2,
      transform: 'rotate(90deg)'
    };
    let loading = '';
    let loadingStyle = {      
      backgroundImage: `url(${loading_gif})`,
      height: MAP_HEIGHT + 'px',
      width: MAP_WIDTH + 'px'
    };
    if(this.props.loading) {
      loading = (
        <div className="Loading" style={loadingStyle}></div>
      );
    }
    return (
      <div>
        <div className="Map" style={mapStyle}>
          <div className="lanes-cont">
            <div className="lane" style={lane0Style}>
              {vehicles[DIRECTIONS.TOP_TO_DOWN]}
            </div>
            <div className="lane" style={lane1Style}>
              {vehicles[DIRECTIONS.RIGHT_TO_LEFT]}
            </div>
            <div className="lane" style={lane2Style}>
              {vehicles[DIRECTIONS.DOWN_TO_UP]}
            </div>
            <div className="lane" style={lane3Style}>
              {vehicles[DIRECTIONS.LEFT_TO_RIGHT]}
            </div>
          </div>
          <div className="lanes-disp">
            <div style={lane0Style}>
            </div>
            <div style={lane1Style}>
            </div>
            <div style={lane2Style}>
            </div>
            <div style={lane3Style}>
            </div>
          </div>
        </div>
        {loading}
      </div>
    );
  }
}

export default Map;
