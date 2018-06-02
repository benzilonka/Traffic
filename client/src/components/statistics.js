/*jshint esversion: 6 */
import React, { Component } from 'react';
import '../styles/Controls.css';
import info_icon from '../images/baseline-info-24px.svg';

class Statistics extends Component {   
    constructor(props) {
      super(props);
      this.state = {
        isMouseInside: false
      };
    } 

    mouseEnter = () => {
        this.setState({ isMouseInside: true });
    }
    mouseLeave = () => {
        this.setState({ isMouseInside: false });
    }

    render() {

        let statistics = (<span></span>);

        let statisticsStyle= {            
            transform: 'rotate(' + (90 * this.props.i) + 'deg)'
        };
            

        let stats_icon_style = {      
            backgroundImage: `url(${info_icon})`,
            transform: 'rotate(' + (90 * this.props.i) + 'deg)'
        }

        if(this.props.statistics != null) {
            let stats = [];
            let i = 0;
            if(this.state.isMouseInside) {
                for (let key in this.props.statistics) {
                    if(key === 'vehicle_info') {
                        continue;
                    }
                    let value = this.props.statistics[key];
                    if(!isNaN(value)) {
                        value = parseFloat(value, 10).toFixed(2);
                    }
                    stats.push({
                        name: key,
                        value: value,
                        key: i++
                    });
                }
                
                statistics = stats.map(function(stat) {
                    return (
                        <p key={stat.key}>{stat.name}: {stat.value}</p>
                    )
                });
            }

            let show_stats = (<span></span>);
            if(!this.state.isMouseInside) {
                show_stats = (
                    <div className="show-stats" style={stats_icon_style} onMouseEnter={this.mouseEnter}></div>
                );
            }

            return (
                <div className="statistics"  onMouseLeave={this.mouseLeave}>
                    {show_stats}
                    <div className="text" style={statisticsStyle}>
                        {statistics}
                    </div>
                </div>
            );
        }
        return (
            <span></span>
        );
    }
}

export default Statistics;