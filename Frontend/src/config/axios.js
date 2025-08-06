import axios from "axios";

const agentAxios = axios.create({
  baseURL: "http://localhost:5000/api/agent",
  withCredentials:true,
  headers: {
    "agent-key": "erl_doiadnafkfsnsfkjnsfeionnb_fnfsoefnionfnsfkjdf",
    "Content-Type": "application/json"
  }
});

export default agentAxios;
