import http from 'k6/http';
import { check, fail } from 'k6';
import { data } from './utils/data.js';
import chooseOptions from './options/choose_options.js';
import createTestUser from './utils/create_user.js'
const title = "POST /user";

export let options = chooseOptions(title);

const ENV = __ENV.ENV || 'local';
const url = `${data[ENV].api_service_base_url}/user`;

export function setup() {
  createTestUser(ENV)
}

export default function getAllUsers() {
  console.log(url);
  const response = http.get(url);
  console.log(response.body);
  
  if (!check(response, {
    "Create User Success": res => res.status === 200
  })) {
    fail(`Unexpected Status Code: ${response.status}`);
  }
}
