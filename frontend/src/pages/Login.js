import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";

function Login(){

  const navigate = useNavigate();

  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");

  const handleLogin = async () => {

    try{

      const res = await API.post("/login",{
        email,
        password
      });

      if(res.data.user_id){

        localStorage.setItem("user_id",res.data.user_id);

        navigate("/assessment");

      }else{

        alert("Invalid Login");

      }

    }catch(error){

      alert("Server Error");

    }

  };

  return(

    <div className="card">

      <h2>Login</h2>

      <input
        placeholder="Email"
        onChange={(e)=>setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        onChange={(e)=>setPassword(e.target.value)}
      />

      <button onClick={handleLogin}>Login</button>

    </div>

  );

}

export default Login;