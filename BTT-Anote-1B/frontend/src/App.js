import Chatbot from "./Chatbot";
import { BrowserRouter as Router} from "react-router-dom";
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';

function App() {
    return (
      <Router>
        <div className="border-[#9B9B9B] border-[4px] mx-auto md:w-4/12 rounded-2xl mt-20">
        <Chatbot />
        </div>
      </Router>
    );
}

export default App;
