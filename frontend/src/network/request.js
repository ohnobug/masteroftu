import axios from "axios";
import { Navigate } from "react-router";



const request = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:3000",
    withCredentials: true,
    headers: {
        "Content-Type": "application/json"
    },
    responseType: "json",
});


export const getData = (url, data) => {
    let token = localStorage.getItem("token");

    return new Promise((resolve, reject) => {
        request.post(url, data, {
            headers: {
                "Authorization": token ? "bearer " + token : null
            }
        })
            .then((response) => {
                resolve(response.data);
            }).catch((error) => {
                reject(error);
                console.error("Error fetching data:", error);
            });
    });
};

