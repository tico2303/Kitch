import React from 'react';
import "./item.css";

class Item extends React.Component {
    render() {
        const title = this.props.item.name + " - " + this.props.item.price;
        const description = "Ingredients: " + this.props.item.ingredients;
        const img = {
            backgroundImage: `url('${this.props.item.img}')`
        }
        /*
        const img = {
            backgroundColor:'red'
        };
        const ttl_style = {
            backgroundColor:'green'
        };
        const des_style = {
            backgroundColor:'blue'
        };
        const item_style = {
            backgroundColor:'blue'
        };
        */
        return (
            <div className="item" > 

            <a href="/item/">
                <div className="item-picture" style={img}> 

                </div>
            </a>

                <div className="item-description">
                    { description }
                </div>

            </div>

        );
    }
}

export default Item;
