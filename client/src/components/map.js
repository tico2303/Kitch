import React from 'react';
import Map, { GoogleApiWrapper, Marker } from 'google-maps-react';

class SimpleMapPage extends React.Component {
    render() {
        const style = {
            width: '100%',
            height: '100%'
        }

    return (
      <Map google={this.props.google} style={style} zoom={12} center={this.props.current_center}>
                {this.props.items.map( (item) =>{ return <Marker position={this.props.current_center} title={item.name}/> })}
      </Map>
    );
  }
}


export default GoogleApiWrapper({
  apiKey: 'AIzaSyAbZbXeWZwouePtArEZ7V9rPUWBgDx7xBI',
})(SimpleMapPage);
