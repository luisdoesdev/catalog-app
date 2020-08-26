import React from "react";

// Components
import Nav from '../components/Nav'

class Home extends React.Component {
  render() {
    const name = "hello";
    return (

       <div>
       <Nav/>

      <div className="shopping-list">
       
        <div class="container container-content">
          <div class="row">
            <div class="category col-lg-2 col-sm-4">
              <h2>Categories</h2>

              <li>
                <a href="/catalog/Soccer/items">Soccer</a>
              </li>

              <li>
                <a href="/catalog/Skateboard/items">Skateboard</a>
              </li>
            </div>
            <div class="items col-sm-6">
              <ul>
                <h2 >
                  Latest Items
                </h2>

                <li>
                  <a href="/catalog/Soccer/%20Soccer%20Ball"> Soccer Ball</a>
                  <span >(Soccer)</span>
                </li>

                <li>
                  <a href="/catalog/Soccer/Soccer%20Shoes">Soccer Shoes</a>
                  <span >(Soccer)</span>
                </li>

                <li>
                  <a href="/catalog/Skateboard/Deck">Deck</a>
                  <span >(Skateboard)</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
        <footer class="footer text-right ">
          <div class="container-fluid">
            <span class="text-muted pr-2">
              ©
              <a
                href="https://github.com/letorruella"
              >
               
                Luis E Torruella
              </a>
            </span>
          </div>
        </footer>
      </div>
      </div>
    );
  }
}

export default Home;
