import React from "react";


function Nav(){
    return (
        <nav class="navbar ">
          <div id="navbar" class="container container-nav">
            <h2>
              <a class="brand-name" href="/">
                Catalog
              </a>
            </h2>

            <form action="/auth/login">
              <button
                type="submit"
                id="sign-in"
               
                class="btn btn-primary"
              >
                Sign in
              </button>
            </form>
          </div>
        </nav>
    )
}


export default Nav;