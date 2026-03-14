import { Link } from "react-router-dom";

function Navbar() {

  return (

    <nav style={{padding:"10px",background:"#222",color:"#fff"}}>

      <Link to="/" style={{marginRight:"15px",color:"#fff"}}>Login</Link>
      <Link to="/register" style={{marginRight:"15px",color:"#fff"}}>Register</Link>
      <Link to="/assessment" style={{marginRight:"15px",color:"#fff"}}>Assessment</Link>

    </nav>

  );

}

export default Navbar;