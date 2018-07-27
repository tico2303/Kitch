import React from 'react';
import "./item.css";

class Item extends React.Component {
    render() {
        const title = this.props.item.name + " - " + this.props.item.price;
        const description = "Ingredients: " + this.props.item.ingredients;

        const img = {
            backgroundImage: `url('${this.props.item.img}')`
        }

        return (
            <div className="item"> 

                <div className="item-picture" style={img}> 
                </div>

                <div className="item-title"> 
                    { title }
                </div>

                <div className="item-description">
                    { description }
                </div>

            </div>
        );
    }
}

export default Item;
