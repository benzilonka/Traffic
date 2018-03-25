import React, { Component } from 'react';
import '../styles/Map.css';
//import car_image from '../images/car.png';
//import bus_image from '../images/bus.png';

class Vehicle extends Component {
    
  render() {
    var style = {
        top: (this.props.y),// - this.getVehicleDimensions(this.props.type).height / 2) + 'px',
        left: (this.props.x),// - this.getVehicleDimensions(this.props.type).width / 2) + 'px',
        backgroundColor: 'red',
        borderRadius: '50%',
        width: this.getVehicleDimensions(this.props.type).width + 'px',
        height: this.getVehicleDimensions(this.props.type).height + 'px'
    }
    let speed = null;
    if(this.props.showSpeed) {
      speed = (
        <span>speed: {this.props.speed.toFixed(2)} m/s</span>
      );
    }
    let ttc = null;
    if(this.props.showTTC) {
      if(this.props.ttc > -1) {
        ttc = (
          <span>ttc: {this.props.ttc.toFixed(2)} s</span>
        );
      }
      else {
        ttc = (
          <span>ttc: -</span>
        );
      }
    }
    let distance = null;
    if(this.props.showDistance) {
      distance = (
        <span>dis: {this.props.distance.toFixed(2)} m</span>
      );
    }
    let label = (
      <div className="vehicle-label">
           {speed} &nbsp;&nbsp; {ttc} &nbsp;&nbsp; {distance}
      </div>
    );

    return (
      <div className="vehicle" style={style}>
        {label}
      </div>
    );
  }

  getVehicleDimensions = type => {
    switch(type) {
      case 'car':
        return {
          width: 8,
          height: 8
        };
      case 'bus':
        return {
          width: 12,
          height: 12
        };
      default:
        return {
          width: 0,
          height: 0
        };
    }
  }
}

export default Vehicle;
