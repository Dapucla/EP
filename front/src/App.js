import logo from './logo.svg';
import React, {Component} from "react";
import './App.css';
import axios from "axios";
import './base.css';

class App extends React.Component{
    state = {
        categories: []
    }

  componentDidMount() {
    let data;

    axios.get('http://ip4sem.std-972.ist.mospolytech.ru/api/smartphones/')
    .then(res => {
      data = res.data;
      this.setState({
          categories: data
      });
    })
    .catch(err => {})
      console.log(this.state.categories)
  }


    render() {
        return (
            <div className="App">
                <div className="contact">
                    <ul className="responsive-table">
                        <li className="table-header">
                            <div className="col col-1">Id</div>
                            <div className="col col-2">Название</div>
                            <div className="col col-3">Описание</div>
                            <div className="col col-4">Цена</div>
                        </li>
                        {this.state.categories.map(c =>
                            <li className="table-row" key={c.id}>
                                <div className="col col-1">{c.id}</div>
                                <div className="col col-2">{c.title}</div>
                                <div className="col col-3">{c.description}</div>
                                <div className="col col-4">{c.price}</div>
                            </li>
                        )}
                    </ul>
                </div>

            </div>
        );
    }


}

export default App;
