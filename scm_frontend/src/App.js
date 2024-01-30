import Navigation from './js/navigation';
import Dashboard from './js/dashboard/dashboard';
import Assets from './js/assets/assets';
import Properties from './js/properties/properties';
import Controls from './js/controls/controls';
import Constraints from './js/constraints/constraints';
import Tags from './js/tags/tags';

import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

function App() {
    let page;
    if (window.location.pathname == '/') {
      page = <Dashboard />
    } else if (window.location.pathname == '/assets') {
      page = <Assets />
    } else if (window.location.pathname == '/properties') {
      page = <Properties />
    } else if (window.location.pathname == '/controls') {
      page = <Controls />
    } else if (window.location.pathname == '/constraints') {
      page = <Constraints />
    } else if (window.location.pathname == '/tags') {
      page = <Tags />
    }

    return (
      <>
        <header>
          <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" />
        </header>
        <nav>
          <Navigation />
        </nav>
        <body>
          <div class="content">
            {page}
          </div>
        </body>
      </>
    );
}

export default App;
