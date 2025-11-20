import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8080"   // cloud orchestrator
});

export const fetchEvents = () => API.get("/events");
export const fetchSignalStatus = () => API.get("/status"); // if added later
