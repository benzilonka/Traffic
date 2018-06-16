/*jshint esversion: 6 */
import React, { Component } from 'react';
import '../styles/Map.css';
//import car_image from '../images/car.png';
//import bus_image from '../images/bus.png';

class Vehicle extends Component {

  render() {
    
    let x = this.props.x;
    if(x < 17) {
      x *= 7 / 4;
    }
    var style = {
        top: (this.props.y),// - this.getVehicleDimensions(this.props.type).height / 2) + 'px',
        left: x,// - this.getVehicleDimensions(this.props.type).width / 2) + 'px',
        backgroundColor: 'blue',
        borderRadius: '50%',
        width: this.getVehicleDimensions(this.props.type).width + 'px',
        height: this.getVehicleDimensions(this.props.type).height + 'px'
    };
    if(this.props.highlight) {
      style.backgroundColor = 'deeppink';
      style.zIndex = 2;
    }
    let speed = null;
    if(this.props.showSpeed && this.props.speed) {
      speed = (
        <div>speed: {this.props.speed.toFixed(2)} m/s</div>
      );
    }
    let ttc = null;
    if(this.props.showTTC) {
      if(this.props.ttc && this.props.ttc > -1) {
        ttc = (
          <div>ttc: {this.props.ttc.toFixed(2)} s</div>
        );
      }
      else {
        ttc = (
          <div>ttc: -</div>
        );
      }
    }
    let distance = null;
    if(this.props.showDistance && this.props.distance) {
      distance = (
        <div>dis: {this.props.distance.toFixed(2)} m</div>
      );
    }
    let passed_in_red = null;
    if(this.props.passed_in_red) {
      passed_in_red = (
        <div className="red-light-alert">RED LIGHT!</div>
      );
    }
    let label = (
      <div className="vehicle-label">
           {passed_in_red}{speed}{ttc}{distance}
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
      case 'bus':
      return {
        width: 5,
        height: 12
      };
      case 'car':
      default:
        return {
          width: 4,
          height: 8
        };
    }
  }
}

export default Vehicle;
