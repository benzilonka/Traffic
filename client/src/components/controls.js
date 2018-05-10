/*jshint esversion: 6 */
import React, { Component } from 'react';
import {
    Container, 
    Row, 
    Col,
    Button
  } from 'reactstrap';
import { PlayButton, PauseButton, ProgressBar } from 'react-player-controls';
import '../styles/Controls.css';
import '../styles/video_controls.css';
import 'react-select/dist/react-select.css';

const FRAME_TIME = 0.066666666666;

class Controls extends Component {

    

    render() {
        let playPause = (
            <PlayButton isEnabled={true} onClick={this.props.playPause} />
        );
        if(this.props.playing) {
            playPause = <PauseButton type="button" onClick={this.props.playPause} />
        }

        let time_passed = 0;
        try {
            let date_time_passed = new Date(null);
            date_time_passed.setSeconds(this.props.played * FRAME_TIME * 1000); // specify value for SECONDS here
            time_passed = date_time_passed.toISOString().substr(11, 8);
        }
        catch(e) {
            console.log(e);
        }

        let currJunction = (<span></span>);        
        if(typeof this.props.selectedJunction === 'object' && this.props.selectedJunction != null) {
            let currDataset = (<span></span>);
            if(typeof this.props.selectedJunction.currentDataset === 'number' && this.props.selectedJunction.currentDataset != null) {
                if(this.props.selectedJunction.datasets != null) {
                    let self = this;
                    this.props.selectedJunction.datasets.map(function(dataset) {
                        if(dataset.id === self.props.selectedJunction.currentDataset) {
                            currDataset = (
                                <span>- {dataset.name}</span>
                            );
                        }
                        return null;
                    });
                }
            }
            currJunction = (
                <Container id="junction-controls-title">
                    <Row>
                        <Col xs={12}>
                            <p>
                                <strong>Showing Junction {this.props.selectedJunction.name} {currDataset}</strong>
                                <Button color="primary" onClick={(e) => this.props.resetSelection()}>Reset</Button>
                            </p>
                        </Col>   
                    </Row>
                </Container>
            );
        }

        return (
          <div className="Controls player">
            {currJunction}
            <Container>
                    <Row>
                        <Col xs={2}>
                            {playPause}
                        </Col>
                        <Col xs={6}>
                            <ProgressBar
                                totalTime={1}
                                currentTime={this.props.played}
                                isSeekable={true}
                                onSeek={this.props.onSeekChange}
                                onSeekStart={this.props.onSeekMouseDown}
                                onSeekEnd={this.props.onSeekMouseUp}
                            />
                            <small>{time_passed}</small>
                        </Col>
                        <Col xs={4}>
                            <Row>
                                <Col xs={8}>
                                    <ProgressBar
                                        totalTime={10}
                                        currentTime={this.props.playbackRate}
                                        isSeekable={true}
                                        onSeek={this.props.setPlaybackRate}
                                    />
                                </Col>
                                <Col xs={4}>
                                    <p className="speed"> x{(''+this.props.playbackRate).substring(0, Math.min(4, (''+this.props.playbackRate).length))}</p>
                                </Col>
                            </Row>
                        </Col>
                    </Row>
                </Container>
                <Container>
                    <Row>
                        <Col xs={12}>
                            <p></p>
                        </Col>
                    </Row>
                </Container>
                <Container>
                    <Row>
                        <Col xs={12}>
                            <Button color="danger" onClick={(e) => this.props.toggleShowTTC()}>Toggle TTC</Button>
                            &nbsp;
                            <Button color="danger" onClick={(e) => this.props.toggleShowSpeed()}>Toggle Speed</Button>
                            &nbsp;
                            <Button color="danger" onClick={(e) => this.props.toggleShowDistance()}>Toggle Distance</Button>
                        </Col>   
                    </Row>
                </Container>
          </div>
        );
      }
    }
    
    export default Controls;



