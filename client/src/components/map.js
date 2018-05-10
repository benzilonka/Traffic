/*jshint esversion: 6 */
import React, { Component } from 'react';
import Vehicle from './vehicle.js';
import TrafficLight from './TrafficLight.js';
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
};
let mapStyle = {      
  height: MAP_HEIGHT + 'px',
  width: MAP_WIDTH + 'px'
};
let lane0Style = {
  top: 0,
  left: MAP_HEIGHT / 2 - LANE_WIDTH / 2,
  width: LANE_WIDTH,
  height: MAP_HEIGHT,
};
let lane1Style = {
  top: 0,
  left: MAP_HEIGHT / 2 - LANE_WIDTH / 2,
  width: LANE_WIDTH,
  height: MAP_HEIGHT,
  transform: 'rotate(270deg)'
};
let lane2Style = {
  top: 0,
  left: MAP_HEIGHT / 2 - LANE_WIDTH / 2,
  width: LANE_WIDTH,
  height: MAP_HEIGHT,
  transform: 'rotate(180deg)'
};
let lane3Style = {
  top: 0,
  left: MAP_HEIGHT / 2 - LANE_WIDTH / 2,
  width: LANE_WIDTH,
  height: MAP_HEIGHT,
  transform: 'rotate(90deg)'
};
let lanesIntersect = {
  top: "50%",
  left: "50%",
  width: LANE_WIDTH,
  height: LANE_WIDTH,
  transform: "translate(-" + LANE_WIDTH / 2 + "px,-" + LANE_WIDTH / 2 + "px)"
}
let loadingStyle = {      
  backgroundImage: `url(${loading_gif})`,
  height: MAP_HEIGHT + 'px',
  width: MAP_WIDTH + 'px'
};

class Map extends Component { 
  
  render() {

    let vehicles = [[], [], [], []];
    let traffic_lights = [null, null, null, null];
    try {
      if(this.props.currentFrame != null) {
        let self = this;
        this.props.frames.map(function(directionFrames, index) {
          if(directionFrames != null && directionFrames.cars != null) {
            if(directionFrames.cars[self.props.currentFrame] != null) {
              let _vehicles = directionFrames.cars[self.props.currentFrame].map(function(vehicle) {
                let x = vehicle.x;
                let y = vehicle.y;
                let highlight = false;
                if(self.props.highlightVehicle != null) {
                  if(vehicle.tracking_id === self.props.highlightVehicle) {
                    highlight = true;
                  }
                }
                return (
                    <Vehicle key={vehicle.key} 
                             x={x}
                             y={y-10} 
                             type={vehicle.type}
                             speed={vehicle.speed}
                             ttc={vehicle.ttc}
                             distance={vehicle.distance}
                             showSpeed={self.props.showSpeed}
                             showTTC={self.props.showTTC}
                             showDistance={self.props.showDistance}
                             highlight={highlight}
                             >
                    </Vehicle>
                );
              });
              vehicles[index] = _vehicles;
            }
          }
          if(directionFrames != null && directionFrames.traffic_lights != null) {
            if(directionFrames.traffic_lights[self.props.currentFrame] != null) {
              let t = directionFrames.traffic_lights[self.props.currentFrame];
              traffic_lights[index] = (
                <TrafficLight light={t}></TrafficLight>
              );
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
    
    let loading = '';
    if(this.props.loading) {
      loading = (
        <div className="Loading" style={loadingStyle}></div>
      );
    }


    return (
      <div>
        <div className="Map" style={mapStyle}>
          <div className="Map-center"></div>
          <div className="lanes-disp">
            <div style={lane0Style} className="lane-disp">
            </div>
            <div style={lane1Style} className="lane-disp">
            </div>
            <div style={lane2Style} className="lane-disp">
            </div>
            <div style={lane3Style} className="lane-disp">
            </div>
            <div style={lanesIntersect}>
            </div>
          </div>
          <div className="lanes-cont">
            <div className="lane" style={lane0Style}>
              {vehicles[DIRECTIONS.TOP_TO_DOWN]}
              {traffic_lights[0]}
            </div>
            <div className="lane" style={lane1Style}>
              {vehicles[DIRECTIONS.RIGHT_TO_LEFT]}
              {traffic_lights[1]}
            </div>
            <div className="lane" style={lane2Style}>
              {vehicles[DIRECTIONS.DOWN_TO_UP]}
              {traffic_lights[2]}
            </div>
            <div className="lane" style={lane3Style}>
              {vehicles[DIRECTIONS.LEFT_TO_RIGHT]}
              {traffic_lights[3]}
            </div>
          </div>
        </div>
        {loading}
      </div>
    );
  }
}

export default Map;
