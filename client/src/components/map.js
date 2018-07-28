import React from 'react';
import {Map, GoogleApiWrapper, Marker, InfoWindow} from 'google-maps-react';

class SimpleMapPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            activeMarker:{},
            selectedPlace:{}
        };
        console.log("SimpleMapPage Constructor Initialized");
    }
    render() {
        const style = {
            width: '100%',
            height: '100%'
        }
    
    const mouseOverMarker = (props, marker)=>{
        console.log("props: ", Object.keys(props));
        console.log("props title: ",props.title);
        console.log("props title: ",marker);
        console.log("mouseOverMarker called");
        this.setState(
            {
                selectedPlace:props.title,
                activeMarker:marker
            }
        )
    };
    return (
      <Map google={this.props.google} style={style} zoom={9} center={this.props.current_center}>
                {this.props.items.map( (item) =>{ 
                    const location = {lat:item["lat"], lng:item["lng"]}
                    console.log("Marker item location:",location)
                    return( 
                        <Marker 
                            key={item.name}
                            onClick={mouseOverMarker}
                            position={location} 
                            title={item.name} />
                    
                    );
                                                }
                                      )
                }
      </Map>
    );
  }//end render
}//end SimpleMapPage


export default GoogleApiWrapper({
  apiKey: 'AIzaSyAbZbXeWZwouePtArEZ7V9rPUWBgDx7xBI',
})(SimpleMapPage);
