import axios from "axios";

let token = localStorage.getItem("token");

const request = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:3000",
    withCredentials: true,
    headers: {
        "Content-Type": "application/json"
    },
    responseType: "json",
});

if (token) {
    request.headers['Authorization'] = "bearer " + token
}

export const getData = (url, data) => {
    return new Promise((resolve, reject) => {
        request.post(url, data)
            .then((response) => {
                resolve(response.data);
            }).catch((error) => {
                reject(error);
                console.error("Error fetching data:", error);
            });
    });
};

