/*jshint esversion: 6 */
import React, { Component } from 'react';
import ReactPlayer from 'react-player';
import '../styles/Videos.css';

class Video extends Component {

    seekTo = n => {    
        if(this.refs.player) {
            this.refs.player.seekTo(n);
        }
    }

    render() {
        if(this.props.url == null) {
            return (
                <div className="Video">
                    <p></p>  
                </div>
            );
        }
        else {
            return (
                <div className="Video">
                    <ReactPlayer
                        className="video-player"
                        ref="player"
                        width='100%'
                        height='100%'
                        loop={false}
                        url={this.props.url}
                        playing={this.props.playing}
                        playbackRate={this.props.playbackRate}
                        onProgress={this.props.onProgress}                         
                        onEnded={this.props.onEnded}   
                        />
                    <p></p>
                </div>
            );
        }
    }
}

export default Video;
