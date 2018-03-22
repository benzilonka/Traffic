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

    return (
      <div className="vehicle" style={style}>        
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
