import React from 'react';
import Item from './item';
import SimpleMapPage from './map';
import '../App.css';

class SearchPage extends React.Component {   
    constructor(props) {
        super(props);
        this.state = {
            items: [],
            // 48.853642, 2.365598
            loc: {lat: 48.853642, lng: 2.365598}
        };
        console.log("Constructor Initialized");
    }


    componentDidMount() {

        function urlbuilder(route,json_data){
            const url =  'http://localhost:5000/api/v1/';
            let ret = [];
            ret.push(url + route + '?');
            for (let d in json_data)
                ret.push(encodeURIComponent(d) + '=' + encodeURIComponent(json_data[d]));
            return ret.join('&');
        }

        console.log("APP COMPONENT MOUNTED");
        fetch(urlbuilder('item/radius',{"lat":34.023891,"lng":-117.619385,"radius":10000,"number_of_results":20}))
        .then(response => {
            return response.json();
        }) // parses response to JSON
        .catch(error => console.error(`Fetch Error =\n`, error))
        .then( (data) => {
            console.log("data",data["items"]);
            this.setState({
                items:data["items"]
            })});

    }


    render() {

    // Show a map centered at (position.coords.latitude, position.coords.longitude).
    const showMap = (position) => {
        const user_location = {lat: position.coords.latitude, lng: position.coords.longitude};
        this.setState({loc:user_location});
    }

    // One-shot position request.
    navigator.geolocation.getCurrentPosition(showMap);

    return (


      <div className="app">

        <div className="main">

            <div className="search">
            </div>

            <div className="items">
                {this.state.items.map((item)=>{ return <Item key={item.name} item={item}/> })}
            </div>

        </div>

        <div className="map">
            <SimpleMapPage items={this.state.items} zoom={11} current_center={this.state.loc} />
        </div>

      </div>
    );
  }
}
export default SearchPage;
