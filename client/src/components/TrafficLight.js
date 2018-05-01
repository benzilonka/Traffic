/*jshint esversion: 6 */
import React, { Component } from 'react';
import '../styles/Map.css';
//import car_image from '../images/car.png';
//import bus_image from '../images/bus.png';

class TrafficLight extends Component {
    
  render() {
    let leftStyle = {
        backgroundColor: this.props.light.left
    };
    let forwardStyle = {
        backgroundColor: this.props.light.forward
    };
    let rightStyle = {
        backgroundColor: this.props.light.right
    };
    let left = (<div style={leftStyle}></div>);
    let forward = (<div style={forwardStyle}></div>);
    let right = (<div style={rightStyle}></div>);
    return (
      <div className="traffic-light">
        {left}{forward}{right}
      </div>
    );
  }

}

export default TrafficLight;
