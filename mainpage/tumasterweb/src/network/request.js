import axios from "axios";

const request = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:3000",
    withCredentials: true,
    headers: {
        "Content-Type": "application/json",
    },
});

export const getData = (url) => {
    return new Promise((resolve, reject) => {
        request.post(url)
            .then((response) => {
                resolve(response.data);
            }).catch((error) => {
                reject(error);
                console.error("Error fetching data:", error);
            });
    });
};

