import http from 'k6/http';
import { data } from './data.js';


export default function createTestUser(environment){
    const url = `${data[environment].api_service_base_url}/user`;
    const headers = {
        "Content-Type": "application/json",
    };
    const randomString = Math.random().toString(36).substring(7);
    const body = JSON.stringify({
        email: `user_${randomString}@example.com`,
        name: "User Name",
        surname: "User Surname"
    });

    const response = http.post(url, body, { headers });
    if (response.status !== 201) {
      throw new Error(`Unexpected status code: ${response.status}`);
    }
    
    return JSON.parse(response.body);
}
