/*jshint esversion: 6 */
import React, { Component } from 'react';
import Vehicle from './vehicle.js';
import Statistics from './statistics.js';
import TrafficLight from './TrafficLight.js';
import '../styles/Map.css';

const MAP_HEIGHT = 735;
const MAP_WIDTH = 735;
const LANE_WIDTH = 70;
const LANE_HEIGHT = 735;
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
  height: LANE_HEIGHT,
};
let lane1Style = {
  top: 0,
  left: MAP_HEIGHT / 2 - LANE_WIDTH / 2,
  width: LANE_WIDTH,
  height: LANE_HEIGHT,
  transform: 'rotate(270deg)'
};
let lane2Style = {
  top: 0,
  left: MAP_HEIGHT / 2 - LANE_WIDTH / 2,
  width: LANE_WIDTH,
  height: LANE_HEIGHT,
  transform: 'rotate(180deg)'
};
let lane3Style = {
  top: 0,
  left: MAP_HEIGHT / 2 - LANE_WIDTH / 2,
  width: LANE_WIDTH,
  height: LANE_HEIGHT,
  transform: 'rotate(90deg)'
};
let lanesIntersect = {
  top: "50%",
  left: "50%",
  width: LANE_WIDTH,
  height: LANE_WIDTH,
  transform: "translate(-" + LANE_WIDTH / 2 + "px,-" + LANE_WIDTH / 2 + "px)"
};


class Map extends Component {

  constructor(props) {
    super(props);
    this.state = {
      show_vehicle_stats: false,
      vehicle_statistics: [null, null, null, null]
    };
  } 

  showVehicleStatistics = () => {
    this.setState({
      show_vehicle_stats: true
    });
  }

  hideVehicleStatistics = () => {
    this.setState({
      show_vehicle_stats: false
    });
  }

  toggleVehicleStatistics = (statistics, i, tracking_id) => {
    let stats = this.state.vehicle_statistics;
    if(JSON.stringify(stats[i]) === JSON.stringify(statistics)) {
      stats[i] = null;
    } else {
      stats[i] = statistics;
    }
    this.setState({
      vehicle_statistics: stats
    });
    
    this.props.highlightVehicleFunc(tracking_id);
  }

  shouldComponentUpdate = (nextProps, nextState) => {
      return !this.state.mouseDown;
  }
  onMouseDown = () => {
    this.setState({
      mouseDown: true
    });
  }
  onMouseUp = () => {
    this.setState({
      mouseDown: false
    });
  }
  vehiclePassedInRed = (currFrame, vehicle, cars) => {
    if(vehicle.passed_in_red) {
      return true;
    }
    const MAX = 2;
    let c = 0;
    for(let i = currFrame - 1; i >= 0; i--) {
      for(let j = 0; j < cars[i].length; j++) {
        if(cars[i][j].tracking_id === vehicle.tracking_id) {
          if(cars[i][j].passed_in_red) {
            return true;
          }
        }
      }
      if(c++ > MAX) {
        break;
      }
    }
    c = 0;
    for(let i = currFrame + 1; i < cars.length; i++) {
      for(let j = 0; j < cars[i].length; j++) {
        if(cars[i][j].tracking_id === vehicle.tracking_id) {
          if(cars[i][j].passed_in_red) {
            return true;
          }
        }
      }
      if(c++ > MAX) {
        break;
      }
    }
    return false;
  }

  render = () => {    
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
                let vehicle_stats = null;
                if(self.props.statistics[index] != null) {
                  vehicle_stats = self.props.statistics[index].vehicle_info[vehicle.tracking_id];
                }
                return (
                  <div 
                      onClick={(e) => self.toggleVehicleStatistics(vehicle_stats, index, vehicle.tracking_id)}
                      onMouseDown={self.onMouseDown}
                      onMouseUp={self.onMouseUp}
                      onMouseLeave={self.onMouseUp}
                      key={vehicle.key}
                      >
                    <Vehicle
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
                             passed_in_red={self.vehiclePassedInRed(self.props.currentFrame, vehicle, directionFrames.cars)}
                             >
                    </Vehicle>
                  </div>
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
  
    let vehicle_statistics = [];
    for(let i = 0; i < 4; i++) {
      if(this.state.vehicle_statistics[i] != null) {
        let stats = [];
        let j = 0;
        for (let key in this.state.vehicle_statistics[i]) {
          let value = this.state.vehicle_statistics[i][key];
          if(!isNaN(value)) {
            value = parseFloat(value, 10).toFixed(2);
          }
          stats.push({
              name: key,
              value: value,
              key: j++
          });
        }
        vehicle_statistics[i] = stats.map(function(stat) {
            return (
                <p key={stat.key}>{stat.name}: {stat.value}</p>
            )
        });
  
        let statisticsStyle= {            
            transform: 'rotate(' + (90 * i) + 'deg)'
        };
        vehicle_statistics[i] = (
          <div className="vehicle-statistics" style={statisticsStyle} onClick={(e) => this.toggleVehicleStatistics(null, i, -1)}>       
            {vehicle_statistics[i]} 
          </div>
        );
      }
    }


    return (
      <div>
        <div className="Map" style={mapStyle}>
          <div className="Map-center"></div>
          <div className="lanes-disp">
            <div style={lane0Style} className="lane-disp">
              <Statistics statistics={this.props.statistics[0]} i={0}></Statistics>
              {vehicle_statistics[0]}
            </div>
            <div style={lane1Style} className="lane-disp">
              <Statistics statistics={this.props.statistics[1]} i={1}></Statistics>              
              {vehicle_statistics[1]}
            </div>
            <div style={lane2Style} className="lane-disp">
              <Statistics statistics={this.props.statistics[2]} i={2}></Statistics>              
              {vehicle_statistics[2]}
            </div>
            <div style={lane3Style} className="lane-disp">
              <Statistics statistics={this.props.statistics[3]} i={3}></Statistics>              
              {vehicle_statistics[3]}
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
      </div>
    );
  }
}

export default Map;
